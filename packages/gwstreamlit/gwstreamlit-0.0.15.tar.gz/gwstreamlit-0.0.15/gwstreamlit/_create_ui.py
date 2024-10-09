from typing import Optional

import streamlit as st
import pandas as pd

from gwstreamlit._utils import construct_function, option_function
from gwstreamlit.constants import ButtonLevel, MODAL_BUTTONS
from gwstreamlit.models import BaseConfig, InputFieldsBase, Button
from gwstreamlit.utils import disabled, build_label, fetch_boolean, _fetch_tab


def create_ui_tabs(gws):
    """Creates a list of tabs to be used in the UI"""
    tab_dict = {item.Tab: None for item in gws.model.Inputs if item.Tab is not None}
    if len([item for item in gws.model.Inputs if item.Tab is None]) > 0:
        tab_dict["Main"] = None

    for tab in gws.model.Tabs:
        tab_dict[tab.Label] = None
    tab_dict["Output"] = None

    tabs = st.tabs(tab_dict.keys())
    tab_position = 0

    for tab in tab_dict.keys():
        tab_dict[tab] = tabs[tab_position]
        tab_position += 1
    gws.tab_dict = tab_dict


def create_ui_title(gws):
    """Creates a title for the UI page and a description if it exists in the YAML file.
    If the title exists in the yaml file no buttons are generated."""
    try:
        st.header(gws.model.Name, divider="blue")
        if gws.model.Description is not None:
            st.markdown(gws.model.Description)
        if gws.model.Concept is not None:
            st.write(f"Concept by: {gws.model.Concept}")
        if gws.model.Developer is not None:
            st.write(f"Developed by: {gws.model.Developer}")
    except Exception as e:
        print(e)


def discover_functions(gws):
    """Discovers the functions in the YAML file, the functions are constructed and stored in the
    appropriate location in the model"""
    for button in [item for item in gws.model.Buttons]:
        button.OnClickFunction = on_click = construct_function(button.OnClick)

    for input_item in [item for item in gws.model.Inputs]:
        input_item.OnChangeFunction = construct_function(input_item.OnChange)
        if input_item.DefaultFunction is not None:
            input_item.DefaultFunctionBuilt = construct_function(input_item.DefaultFunction)
        if input_item.InputOptions is not None:
            if len(input_item.InputOptions) == 1 and input_item.InputOptions[0].Function is not None:
                function_name = input_item.InputOptions[0].Function
                input_item.InputOptions[0].OptionsFunction = construct_function(function_name)



def create_ui_buttons(gws):
    """Generates a set of buttons based on the YAML file provided"""
    with st.container():
        columns = st.columns([1, 1, 1, 1, 1])
        column_index = 0
        for button in [item for item in gws.model.Buttons if item.Level is not ButtonLevel.tab]:
            with columns[column_index]:
                try:
                    on_click = button.OnClickFunction
                    if button.Icon is None:
                        icon = None
                    else:
                        icon = f":material/{button.Icon}:"
                    st.button(f"{button.Label}", key=button.Key, on_click=on_click, type=button.Variant.value,
                              use_container_width=True)
                except Exception as e:
                    pass
            column_index += 1


def create_tab_buttons(gws):
    """Generates a set of buttons based on the YAML file provided"""
    button_tab_list = [item.Tab for item in gws.model.Buttons if item.Level == ButtonLevel.tab]
    if len(button_tab_list) == 0:
        return
    for tab in button_tab_list:
        with _fetch_tab(tab):
            with st.container():
                columns = st.columns([1, 1, 1, 1, 1])
                column_index = 4
                button_list = [item for item in gws.model.Buttons if item.Tab == tab and
                               item.Level == ButtonLevel.tab]
                for button in list(reversed(button_list)):
                    if button.Popover is not None:
                        with st.popover(button.Label):
                            create_modal()
                    if button.Key in st.session_state:
                        continue
                    with columns[column_index]:
                        on_click = construct_function(button.OnClick)
                        st.button(f"{button.Label}", key=button.Key, on_click=on_click,
                                  type=button.Variant.value, use_container_width=True)
                    column_index -= 1


def create_ui_inputs(gws):
    """Main processing for the inputs defined in the yaml file. Each type of input
    is handled separately. Each input has a key generated that corresponds to the label or code
    and the state name defined in the main module for the application"""
    if gws.model.Inputs is None:
        return
    for ui_item in gws.model.Inputs:
        build_input(gws, ui_item)


