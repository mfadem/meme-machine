# Imports for relevant libraries
import json
import requests
import urllib
import random
import os
import tweepy
from PIL import Image

class TwitterBot:
    def __init__(self, json_file):
        self.api_key = ''
        self.api_client = None
        self.templates = []

        with open(json_file, 'r') as json_config:
            dict_config = json.load(json_config)
            self.api_key = dict_config["api-key"]
            self.api_secret_key = dict_config["api-secret-key"]
            self.bearer_token = dict_config["bearer-token"]
            self.access_token = dict_config["access-token"]
            self.access_token_secret = dict_config["access-token-secret"]
            self.imgflip_username = dict_config["imgflip-username"]
            self.imgflip_password = dict_config["imgflip-password"]
            self.browser_user_agent = dict_config["browser-user-agent"]

        # Authenticate the api client
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api_client = tweepy.API(auth, wait_on_rate_limit=True)

    def updateBotStatus(self, status_text="", media_id=""):
        with open('user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        self.api_client.update_status(status_text, media_ids=media_id)

    def slideIntoDM(self):
        with open('user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        self.api_client.send_direct_message(user_dict["id"], "", attachment_type="media", attachment_media_id=media_id)

    def getData(self, user=""):
        tweets = self.api_client.home_timeline()
        for tweet in tweets:
            print(tweet.text)
        user_data = self.api_client.get_user(screen_name=user)
        with open('user.json', 'w') as user_json:
            json.dump(user._json, user_json, indent=4)

    def mediaUpload(self, filename):
        media_upload = self.api_client.media_upload(filename)
        media_id = [media_upload.media_id_string]
        return media_id

    def convertImagePng(self, jpg_file):
        image = Image.open(jpg_file)
        image_name = jpg_file.split(".")
        image_name = image_name[0] + ".png"
        image.save(image_name)
        os.remove(jpg_file)
        return image_name

    def pullMemeTemplates(self):
        data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
        with open('memes.json', 'w') as memes_json:
            json.dump(data, memes_json, indent=4)
        self.templates = [{'name':image['name'],'url':image['url'],'id':image['id'],'box_count':image['box_count']} for image in data]

    def createMeme(self, topText, bottomText, image=None):
        random_meme_id = random.choice(self.templates)
        url = 'https://api.imgflip.com/caption_image'
        params = {
        'username':self.imgflip_username,
        'password':self.imgflip_password,
        'template_id':random_meme_id['id'],
        'text0':topText,
        'text1':bottomText
        }
        response = requests.request('POST',url,params=params).json()

        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', self.browser_user_agent)
        filename, headers = opener.retrieve(response['data']['url'], 'images/' + random_meme_id['name'] + '.jpg')
        return 'images/' + random_meme_id['name'] + '.jpg'


def main():
    apiInstance = TwitterBot("source/config.json")
    apiInstance.pullMemeTemplates()
    meme = apiInstance.createMeme("CS Post Bot 2048", "CS Post Bot 4096")
    converted_meme = apiInstance.convertImagePng(meme)
    media_id = apiInstance.mediaUpload(converted_meme)
    apiInstance.updateBotStatus("Beep Boop", media_id)

# Program Entry Point
if __name__ == '__main__':
    main()
