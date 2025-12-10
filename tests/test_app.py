from unittest.mock import Mock

from core import make_app


def test_make_app_kwargs(api):
    summary = 'Test app'
    app = make_app(summary=summary)
    assert app.title == 'tiny-service-core'
    assert app.summary == summary


def test_make_app_routers(api):
    api.add_public_api = Mock()

    make_app()

    api.add_public_api.assert_called_once()
