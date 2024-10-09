from typing import Any, Dict

from pydantic import BaseModel, Field

from gwstreamlit.constants import ButtonVariantType, ButtonLevel


class Option(BaseModel):
    Value: str = Field(alias="value", default=None)
    Function: str = Field(alias="function", default=None)
    OptionsFunction: Any = Field(alias="function_function", default=None)

class DefaultRow(BaseModel):
    Header: str = Field(alias="row_header", default=None)
    Row: str = Field(alias="row", default=None)


class BaseConfig(BaseModel):
    Code: str = Field(alias="code", default=None)
    Label: str = Field(alias="label", default=None)
    Enabled: str = Field(alias="enabled", default=None)
    OnClick: str = Field(alias="on_click", default=None)
    OnClickFunction: Any = Field(alias="on_click_function", default=None)
    OnChange: str = Field(alias="on_change", default=None)
    OnChangeFunction: Any = Field(alias="on_change_function", default=None)
    Tab: str = Field(alias="tab", default="Main")
    Default: Any = Field(default=None, alias="default")
    DefaultFunction: str = Field(default=None, alias="default_function")
    DefaultFunctionBuilt: str = Field(default=None, alias="default_function_built")
    Extension: str = Field(default=None, alias="extension")
    Icon: str = Field(default=None, alias="icon")
    Immutable: bool = Field(default=False, alias="immutable")
    Key: str = Field(default=None)
    ShortKey: str = Field(default=None)
    InputOptions: list[Option] = Field(default=None, alias="options")


class Button(BaseConfig):
    Variant: ButtonVariantType = Field(default=ButtonVariantType.secondary, alias="variant")
    Level: ButtonLevel = Field(default=ButtonLevel.application, alias="level")
    Popover: bool = Field(default=None, alias="popover")


class Tab(BaseConfig):
    pass


class InputFieldsBase(BaseConfig):
    Type: str = Field(default="text_input", alias="type")
    Required: bool = Field(default=False, alias="required")
    Min: int = Field(default=None, alias="min")
    Max: int = Field(default=None, alias="max")
    Order: str = Field(default=None, alias="order")
    Function: str = Field(alias="function", default=None)
    DefaultRows: list[DefaultRow] = Field(default=[], alias="default_rows")


class InputFields(InputFieldsBase):
    Image: str = Field(default=None, alias="image")
    Columns: list[InputFieldsBase] = Field(default=[], alias="columns")


class UserInterface(BaseConfig):
    Name: str = Field(alias="name")
    Description: str = Field(alias="description", default=None)
    Developer: str = Field(alias="developer", default=None)
    Concept: str = Field(alias="concept", default=None)
    Title: bool = Field(default=False, alias="title")
    Inputs: list[InputFields] = Field(default=[], alias="inputs")
    Tabs: list[Tab] = Field(default=[], alias="tabs")
    Buttons: list[Button] = Field(default=[], alias="buttons")
