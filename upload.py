import sys
import requests
from requests_toolbelt import *
URL = sys.argv[1]
file = sys.argv[2]
filename = file.split("/")[-1]
m = MultipartEncoder(
    {'file': (filename, open(file, 'rb'),
                     'application/octet-stream')})

headers = {
    "Content-Type": m.content_type,
    "referer": URL,
}
re = requests.post(URL, data=m, headers=headers)
print(re)
