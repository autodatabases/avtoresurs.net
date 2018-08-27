import logging
from django.contrib.auth.models import User

from service.parser.point import get_primary_account_profile_or_none
from user_profile.models import UserProfile


bonus_users_accounts = User.objects.filter(username__startswith='cl')

for bonus_acc_user in bonus_users_accounts:
    # bonus account
    bonus_acc_prof = UserProfile.objects.get(user=bonus_acc_user)
    logging.warning('Bonus account={bonus_acc_name}'.format(
        bonus_acc_name=bonus_acc_user.username
    ))

    # primary account
    primary_acc_prof = get_primary_account_profile_or_none(bonus_account=bonus_acc_prof)
    if primary_acc_prof:
        logging.warning('+')
        # primary_acc_prof.bonus_code = bonus_acc_user.username
        # primary_acc_prof.save()
