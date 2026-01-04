import urllib.request,sys
url='http://127.0.0.1:8000/static/css/style.css'
try:
    r=urllib.request.urlopen(url,timeout=5)
    print('STATUS',r.getcode())
    print('CONTENT-TYPE',r.info().get('Content-Type'))
    data=r.read(800).decode('utf-8',errors='replace')
    print('\n--- START OF FILE ---\n')
    print(data[:800])
    print('\n--- END ---')
except Exception as e:
    print('ERROR',e)
    sys.exit(1)