def build_input(gws, ui_item):
    """Main processing for the inputs defined in the yaml file. Each type of input
    is handled separately. Each input has a key generated that corresponds to the label or code
    and the state name defined in the main module for the application"""

    if ui_item.Key not in gws.input_values.keys():
        gws.input_values[ui_item.Key] = None

    if ui_item.Type == 'text_input':
        generate_text_input(gws, ui_item, None)

    if ui_item.Type == 'text_area':
        generate_text_input(gws, ui_item, None, True)

    if ui_item.Type == "selectbox":
        generate_selectbox(gws, ui_item, None)

    if ui_item.Type == "image":
        generate_image(gws, ui_item)

    if ui_item.Type == "checkbox":
        generate_checkbox(gws, ui_item, None)

    if ui_item.Type == "toggle":
        generate_checkbox(gws, ui_item, None, True)

    if ui_item.Type == "integer_input":
        generate_integer_input(gws, ui_item, None)

    if ui_item.Type == "file_upload":
        generate_file_upload(gws, ui_item, None)

    if ui_item.Type == "multiselect":
        generate_selectbox(gws, ui_item, None, True)

    if ui_item.Type == "table":
        generate_table(gws, ui_item)

    return ui_item.Key


def generate_text_input(gws, item, input_values, text_area=False):
    """text input processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in
    the YAML file."""
    default_value = item.Default
    if item.DefaultFunction:
        defined_function = item.DefaultFunctionBuilt
        default_value = defined_function()

    if gws.input_values.get(item.Key, None) is not None:
        default_value = gws.input_values[item.Key]

    on_change = item.OnChangeFunction
    disabled_input = disabled(item)
    if item.Key not in st.session_state.keys():
        st.session_state[item.Key] = default_value
    # else:
    #     st.session_state[item.Key] = st.session_state.get(item.Key)
    # if st.session_state[item.Key] is None:
    #     st.session_state[item.Key] = default_value
    try:
        if text_area:
            gws.input_values[item.Key] = _fetch_tab(item).text_area(build_label(item), key=item.Key,
                                                                    on_change=on_change, disabled=disabled_input)
        else:
            gws.input_values[item.Key] = _fetch_tab(item).text_input(build_label(item),
                                                                     key=item.Key,
                                                                     on_change=on_change, disabled=disabled_input)
    except Exception as e:
        st.write(e)
    if item.ShortKey in st.session_state.get("common_storage", {}):
        st.session_state["common_storage"][item.ShortKey] = st.session_state[item.Key]


def generate_image(gws, item):
    if item.Image is not None:
        caption = f"{build_label(item)} - {item.Image}"
        _fetch_tab(item).image(item.Image, caption=caption)


def generate_checkbox(gws, item: BaseConfig, input_values, toggle=False):
    """Check Box Processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in the
    YAML file."""
    default_value = item.Default
    if gws.input_values.get(item.Key, None) is not None:
        default_value = gws.input_values[item.Key]
    on_change = item.OnChangeFunction
    disabled_field = fetch_boolean(item.Immutable)
    try:
        if not toggle:
            gws.input_values[item.Key] = _fetch_tab(item).checkbox(build_label(item), default_value, key=item.Key,
                                                                   on_change=on_change, disabled=disabled_field)
        else:
            gws.input_values[item.Key] = _fetch_tab(item).toggle(build_label(item), default_value, key=item.Key,
                                                                 on_change=on_change, disabled=disabled_field)
    except Exception as e:
        st.write(e)


def generate_file_upload(gws, item, input_values):
    """File Upload Processing. The extension is used to set the type of file that can be uploaded.
    The on_change function is constructed based on the name provided in the YAML file.
    The input is disabled if the immutable flag is set in the YAML file."""
    try:
        on_change = item.OnChangeFunction
        gws.input_values[item.Key] = _fetch_tab(item).file_uploader(build_label(item), type=item.Extension,
                                                                    accept_multiple_files=False, key=item.Key,
                                                                    on_change=on_change)
    except Exception as e:
        st.write(e)


def generate_integer_input(gws, item: InputFieldsBase, input_values):
    """Integer Input Processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in the
    YAML file. The min and max values are used to set the range of the input."""
    if item.Min:
        min_value = item.Min
    else:
        min_value = 0

    if item.Max:
        max_value = item.Max
    else:
        max_value = 100

    if gws.input_values.get(item.Key, None):
        default_value = gws.input_values[item.Key]
    else:
        default_value = min_value
    try:
        on_change = item.OnChangeFunction
        disabled_field = fetch_boolean(item.Immutable)
        gws.input_values[item.Key] = _fetch_tab(item).number_input(build_label(item), value=default_value,
                                                                   key=item.Key, step=1, min_value=min_value,
                                                                   max_value=max_value, on_change=on_change,
                                                                   disabled=disabled_field)
    except Exception as e:
        st.write(e)


