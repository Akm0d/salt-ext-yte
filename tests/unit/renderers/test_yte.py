import pytest
import saltext.yte.renderers.yte_mod as yte_renderer


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        yte_renderer: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in yte_renderer.__salt__
    assert yte_renderer.__salt__["this_does_not_exist.please_replace_it"]() is True
