from django.contrib.auth import get_user_model

User = get_user_model()


def get_seller_users():
    return User.objects.filter(is_seller=True)