def generate_selectbox(gws, item: BaseConfig, input_values, multiselect=False):
    """select box processing. The default value is used if it exists in the YAML file. If the value is already
    in the input_values dictionary it is used instead of the default value. The on_change function is constructed
    based on the name provided in the YAML file. The input is disabled if the immutable flag is set in the
    YAML file.
    If the options are defined as a function the function is called to get the options. If the default value is not
    in the options list the first option is used as the default value."""
    options_dict = options_list(gws, item)
    options = options_dict.get("options")
    default_value = options_dict.get("default_value")
    on_change = item.OnChangeFunction
    if options is not None and len(options) > 0 and default_value is not None:
        index_value = options.index(default_value)
    else:
        index_value = None
    disabled_field = fetch_boolean(item.Immutable)
    if item.Key in gws.input_values.keys():
        st.session_state[item.Key] = st.session_state.get(item.Key)
    if st.session_state.get(item.Key) is None and default_value is not None:
        st.session_state[item.Key] = default_value
    try:
        if multiselect:
            gws.input_values[item.Key] = _fetch_tab(item).multiselect(build_label(item), options,
                                                                      key=item.Key, on_change=on_change,
                                                                      disabled=disabled_field)
        else:
            gws.input_values[item.Key] = _fetch_tab(item).selectbox(build_label(item), options, index=index_value,
                                                                    key=item.Key,
                                                                    on_change=on_change,
                                                                    disabled=disabled_field)
    except Exception as e:
        st.write(e)


def generate_table(gws, item):
    """Main Processing for table generation. Each table is backed by a dataframe that is stored
    in self.data_frame."""
    default_rows = gws.default_rows.get(item.Label, dict())
    generate_dataframe(gws, item, default_rows)


def generate_dataframe(gws, item: InputFieldsBase, default_rows: dict):
    """Generate the Table Dataframe. The default rows are used to populate the dataframe if it is empty. The columns
    are generated based on the YAML file provided. The dataframe is stored in self.data_frame and can be updated"""
    if item.Columns is None:
        return

    if item.Columns[0].Function is not None:
        defined_function = construct_function(item.Columns[0].Function)
        columns = defined_function()
    else:
        columns = [entity_item.Label for entity_item in item.Columns]
    df_key = f"{item.Key}_df"
    if df_key in st.session_state.keys():
        df = st.session_state[df_key]
    else:
        df = pd.DataFrame(columns=columns, data=default_rows)
        if item.Order:
            df.sort_values(by=[item.Order], inplace=True, ignore_index=True)

    column_config = create_column_config(gws, item.Columns)
    _fetch_tab(item).markdown(f"**{item.Label}**")

    st.session_state[df_key] = df
    try:
        if item.Immutable:
            _fetch_tab(item).dataframe(st.session_state[df_key], hide_index=True, column_config=column_config,
                                       use_container_width=True, key=item.Key, selection_mode="single-row",
                                       on_select="rerun")
        else:
            _fetch_tab(item).data_editor(st.session_state[df_key], num_rows="dynamic", column_config=column_config,
                                         use_container_width=True, key=item.Key)
    except Exception as e:
        st.write(e)


def create_column_config(gws, columns: list[InputFieldsBase]):
    """Define the column configuration for the data editor, multiselect is not supported in the data editor and
    list column is used"""
    column_config = {}
    for column_item in columns:
        column = column_item.Label
        if column is None:
            column = column_item
        if column_item.InputOptions:
            options_dict = options_list(gws, column_item)
            options = options_dict.get("options")
            default_value = options_dict.get("default_value")
            column_config[column] = st.column_config.SelectboxColumn(options=options, default=default_value)
        if column_item.Type == "checkbox":
            column_config[column] = st.column_config.CheckboxColumn(default=False)
        if column_item.Type == "integer_input":
            min_value = column_item.get('min', -1)
            max_value = column_item.get('max', 100)
            column_config[column] = st.column_config.NumberColumn(max_value=max_value, min_value=min_value, step=1,
                                                                  default=-1)
        if column_item.Type == "multiselect":
            column_config[column] = st.column_config.ListColumn()
    return column_config


def options_list(gws, item):
    defined_option_function = item.InputOptions[0].OptionsFunction
    default_value: Optional[str] = item.Default
    if defined_option_function is None:
        options = [option.Value for option in item.InputOptions]
        if item.Default not in options:
            default_value = item.InputOptions[0].Value
        if gws.input_values.get(item.Key, None) is not None:
            default_value = gws.input_values[item.Key]
    else:
        options = defined_option_function()
    return {"options": options, "default_value": default_value}


def create_modal():
    """Creates a modal dialog for the input fields"""
    st.text_input("Code")
    st.text_input("Name")
    if st.button("Submit"):
        st.write("Submit pressed")


def modal_buttons():
    """Creates a set of buttons for the modal dialog"""
    button_list = []
    for button_default in MODAL_BUTTONS:
        button_list.append(Button.model_validate(button_default))

    with st.container():
        columns = st.columns([1, 1, 1, 1, 1])
        column_index = 0
        for button in button_list:
            with columns[column_index]:
                on_click = construct_function(button.OnClick)
                st.button(f"{button.Label}", key=button.Key, on_click=on_click, type=button.Variant.value,
                          use_container_width=True)
            column_index += 1
