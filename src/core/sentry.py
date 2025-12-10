from . import settings


def init_sentry() -> None:
    if not settings.sentry_dsn:
        return

    import logging

    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration

    logging.captureWarnings(True)

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        traces_sample_rate=settings.traces_sample_rate,
        integrations=[LoggingIntegration(event_level=logging.WARNING)],
    )
