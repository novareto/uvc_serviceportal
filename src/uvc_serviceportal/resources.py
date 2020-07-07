# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import os
from fanstatic import Library, Resource, Group

library = Library('uvc_serviceportal', 'static')

css = Resource(library, 'uvc_serviceportal.css')


vendor = Resource(library, 'dist/js/chunk-vendors.js')
#manifest = Resource(library, 'csc/dist/js/manifest.js')

class VueResource(Resource):

    def render(self, library_url):
        if os.environ.get('FANSTATIC_HMR_URL'):
            library_url = os.environ.get('FANSTATIC_HMR_URL')
        import pdb; pdb.set_trace()
        return super(VueResource, self).render(library_url)

app = VueResource(library, 'dist/js/app.js', bottom=True)

csc = Group([app, vendor])



#
### BOOSTRAP STUFF
#


bootstrap_css = Resource(library, 'uvc_serviceportal_bootrap.css', compiler="sass", source="scss/siguv.scss")
bootstrap_js = Resource(library, 'bootstrap.bundle.js', bottom=True)

bootstrap = Group([bootstrap_css, bootstrap_js])
