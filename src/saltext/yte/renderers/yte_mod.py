"""
Salt renderer module
"""

import logging

from yte import process_yaml

log = logging.getLogger(__name__)

__virtualname__ = "yte"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The yte renderer module is not implemented yet")
    return __virtualname__


def render(data, saltenv="base", sls="", **kwargs):
    """
    Render yte data into a dictionary.
    """
    result = process_yaml(
        data,
        variables=dict(
            salt=__salt__,
            grains=__grains__,
            opts=__opts__,
            pillar=__pillar__,
            saltenv=saltenv,
            sls=sls,
            proxy=__proxy__,
            **kwargs,
        ),
    )
    log.debug(f"Rendered yte data: {result}")
    return result
