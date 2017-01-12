from django import forms
from registration import validators
from registration.forms import RegistrationFormUniqueEmail, RegistrationForm


class RegistrationFormTermsOfServiceRu(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=(
            'Даю свое согласие на обработку моих персональных данных, предусмотренноеЗаконом Российской Федерации от 27 июля 2006 года № 152-ФЗ «О персональных данных».'),
        error_messages={
            'required': validators.TOS_REQUIRED,
        }
    )


class RegistrationFormTOSAndEmail(RegistrationFormUniqueEmail, RegistrationFormTermsOfServiceRu):
    pass

class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(required=True)
