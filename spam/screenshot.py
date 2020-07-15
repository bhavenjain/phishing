import requests
import urllib.parse
from PIL import Image

apivoid_key = "22e61728908b1f484874fa0245267890958b76be";

url = "https://www.google.com/";

r = requests.get(url='https://endpoint.apivoid.com/screenshot/v1/pay-as-you-go/?key='+apivoid_key+'&url='+urllib.parse.quote(url)+'&full_page=1')

print(r.json())