from django.core.management import BaseCommand

#from shop_megano.megano.userprofile.models import UserProfile
from userprofile.models import UserProfile
from django.core.files.storage import FileSystemStorage
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Create profile to superuser')
        fs = FileSystemStorage(location='/Users/skillboxstudy/PycharmProjects/MeganoShop_django/images/')
        file = fs.open('admin.png', 'rb')
        profile, created = UserProfile.objects.get_or_create(
            fullName='Admin',
            email='',
            phone='',
            user_id=1,
            avatar=file.name
        )
        file.close()
        self.stdout.write(self.style.SUCCESS('Profile created!'))
