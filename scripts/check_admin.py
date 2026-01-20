import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'University_Platform.settings')
# Ensure path includes project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import django
django.setup()
from Accounts.models import User
u = User.objects.filter(email='hindkahla413@gmail.com').first()
if u:
    print('Found:', u.email, 'is_staff=', u.is_staff, 'is_superuser=', u.is_superuser, 'role=', u.role)
else:
    print('Admin user not found')
