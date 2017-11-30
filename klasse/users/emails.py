from templated_mail.mail import BaseEmailMessage


class ActivationEmail(BaseEmailMessage):
    template_name = 'emails/activation_email.txt'


class WelcomeEmail(BaseEmailMessage):
    template_name = 'emails/welcome_email.txt'
