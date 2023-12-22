from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.core.cache import cache
from django.dispatch import receiver



# @receiver(user_logged_in, sender = User)
# def user_login_success(sender, request, user, **kwargs):
#     ip = request.META.get('REMOTE_ADDR') # return user ip when user logged in
#     # print("IP : ",ip)
#     request.session['ip'] = ip

@receiver(user_logged_in, sender = User)
def user_login_success(sender, request, user, **kwargs):
    login_count = cache.get('count', 0, version=user.pk) + 1 # current login count + 1 and use version for unique
    cache.set('count', login_count, version= user.pk)