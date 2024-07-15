import json
import os

with open("info.json", "r") as f:
    DATA = json.load(f)

OWNER_IDS = DATA["OWNER_IDS"]
EXTENSIONS = DATA["EXTENSIONS"]
No_Prefix = DATA["np"]
TOKEN = DATA["TOKEN"]
BotName = DATA["BotName"]
serverLink = DATA["serverLink"]
whCL = DATA["wh_cl"]
whBL = DATA["wh_bl"]
statusText = DATA["statusText"]
