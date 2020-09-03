# Imports for relevant libraries
import tweepy
import json
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
            # print(self.api_key)
            # print(self.api_secret_key)
            # print(self.bearer_token)
            # print(self.access_token)
            # print(self.access_token_secret)

        # Authenticate the api client
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api_client = tweepy.API(auth, wait_on_rate_limit=True)

    def getTwitter(self):
        tweets = self.api_client.home_timeline()
        for tweet in tweets:
            print(tweet.text)
        user = self.api_client.get_user(screen_name="Science2048")
        # user = self.api_client.get_user(screen_name="rPrequelMemes")
        with open('user.json', 'w') as user_json:
            json.dump(user._json, user_json, indent=4)

    def postTwitter(self):
        with open('user.json', 'r') as user_json:
            user_dict = json.load(user_json)
        # img = Image.open("images/hello_there.jpg")
        # img.save("images/hello_there.png")
        media_upload = self.api_client.media_upload("images/hello_there.png")
        media_id = [media_upload.media_id_string]
        # self.api_client.send_direct_message(user_dict["id"], "", attachment_type="media", attachment_media_id=media_id)
        self.api_client.update_status("@Science2048", media_ids=media_id)


def main():
    apiInstance = TwitterBot("source/config.json")
    apiInstance.getTwitter()
    apiInstance.postTwitter()

# Program Entry Point
if __name__ == '__main__':
    main()
