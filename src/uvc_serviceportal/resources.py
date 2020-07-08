# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import os
from fanstatic import Library, Resource, Group

library = Library('uvc_serviceportal', 'static')

css = Resource(library, 'uvc_serviceportal.css')


vendor = Resource(library, 'vuedist/js/chunk-vendors.js')
#manifest = Resource(library, 'csc/dist/js/manifest.js')


SCRIPT = "<script defer type='text/javascript' src='%s'></script>"


class VueResource(Resource):

    def render(self, library_url):
        if os.environ.get('FANSTATIC_HMR_URL'):
            return SCRIPT % 'http://localhost:8080/js/chunk-vendors.js' + SCRIPT % os.environ.get('FANSTATIC_HMR_URL') 
        return super(VueResource, self).render(library_url)

app = VueResource(library, 'vuedist/js/app.js', bottom=True)

csc = Group([vendor, app])



#
### BOOSTRAP STUFF
#


bootstrap_css = Resource(library, 'uvc_serviceportal_bootstrap.css', compiler="sass", source="scss/siguv.scss")
bootstrap_js = Resource(library, 'bootstrap.bundle.js', bottom=True)

bootstrap = Group([bootstrap_css, bootstrap_js])
