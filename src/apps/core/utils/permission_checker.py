from django.contrib.auth.models import User


def get_user_group(user: User):
    return user.groups.values_list('name', flat=True).first()
