from PIL import Image
import requests
from io import BytesIO
import telegram

Unsplash_API_KEY = ''
TelegramBot = ''
Chat_ID = ''

bot = telegram.Bot(token=TelegramBot)

image = f"https://api.unsplash.com/photos/random?client_id={Unsplash_API_KEY}"
response = requests.get(image)
photo = response.json()

download_location = photo['links']['download_location']
payload = {'client_id':Unsplash_API_KEY}
status_code = requests.get(download_location, payload).status_code

if status_code == 200:  
    image_id = photo['id']
    download_endpoint = f"https://api.unsplash.com//photos/{image_id}/download?client_id={Unsplash_API_KEY}"
    image_download_url = requests.get(download_endpoint).json()['url']
    response = requests.get(image_download_url)
    format = Image.open(BytesIO(response.content)).format
    filename = f"image.{format}"
    Image.open(BytesIO(response.content)).save(filename) 

else:
    print('download not allowed', status_code)

PHOTO_PATH = filename

bot.send_photo(chat_id=Chat_ID, photo=open(PHOTO_PATH, 'rb'))
