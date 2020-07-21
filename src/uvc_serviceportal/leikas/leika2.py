from pathlib import Path
from uvc_serviceportal.leikas.components import BaseFormularObject


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
