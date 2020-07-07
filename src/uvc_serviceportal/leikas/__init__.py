from pkg_resources import iter_entry_points
from uvc_serviceportal.components import BaseFormularObject


class Registry(dict):
    __slots__ = ()

    def register(self, name: str, form: BaseFormularObject):
        if name in self:
            raise KeyError(f'{name} already exists.')
        if not isinstance(form, BaseFormularObject):
            raise ValueError(f'{name} is not a valid formular class.')
        self[name] = form

    def load(self):
        self.clear()
        for loader in iter_entry_points('uvc_serviceportal.leikas'):
            self.register(loader.name, loader.load())


REGISTRY = Registry()
