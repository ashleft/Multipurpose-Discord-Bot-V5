import json, sys, os
import discord
from discord.ext import commands
from core import Context


def getIgnore(guildID):
    with open("ignore.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "channel": [],
            "role": None,
            "user": [],
            "bypassrole": None,
            "bypassuser": [],
            "commands": []
            
            
        }
        updateignore(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]



def updateignore(guildID, data):
    with open("ignore.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("ignore.json", "w") as config:
        config.write(newdata)
################

def getExtra(guildID):
    with open("extra.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "owners": [],
            "antiSpam": False,
            "antiLink": False,
            "antiinvites": False,
            "punishment": "mute",
            "whitelisted": [],
            "channel": None,
            "mods": [],
            "modrole": None,
            "ignorechannels": []
            
        }
        updateExtra(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateExtra(guildID, data):
    with open("extra.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("extra.json", "w") as config:
        config.write(newdata)






###########autorole###########
def updateautorole(guildID, data):
    with open("autorole.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("autorole.json", "w") as config:
        config.write(newdata)


def getautorole(guildID):
    with open("autorole.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "bots": [],
            "humans": []
        }
        updateautorole(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]
#######################vcrole ############   


def updatevcrole(guildID, data):
    with open("vcrole.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("vcrole.json", "w") as config:
        config.write(newdata)


def getvcrole(guildID):
    with open("vcrole.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "bots": "",
            "humans": ""
        }
        updatevcrole(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]  
    
#######################welcome############


def updategreet(guildID, data):
    with open("greet.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("greet.json", "w") as config:
        config.write(newdata)


def getgreet(guildID):
    with open("greet.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
                "autodel": None,
                "channel": [],
                "color": None,
                "embed": False,
                "footer": "",
                "image": "",
                "message": "<<user.mention>> Welcome To <<server.name>>",
                "ping": False,
                "title": "",
                "thumbnail": ""
        }
        updategreet(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]  




#######################config############


   
def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "antiSpam": False,
            "antiLink": False,
            "antiMentions": False,
            "whitelisted": [],
            "admins": [],
            "adminrole": None,
            "punishment": "none",
            "prefix": ".",
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "wlrole": None,
            "reqrole": None,
            "captcha": False, 
            "captchaChannel": False, 
            "logChannel": 1, 
            "temporaryRole": 1, 
            "roleGivenAfterCaptcha": False
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)



def add_user_to_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        if str(user_id) in file_data["ids"]:
            return

        file_data["ids"].append(str(user_id))
    with open("blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int) -> None:
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(str(user_id))
    with open("blacklist.json", "w") as file:
        json.dump(file_data, file, indent=4)




def blacklist_check():

    def predicate(ctx):
        with open("blacklist.json") as f:
            data = json.load(f)
            if str(ctx.author.id) in data["ids"]:
                return False
            return True

    return commands.check(predicate)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)





def getanti(guildid):
    with open("anti.json", "r") as config:
        data = json.load(config)
    if str(guildid) not in data["guilds"]:
        default = "off"
        updateanti(guildid, default)
        return default
    return data["guilds"][str(guildid)]


def updateanti(guildid, data):
    with open("anti.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildid)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("anti.json", "w") as config:
        config.write(newdata)



def ignore_check():

    def predicate(ctx):
            data = getIgnore(ctx.guild.id)
            ch = data["channel"]
            iuser = data["user"]
            irole = data["role"]
            buser = data["bypassuser"]
            brole = data["bypassrole"]
            if str(ctx.author.id) in buser:
                return True            
            elif str(ctx.author.id) in iuser or str(ctx.channel.id) in ch:
                return False
            else:
                return True
            

    return commands.check(predicate)



def updateHacker(guildID, data):
    with open("events.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("events.json", "w") as config:
        config.write(newdata)


def getHacker(guildID):
    with open("events.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "antinuke": {
                "antirole-delete": True,
                "antirole-create": True,
                "antirole-update": True,
                "antichannel-create": True,
                "antichannel-delete": True,
                "antichannel-update": True,
                "antiban": True,
                "antikick": True,
                "antiwebhook": True,
                "antibot": True,
                "antiserver": True,
                "antiping": True,
                "antiprune": True,
                "antiemoji-delete": True,
                "antiemoji-create": True,
                "antiemoji-update": True,
                "antimemberrole-update": True
            }
        }
        updateHacker(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]



def getLogging(guildID):
    with open("logging.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "mod": None,
            "role": None,
            "message": None,
            "member": None,
            "channel": None,
            "server": None,
            "voice": None
        }
        updateLogging(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateLogging(guildID, data):
    with open("logging.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("logging.json", "w") as config:
        config.write(newdata)

