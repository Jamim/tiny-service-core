from unittest.mock import ANY, patch

from core import make_app, settings


@patch('sentry_sdk.init')
@patch.object(settings, 'sentry_dsn', 'sentry-dsn')
def test_sentry(init, api):
    make_app()

    init.assert_called_once_with(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        traces_sample_rate=settings.traces_sample_rate,
        integrations=[ANY],
    )
