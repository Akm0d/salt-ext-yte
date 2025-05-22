import pytest
import saltext.yte.renderers.yte_mod as yte_renderer


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"test.echo": lambda x: x},
        "__proxy__": {},
        "__grains__": {},
        "__opts__": {},
        "__pillar__": {},
    }
    return {
        yte_renderer: module_globals,
    }


def test_render_conditional():
    SLS = """
    test:
        ?if True:
            test.succeed_without_changes
        ?else:
            test.fail_without_changes
    """
    result = yte_renderer.render(SLS, saltenv="base", sls="test")
    assert result == {"test": "test.succeed_without_changes"}


def test_render_loop():
    SLS = """
    ?for i in range(3):
        ?f"test-{i}": test.succeed_without_changes
    """
    result = yte_renderer.render(SLS, saltenv="base", sls="test")
    assert result == {
        "test-0": "test.succeed_without_changes",
        "test-1": "test.succeed_without_changes",
        "test-2": "test.succeed_without_changes",
    }


def test_render_salt():
    SLS = """
    ?salt['test.echo']('test'):
        test.succeed_without_changes
    """
    result = yte_renderer.render(SLS, saltenv="base", sls="test")
    assert result == {"test": "test.succeed_without_changes"}
