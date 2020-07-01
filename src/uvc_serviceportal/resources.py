# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import os
from fanstatic import Library, Resource, Group

library = Library('uvc_serviceportal', 'static')

css = Resource(library, 'uvc_serviceportal.css')


vendor = Resource(library, 'csc/dist/js/chunk-vendors.js')
#manifest = Resource(library, 'csc/dist/js/manifest.js')

class VueResource(Resource):

    def render(self, library_url):
        if os.environ.get('FANSTATIC_HMR_URL'):
            library_url = os.environ.get('FANSTATIC_HMR_URL')
        return super(VueResource, self).render(library_url)

app = VueResource(library, 'app.js', bottom=True)

csc = Group([app, vendor])

