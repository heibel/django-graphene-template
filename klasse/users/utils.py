from nameparser import HumanName

from django.core import signing

from klasse.users.emails import ActivationEmail, WelcomeEmail


def generate_activation_token(user):
    return signing.dumps(obj=user.email)


def parse_name(name):
    human_name = HumanName(name)

    return dict(
        first_name=human_name.first,
        middle_name=human_name.middle,
        last_name=human_name.last,
    )


def send_activation_email(user, request=None):
    activation_email = ActivationEmail(
        request=request,
        context={
            'user': user,
            'activation_token': generate_activation_token(user)
        })

    activation_email.send(to=[user.email])


def send_welcome_email(user, request=None):
    welcome_email = WelcomeEmail(
        request=request, context={
            'user': user,
        })

    welcome_email.send(to=[user.email])
