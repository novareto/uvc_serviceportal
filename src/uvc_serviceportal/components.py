# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


class BaseFormularObject(object):
    def __init__(self, id, title, description, schema, output, icon):
        self.id = id
        self.title = title
        self.description = description
        self.schema = schema
        self.output = output
        self.icon = icon

    def __html__(self):
        CARD_HTML = f"""
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{self.id}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{self.title}</h6>
            <p class="card-text">{self.description}</p>
            <a href="#" class="btn btn-primary card-link">Anlegen</a>
          </div>
        </div>
        """
        return CARD_HTML
