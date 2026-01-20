import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','University_Platform.settings')
django.setup()
from django.urls import get_resolver
r = get_resolver()
for p in r.url_patterns:
    try:
        print('PATTERN:', p.pattern, '->', type(p))
    except Exception as e:
        print('ERR', e)

inc = None
for p in r.url_patterns:
    if hasattr(p, 'url_patterns'):
        inc = p
        break
if inc:
    print('\nIncluded patterns:')
    for x in inc.url_patterns:
        print('-', x.pattern)
else:
    print('No included patterns found')
