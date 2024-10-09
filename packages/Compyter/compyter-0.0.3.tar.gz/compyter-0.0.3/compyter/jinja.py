#!/usr/bin/env python3
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from compyte import render_content

class Jinja2TemplatesCompyte(Jinja2Templates):
    def jinja_render(self,template:str,scope:dict):
        rendered = self.get_template(template).render(scope)
        rendered = render_content(rendered,scope,path=template)
        return HTMLResponse(rendered)
