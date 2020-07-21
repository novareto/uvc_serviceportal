from urllib.parse import parse_qs, urlparse

from onelogin.saml2.utils import OneLogin_Saml2_Utils

import horseman.meta
import horseman.response
import horseman.http
import roughrider.routing.node
from roughrider.routing.route import add_route as route

from uvc_serviceportal.app import app
from uvc_serviceportal.layout import template_endpoint
from uvc_serviceportal.request import Request


def redirect(url):
    return horseman.response.reply(code=302, headers={'Location': url})


@app.route('/saml/attrs')
@template_endpoint('attrs.pt')
def attrs(request: Request):
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return {'paint_logout': paint_logout, 'attributes': attributes}


@app.route('/saml/metadata')
def metadata(request: Request):
    auth = request.saml_auth()
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        return horseman.response.reply(
            body=metadata,
            headers={'Content-Type': 'text/xml'})

    return horseman.response.reply(code=500, body=', '.join(errors))


@app.route('/saml/sso', methods=['GET'])
def sso(request):
    auth = request.saml_auth()
    # If AuthNRequest ID need to be stored in order to later validate it, do instead
    # sso_built_url = auth.login()
    # request.session['AuthNRequestID'] = auth.get_last_request_id()
    # return redirect(sso_built_url)
    return redirect(auth.login())


@app.route('/saml/sso2', methods=['GET'])
def sso2(request):
    return_to = '/saml/attrs'
    auth = request.saml_auth()
    return redirect(auth.login(return_to))


@app.route('/saml/slo', methods=['GET'])
def slo(request):
    auth = request.saml_auth()
    name_id = request.session.get('samlNameId')
    session_index = request.session.get('samlSessionIndex')
    name_id_format = request.session.get('samlNameIdFormat')
    name_id_nq = request.session.get('samlNameIdNameQualifier')
    name_id_spnq = request.session.get('samlNameIdSPNameQualifier')
    return redirect(auth.logout(
        name_id=name_id,
        session_index=session_index,
        nq=name_id_nq,
        name_id_format=name_id_format,
        spnq=name_id_spnq)
    )

@app.route('/saml/acs', methods=['GET', 'POST'])
@template_endpoint('saml.pt')
def acs(request):
    error_reason = None
    attributes = paint_logout = False

    auth = request.saml_auth()
    request_id = request.session.get('AuthNRequestID')
    auth.process_response(request_id=request_id)
    errors = auth.get_errors()
    not_auth_warn = not auth.is_authenticated()

    if len(errors) == 0:
        if 'AuthNRequestID' in request.session:
            del request.session['AuthNRequestID']
        request.session['samlUserdata'] = auth.get_attributes()
        request.session['samlNameId'] = auth.get_nameid()
        request.session['samlNameIdFormat'] = auth.get_nameid_format()
        request.session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
        request.session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
        request.session['samlSessionIndex'] = auth.get_session_index()
        self_url = OneLogin_Saml2_Utils.get_self_url(request.saml_environ)
        if RelayState := request.data['form'].get('RelayState'):
            return redirect(auth.redirect_to(RelayState))
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if request.user is not None:
        attributes = request.user.data

    return {
        'errors': errors,
        'error_reason': error_reason,
        'not_auth_warn': not_auth_warn,
        'success_slo': False,
        'attributes': attributes,
        'paint_logout': paint_logout
    }


@app.route('/saml/sls', methods=['GET', 'POST'])
@template_endpoint('saml.pt')
def sls(request):
    auth = request.saml_auth()
    request_id = request.session.get('LogoutRequestID')
    dscb = lambda: request.session.clear()
    url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
    errors = auth.get_errors()
    if len(errors) == 0:
        if url is not None:
            return redirect(url)
        else:
            success_slo = True
    elif auth.get_settings().is_debug_active():
        error_reason = auth.get_last_error_reason()

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()
    return {
        'errors': [],
        'error_reason': None,
        'not_auth_warn': False,
        'success_slo': False,
        'attributes': request.user.attributes,
        'paint_logout': paint_logout
    }
