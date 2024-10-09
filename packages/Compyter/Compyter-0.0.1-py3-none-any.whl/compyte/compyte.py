#!/usr/bin/env python3

# Alfred Roos - Skibidi API Package
# License: MIT License
# GitHub: https://github.com/spynets/skibidi
#
# This file is part of the Skibidi API package developed by Alfred Roos.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
from bs4 import BeautifulSoup
from bs4.element import Tag
import black

load_tags = (r"{$",r"$}")  # Escaped for regex (for '{@')
load_pattern = r"{0}(.*?){1}".format(re.escape(load_tags[0]),re.escape(load_tags[1]))

exec_tags = (r"{@",r"@}")  # Escaped for regex (for '{@')
exec_pattern = r"{0}(.*?){1}".format(re.escape(exec_tags[0]),re.escape(exec_tags[1]))

def replace_components(html,local_scope):
    soup = BeautifulSoup(html, 'html.parser')

    components = soup.find_all(attrs={"component": True})
    comp: Tag
    for comp in components:
        comp.attrs['children'] = parse(comp.decode_contents(),local_scope)
        new_html = parse(open(comp.attrs['component'],"r").read(),local_scope,props=comp.attrs)
        comp.replace_with(BeautifulSoup(new_html, 'html.parser'))

    return soup.prettify()

def parse(template,local_scope, props: dict = {}):
    template = replace_components(template,local_scope)
    local_scope['props'] = props


    # Pattern to find exec blocks
    exec_matches = re.findall(load_pattern, template, re.S)

    for part in exec_matches:
        formatted_code = black.format_str(part, mode=black.FileMode())
        # print("exec", formatted_code, sep="\n")

        # Execute the code in the local scope
        exec(formatted_code,local_scope)  # Execute the code in the local scope

        # Remove the executed block from the template
        template = template.replace(load_tags[0] + part + load_tags[1], "")

    # Pattern to find eval blocks
    eval_matches = re.findall(exec_pattern, template, re.S)


    for part in eval_matches:
        formatted_code = black.format_str(part, mode=black.FileMode())
        # print("val", formatted_code, sep="\n")

        val = eval(formatted_code,local_scope)  # Use the same local scope
        template = template.replace(exec_tags[0] + part + exec_tags[1], str(val) if val is not None else "")

    return template
