
from pathlib import Path
import horseman.parsing
import horseman.response
import horseman.meta
from uvc_serviceportal.layout import template_endpoint, xml_endpoint
from uvc_serviceportal import ROUTES
from uvc_serviceportal.leikas.components import REGISTRY
from uvc_serviceportal.leikas.components import BaseFormularObject
from uvc_serviceportal.resources import csc
from autoroutes import Routes
from roughrider.routing.route import add_route as route
from uvc_serviceportal.mq import Message


PATH = Path(__file__)


class Leika2(BaseFormularObject):
    def __init__(self, *args, **kwargs):
        with PATH.with_suffix(".json").open() as fd:
            kwargs["jsonschema"] = fd.read()
        super().__init__(*args, **kwargs)

    @property
    def action(self):
        return "%s/add" % self.id


LEIKA = Leika2(
    id="leika3",
    title="Wohnungshilfe",
    description=u"Wohnungshilfe für gesetzlich Unfallversicherte Gewährung",
    security_level="Q1",
    tags=["Unfall", "Sicherheitsfachkraft"],
    output="<xml><uv><name>{name}</name></uv>",
    icon="bi bi-chevron-right",
)
