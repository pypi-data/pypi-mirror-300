from pathlib import Path
from typing import Any

import streamlit as st
import gwstreamlit._create_ui as gwu

from gwstreamlit._utils import build_default_rows
from gwstreamlit.models import UserInterface, InputFields
from gwstreamlit.process_templates import _process_template_by_name
from gwstreamlit.utils import (find_yaml_ui, find_yaml_other, build_model, _fetch_key, _fetch_configs,
                               _completed_required_fields, _create_saved_state, _save_config, _load_config,
                               _write_string, _fetch_tab, _create_storage_key, _show_info, _show_warning, _show_error,
                               codeify_string)


class GWStreamlit:

    def create_ui(self, modal: bool = False):
        """Builds the UI for the application when the ui is for a modal only the inputs are created"""
        if self.built_ui:
            return
        gwu.create_ui_title(self)
        gwu.create_ui_buttons(self)
        if not self.model.Title:
            gwu.create_ui_tabs(self)
        gwu.create_tab_buttons(self)
        gwu.create_ui_inputs(self)
        self.built_ui = True



    def find_model_part(self, identifier: str):
        """Finds a model part by the identifier provided. The identifier can be the code or the
        label of the item. If the item is not found None is returned.
        @param identifier: str"""
        items = [item for item in self.model.Inputs if codeify_string(item.Code) == codeify_string(identifier)]
        if len(items) == 0:
            items = [item for item in self.model.Inputs if item.Label == identifier]
        if len(items) == 0:
            return None
        return items[0]

    def __init__(self, application: str = None, yaml_file: dict = None):
        self.application = application
        self.yaml_file = yaml_file
        self.model = build_model(self.yaml_file)
        self.keys = []
        self.input_values = {}
        self.button_values = {}
        self.built_ui = False
        self.tab_dict = {}
        self.default_rows = build_default_rows(self)
        self.child = None
        self.saved_state: dict
        self.modal = False
        self.common_storage = {}

    def populate(self, application: str = None, yaml_file: dict = None):
        self.application = application
        self.yaml_file = yaml_file
        self.model = build_model(self.yaml_file)
        self.default_rows = build_default_rows(self)
        self.built_ui = False
        set_common_storage(self.yaml_file)
        gwu.discover_functions(self)

def set_common_storage(yaml_file: dict):
    if "common_storage" not in st.session_state:
        st.session_state["common_storage"] = {}
    common_storage = st.session_state["common_storage"]
    if "common_storage" in yaml_file:
        for item in yaml_file["common_storage"]:
            if item.get("value") not in common_storage:
                common_storage[item.get("value")] = None
                ...


def initialize(application: str, yaml_file_name: str):
    """Initializes the application"""
    if has_modal():
        return
    if Path(yaml_file_name).name == yaml_file_name:
        yaml_file = find_yaml_ui(yaml_file_name)
    else:
        yaml_file = find_yaml_other(yaml_file_name)
    st.session_state["GWStreamlit"].populate(application, yaml_file)
    st.session_state["GWStreamlit"].create_ui()


def required_fields() -> bool:
    """Checks if all required fields have been completed"""
    return _completed_required_fields()


def fetch_key(ui_item: Any) -> str:
    """Fetches the key for the item provided"""
    return _fetch_key(ui_item)


def fetch_configs(application_name: str = None) -> list:
    """Extract the configurations for the application"""
    if application_name is None:
        application_name = st.session_state["GWStreamlit"].application
    return _fetch_configs(application_name)


def create_saved_state(*, short_key: bool = False):
    """Creates a saved state for the application"""
    return _create_saved_state(short_key=short_key)


def save_config(file_name, config_data: None):
    """Save the configuration information"""
    if config_data is None:
        config_data = create_saved_state()
    application_name = st.session_state["GWStreamlit"].application
    _save_config(application_name, file_name, config_data)


def load_config(file_name):
    """Loads a configuration file"""
    _load_config(file_name)


def process_template_by_name(template_name, input_dict: dict, location="resources/templates"):
    """Processes a template by name"""
    return _process_template_by_name(template_name, input_dict, location)


def write_string(location, file_name, content, **kwargs):
    """Writes a string to a file"""
    _write_string(location, file_name, content, **kwargs)


def fetch_tab(item: Any):
    """Fetches a tab by the item provided"""
    return _fetch_tab(item)


def create_storage_key(value: str) -> str:
    """Creates a storage key for the value provided"""
    return _create_storage_key(value)


def generate_image(item):
    gws = st.session_state["GWStreamlit"]
    gwu.generate_image(gws, item)


def find_model_part(identifier: str):
    gws = st.session_state["GWStreamlit"]
    return gws.find_model_part(identifier)


def show_info(message, tab=None):
    _show_info(message, tab)


def show_warning(message, tab=None):
    _show_warning(message, tab)


def show_error(message, tab=None):
    _show_error(message, tab)


def model() -> UserInterface:
    gws = st.session_state["GWStreamlit"]
    return gws.model


def model_inputs() -> list[InputFields]:
    gws = st.session_state["GWStreamlit"]
    return gws.model.Inputs


def value(identifier: str):
    item = find_model_part(identifier)
    if item is None:
        key = create_storage_key(identifier)
        return st.session_state.get(key, None)
    else:
        return st.session_state.get(item.Key, None)


def save_storage(key, storage_value: Any):
    key = create_storage_key(key)
    st.session_state[key] = storage_value


def has_modal() -> bool:
    gws = st.session_state.get("GWStreamlit", None)
    if gws is None:
        return False
    return gws.modal


def fetch_value(name: str):
    item_value = st.session_state.get(fetch_key(name), None)
    if item_value is None:
        item_value = st.session_state["common_storage"].get(name, None)
    return item_value
