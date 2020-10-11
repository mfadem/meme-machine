# Meme Machine
This code is for my twitter bot: [CS Post Bot 4096](https://twitter.com/MemeMachine4096)

Competition to [CS Post Bot 2048](https://github.com/cgilbert250/CSPostBot2048)

## Installation & Execution
* Clone this repo
* Pip install the `requirements.txt` file: `pip3 install -r requirements.txt`
    * I reccommend using a virtual environment to keep everything kosher on your system
* Create a `config.json` file in the `json` directory following the directions below
* Run the code from the root of the project with `python3 source/bot.py`

## Development
* This bot was developed on WSL Ubuntu `18.04` utilizing Python `3.6.9`

## Libraries
This Bot utilizes the following libraries:
* Tweepy: Easily interface with Twitter API
* Pillow: Modify/Create Images
* Requests: Send http/https requests to Imgflip API

## Config File
Your `json/config.json` file should look like this:

    {
        "api-key": "Your Twitter Key Here!",
        "api-secret-key": "Your Twitter Key Here!",
        "bearer-token": "Your Twitter Token Here!",
        "access-token": "Your Twitter Token Here!",
        "access-token-secret": "Your Twitter Token Here!",
        "imgflip-username": "Your Imgflip Username Here!",
        "imgflip-password": "Your Imgflip Password Here!",
        "browser-user-agent": "Your Browser User Agent Here!"
    }

## Input
This bot is using the /r/ProgrammerHumor AI text found on pastebin [here](https://pastebin.com/u/minimaxir)