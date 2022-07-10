from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.conf import settings
from django.utils import  timezone

import os
from djoser import utils
from celery import shared_task
from datetime import timedelta
from dotenv import load_dotenv

from .models import User

load_dotenv()

@shared_task
def upload_image_to_cloud(image):
    """Profile images are uploaded to cloud"""
    pass

def get_users(days):
    """Utility function to get users based on the number of days for the next two tasks"""

    users= []

    for user in User.objects.all():
        if (not user.is_active) & (timezone.now() - user.date_joined > timedelta(days= days)):
            users.append(user)

    return users

def get_activate_email_url(user):
    """Generates personalized activate account uri for users"""

    ids= {}
    ids["uid"] = utils.encode_uid(user.pk)
    ids["token"] = default_token_generator.make_token(user)
    HOST = os.environ.get("HOST", default="http://localhost:8000/")
    uri= HOST + settings.DJOSER.get("ACTIVATION_URL")

    return uri.format(**ids)

@shared_task
def send_account_delete_warning_mail():
    """Users who are yet to activate their accounts after three days of creation will be sent
     warning of account deletion after three days"""
    
    users= get_users(3)
    mails= [user.email for user in users]
    names= [user.full_name for user in users]
    activation_uris= [get_activate_email_url(user) for user in users]

    for idx, _ in enumerate(users):
        context= {"name": names[idx], "activation_uri": activation_uris[idx]}

        try:
            msg= BaseEmailMessage(template_name= 'account/send_reminder_mail.html', context= context)
            msg.send(to= [mails[idx]])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')



@shared_task
def delete_unactivated_accounts():
    """Delete accounts that have not been activated  after six days of creation"""
    users_emails= [user.email for user in get_users(6)]
    User.objects.filter(email__in=users_emails).delete()
    print(f"Deleted users: {users_emails}")