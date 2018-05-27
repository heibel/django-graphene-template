from config.settings.base import Base


class Local(Base):

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "y5y4%&fcjd&o&+h&%fu8=+*(mq0%g7jo3)!3=1%ot^0ccehy6z"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    # Email
    # https://docs.djangoproject.com/en/1.11/topics/email/
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    @property
    def GRAPHENE(self):
        graphene = super(Local, self).GRAPHENE

        graphene["MIDDLEWARE"] = ("graphene_django.debug.DjangoDebugMiddleware",)

        return graphene
