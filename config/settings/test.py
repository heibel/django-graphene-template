import os

from config.settings.base import BASE_DIR, Base


class NoMigrations(object):

    def __getitem__(self, item):
        return None

    def __contains__(self, item):
        return True


class Test(Base):

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "y5y4%&fcjd&o&+h&%fu8=+*(mq0%g7jo3)!3=1%ot^0ccehy6z"

    # DEBUG
    # ------------------------------------------------------------------------------
    # Turn debug off so tests run faster
    DEBUG = False

    # Mail settings
    # ------------------------------------------------------------------------------
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025

    # In-memory email backend stores messages in django.core.mail.outbox
    # for unit testing purposes
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    # CACHING
    # ------------------------------------------------------------------------------
    # Speed advantages of in-memory caching without having to run Memcached
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # PASSWORD HASHING
    # ------------------------------------------------------------------------------
    # Use fast password hasher so tests run faster
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

    # DATABASE CONFIGURATION
    # ------------------------------------------------------------------------------
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
        }
    }

    MIGRATION_MODULES = NoMigrations()

    @property
    def TEMPLATES(self):
        templates = super(Test, self).TEMPLATES

        # Turn debug off so tests run faster
        templates[0]["OPTIONS"]["debug"] = False

        return templates
