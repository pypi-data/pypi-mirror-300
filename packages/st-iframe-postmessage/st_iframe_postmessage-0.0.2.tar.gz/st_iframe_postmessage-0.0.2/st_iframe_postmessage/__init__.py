import os

import streamlit.components.v1 as components

_RELEASE = True

if os.getenv('_ST_IFRAME_POSTMESSAGE_NOT_RELEASE_'):
    _RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_iframe_postmessage",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_iframe_postmessage", path=build_dir)


def st_iframe_postmessage(message: str | dict, target_origin: str = "*"):
    """

    Parameters
    ----------
    message: str|dict
        message to be sent
    target_origin: str
        target origin for post message
        defaults to "*" - for security reason change
    Returns
    -------
    None
    """
    component_value = _component_func(message=message, target_origin=target_origin, default=None)

    return component_value
