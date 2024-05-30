from django.core.management import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

#from shop_megano.megano.userprofile.models import UserProfile
from userprofile.models import UserProfile

class Command(BaseCommand):
    """
    Команда для создания профиля всем пользователям,
    имеющие статус superuser.
    """
    def handle(self, *args, **options):
        self.stdout.write('Create profile to superuser')
        give_all_superusers = User.objects.filter(is_superuser=True)
        # print(give_all_superusers)
        # first_superuser = User.objects.filter(is_superuser=True).first()
        # print(first_superuser)
        #
        # print(give_all_superusers)
        # for name in give_all_superusers:
        #     print(name.id)

        image_file_path = '/Users/skillbox/PycharmProjects/MeganoShop_django/images/admin.jpeg'

        for admin in give_all_superusers:
            with open(image_file_path, 'rb') as img:
                profile, created = UserProfile.objects.get_or_create(
                    fullName='Admin',
                    email='',
                    phone='',
                    user_id=admin.id,
                    avatar=ContentFile(img.read(), name='admin.jpeg')
                )
        self.stdout.write(self.style.SUCCESS('Profile created!'))
