import os
import sys
import django

# Ensure project root is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'University_Platform.settings')
django.setup()

from Accounts.models import User

EMAIL = 'hindkahla413@gmail.com'
PASSWORD = 'Hind@1977'

user, created = User.objects.get_or_create(email=EMAIL)
if created:
    user.set_password(PASSWORD)
    user.role = User.ADMIN
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print('Admin user created:', EMAIL)
else:
    # Update password and admin flags if user exists
    user.set_password(PASSWORD)
    user.role = User.ADMIN
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print('Admin user updated:', EMAIL)
