import sentry_sdk

from settings import settings


def init_sentry():
    if settings.sentry_dsn:
        sentry_sdk.init(settings.sentry_dsn, environment=settings.environment)
