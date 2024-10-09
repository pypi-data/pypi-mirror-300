import streamlit as st
from jinja2 import FileSystemLoader, Environment, select_autoescape, TemplateNotFound

from gwstreamlit.utils import _fetch_tab


def _process_template_by_name(template_name, input_dict: dict, location):
    gw_streamlit = st.session_state["GWStreamlit"]
    env = Environment(
            loader=FileSystemLoader(location),
            autoescape=select_autoescape(),
            trim_blocks=True,
    )
    template_result = None
    try:
        template = env.get_template(template_name)
        template_result = template.render(input_dict)
    except TemplateNotFound:
        _fetch_tab("Output").warning(f"Template - {template_name} was not found")

    return template_result
