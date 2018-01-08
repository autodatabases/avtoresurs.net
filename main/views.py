from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import render_to_string

from avtoresurs_new import settings
from main.forms import ResendActivationEmailForm

from registration.forms import User


# todo make CBV
def resend_activation_email(request):
    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    context = Context()

    form = None
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email, is_active=0)

            if not users.count():
                form._errors["email"] = 'Учетная запись на таком e-mail не найдена или уже зарегистрирована.'

            REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')
            print(REGISTRATION_SALT)
            for user in users:
                activation_key = signing.dumps(
                    obj=getattr(user, user.USERNAME_FIELD),
                    salt=REGISTRATION_SALT,
                )
                context = {}
                context['activation_key'] = activation_key
                context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
                context['site'] = get_current_site(request)

                subject = render_to_string(email_subject_template,
                                           context)
                # Force subject to a single line to avoid header-injection
                # issues.
                subject = ''.join(subject.splitlines())
                message = render_to_string(email_body_template,
                                           context)
                user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                context['email'] = form.cleaned_data["email"]
                return render(request, 'registration/resend_activation_email_done.html', context)

    if not form:
        form = ResendActivationEmailForm()

    context.update({"form": form})
    return render(request, 'registration/resend_activation_email_form.html', context)
