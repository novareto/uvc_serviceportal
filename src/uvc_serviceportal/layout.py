import wrapt
import horseman.response
from pathlib import Path
from chameleon import PageTemplateLoader
from uvc_serviceportal.resources import css, bootstrap, csc


TEMPLATES = PageTemplateLoader(
    str((Path(__file__).parent / 'templates').resolve()), ".pt")


class Layout:

    def __init__(self, name, **namespace):
        self._template = TEMPLATES[name]
        self._namespace = namespace

    @property
    def macros(self):
        return self._template.macros

    def render(self, content, **extra):
        css.need()
        csc.need()
        bootstrap.need()
        ns = {**self._namespace, **extra}
        return self._template.render(content=content, **ns)


def xml_endpoint(template_name: str):
    template = TEMPLATES[template_name]

    @wrapt.decorator
    def render(endpoint, instance, args, kwargs):
        result = endpoint(*args, **kwargs)
        if isinstance(result, horseman.response.Response):
            return result
        assert isinstance(result, dict)

        content = template.render(**result)
        return horseman.response.reply(
            body=content,
            headers={'Content-Type': 'application/xml'})

    return render


layout = Layout('layout.pt')

def template_endpoint(template_name: str, layout=layout):
    template = TEMPLATES[template_name]

    @wrapt.decorator
    def render(endpoint, instance, args, kwargs):
        result = endpoint(*args, **kwargs)
        if isinstance(result, horseman.response.Response):
            return result
        assert isinstance(result, dict)

        request = args[0]
        path = request.environ['PATH_INFO']
        content = template.render(macros=layout.macros, **result)
        if layout is not None:
            body = layout.render(content, path=path, user=request.user)
            return horseman.response.reply(
                body=body,
                headers={'Content-Type': 'text/html; charset=utf-8'})
        return horseman.response.reply(
            body=content,
            headers={'Content-Type': 'text/html; charset=utf-8'})

    return render
