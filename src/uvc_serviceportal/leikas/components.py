# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import json
from pkg_resources import iter_entry_points



class BaseFormularObject:

    def __init__(self, id, title, description, schema, output, icon):
        self.id = id
        self.title = title
        self.description = description
        self.schema = schema
        self.output = output
        self.icon = icon

    def as_dict(self):
        return dict(id=self.id, title=self.title, description=self.description, icon=self.icon)

    def __html__(self):
        CARD_HTML = f"""
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{self.id}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{self.title}</h6>
            <p class="card-text">{self.description}</p>
            <a href="/{self.id}" class="btn btn-primary card-link">
                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-plus" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" d="M8 3.5a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5H4a.5.5 0 0 1 0-1h3.5V4a.5.5 0 0 1 .5-.5z"/>
                  <path fill-rule="evenodd" d="M7.5 8a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1H8.5V12a.5.5 0 0 1-1 0V8z"/>
                </svg>
                Anlegen
            </a>
          </div>
        </div>
        """
        return CARD_HTML


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

    def json(self):
        return json.dumps([x.as_dict() for x in self.values()])



REGISTRY = Registry()
