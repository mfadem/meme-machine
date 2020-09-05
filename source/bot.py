# Imports for relevant libraries
import json
import requests
import urllib
import tweepy
from PIL import Image

class TwitterBot:
    def __init__(self, json_file):
        self.api_key = ''
        self.api_client = None

        with open(json_file, 'r') as json_config:
            dict_config = json.load(json_config)
            self.api_key = dict_config["api-key"]
            self.api_secret_key = dict_config["api-secret-key"]
            self.bearer_token = dict_config["bearer-token"]
            self.access_token = dict_config["access-token"]
            self.access_token_secret = dict_config["access-token-secret"]
            self.imageflip_username = dict_config["imageflip-username"]
            self.imageflip_password = dict_config["imageflip-password"]
            self.templates = []
            # print(self.api_key)
            # print(self.api_secret_key)
            # print(self.bearer_token)
            # print(self.access_token)
            # print(self.access_token_secret)
            # print(self.imageflip_username)
            # print(self.imageflip_password)

        # Authenticate the api client
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api_client = tweepy.API(auth, wait_on_rate_limit=True)

    def updateBotStatus(self, status_text=""):
        with open('user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        media_id = mediaUpload("images/hello_there.png")
        self.api_client.update_status("@Science2048", media_ids=media_id)

    def slideIntoDM(self):
        with open('user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        media_id = mediaUpload("images/hello_there.png")
        self.api_client.send_direct_message(user_dict["id"], "", attachment_type="media", attachment_media_id=media_id)

    def getData(self, user=""):
        tweets = self.api_client.home_timeline()
        for tweet in tweets:
            print(tweet.text)
        user_data = self.api_client.get_user(screen_name=user)
        with open('user.json', 'w') as user_json:
            json.dump(user._json, user_json, indent=4)

    def mediaUpload(self, filename):
        media_upload = self.api_client.media_upload("images/hello_there.png")
        media_id = [media_upload.media_id_string]
        return media_id

    def convertImagePng(self, jpg_file):
        image = Image.open(jpg_file)
        image_name = jpg_file.split(".")
        image_name = image_name[0] + ".png"
        image.save(image_name)

    def pullMemeTemplates(self):
        data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
        self.templates = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

        print('Here is the list of available memes : \n')
        ctr = 1
        for meme in self.templates:
            print(ctr, meme['name'])
            ctr = ctr+1

    def createMeme(self, topText, bottomText, image=""):
        return True


def main():
    apiInstance = TwitterBot("source/config.json")
    apiInstance.pullMemeTemplates()
    # apiInstance.getTwitter()

# Program Entry Point
if __name__ == '__main__':
    main()
