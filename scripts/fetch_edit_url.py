import urllib.request, re
url='http://127.0.0.1:8000/librarian/books/'
try:
    r=urllib.request.urlopen(url, timeout=5)
    html=r.read().decode('utf-8',errors='replace')
    m=re.search(r'data-edit-url="([^"]+)"', html)
    if m:
        print('EDIT_URL', m.group(1))
    else:
        print('NO_EDIT_URL_FOUND')
    start=html.find('<table')
    if start!=-1:
        print(html[start:start+800])
except Exception as e:
    print('ERROR', e)
