# Imports for relevant libraries
import json
import requests
import urllib
import random
import os
import sys
import tweepy
from PIL import Image

class TwitterBot:
    def __init__(self, json_file):
        """
            Grab all of the keys/tokens and set up the tweepy client
        """
        self.api_key = ''
        self.api_client = None
        self.templates = []

        # Grab the user config from the json file
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
        """
            Push a new status to Twitter with generated text/media
        """
        self.api_client.update_status(status_text, media_ids=media_id)

    def slideIntoDM(self, user="", media_id=""):
        """
            Send a DM to a specified user along with media
        """
        self.getData(user)
        with open('json/user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        self.api_client.send_direct_message(user_dict["id"], "", attachment_type="media", attachment_media_id=media_id)

    def getData(self, user=""):
        """
            Get the data for a specified user (i.e. user ID, name, tweets, pfp, etc.)
        """
        user_data = self.api_client.get_user(screen_name=user)
        with open('json/user.json', 'w') as user_json:
            json.dump(user_data._json, user_json, indent=4)

    def mediaUpload(self, filename):
        """
            Push media to Twitter so it can be used by the bot, media has a time limit on it
        """
        media_upload = self.api_client.media_upload(filename)
        media_id = [media_upload.media_id_string]
        return media_id

    def convertImagePng(self, jpg_file):
        """
            Imgflip deals in jpeg, twitter deals in png and Siths deal in absolutes
        """
        image = Image.open(jpg_file)
        image_name = jpg_file.split(".")
        image_name = image_name[0] + ".png"
        image.save(image_name)
        os.remove(jpg_file)
        return image_name

    def pullMemeTemplates(self):
        """
            Pull the top 100 meme templates from imgflip
        """
        data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
        with open('json/memes.json', 'w') as memes_json:
            json.dump(data, memes_json, indent=4)
        self.templates = [{'name':image['name'],'url':image['url'],'id':image['id'],'box_count':image['box_count']} for image in data]

    def createMeme(self, topText, bottomText):
        """
            Slap some text on a image and you get a meme. That's how it works, right?
        """
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
        if not os.path.isdir("images"):
            os.mkdir("images/")
        filename, headers = opener.retrieve(response['data']['url'], 'images/' + random_meme_id['name'] + '.jpg')
        return 'images/' + random_meme_id['name'] + '.jpg'


def main():
    try:
        apiInstance = TwitterBot("json/config.json")
        apiInstance.pullMemeTemplates()
        meme = apiInstance.createMeme("CS Post Bot 2048", "CS Post Bot 4096")
        converted_meme = apiInstance.convertImagePng(meme)
        media_id = apiInstance.mediaUpload(converted_meme)
        apiInstance.updateBotStatus("Beep Boop, my creator hasn't created any meme text yet ¯\_(ツ)_/¯", media_id)
        os.remove(converted_meme)
    except Exception as err:
        print("Hey, I was lazy creating this thing and didn't add any error handling. ¯\_(ツ)_/¯ \n {0}\n\t{1}".format(err.with_traceback, err))
        sys.exit(-1)

# Program Entry Point
if __name__ == '__main__':
    main()
