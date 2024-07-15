import json
from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Exports users data'

    def handle(self, *args, **options):
        users = list(User.objects.values())

        formatted_users = []
        for user in users:
            formatted_user = {
                "model": "auth.user",
                "pk": user['id'],
                "fields": {
                    "password": user['password'],
                    "last_login": user['last_login'].isoformat() if 'last_login' in user else None,
                    "is_superuser": user['is_superuser'],
                    "username": user['username'],
                    "first_name": user['first_name'],
                    "last_name": user['last_name'],
                    "email": user['email'],
                    "is_staff": user['is_staff'],
                    "is_active": user['is_active'],
                    "date_joined": user['date_joined'].isoformat() if 'date_joined' in user else None,
                    "groups": user.get('groups', []),
                    "user_permissions": user.get('user_permissions', [])
                }
            }
            formatted_users.append(formatted_user)

        with open('fixtures/users-fixtures.json', 'w') as f:
            json.dump(formatted_users, f)