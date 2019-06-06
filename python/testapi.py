import requests
# data to be sent to api


data = { 'sketch': "BASE64 PNG/JPG/JPEG", 'hint': "BASE64 PNG With Transparence", 'opacity': 0.0 }

# sending post request and saving response as response object
r = requests.post(url='https://dvic.devinci.fr/dgx/paints_torch/api/v1/colorizer', data=data)
print(r)