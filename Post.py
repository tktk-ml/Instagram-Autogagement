from utils.log import Log
from utils.screen import Screen
import random
import sys
import configparser
import os
import time
import instabot
from Instagram.Instagram import Instagram

useProxy = True

proxy_url = ''

if(useProxy):
    config = configparser.ConfigParser()
    config.read('config/proxy_settings.ini')
    proxy_url = config['Proxy']['url']

username = ''
password = ''
popularPost = ''

def welcome():
    Screen.clear()
    Screen.welcomeAscii()
    start = ["Oops, I think I dropped something", "Arrg, this fricking USB never inserts at 1st try", "Sssh, do you hear that? We have baited them", "Wut u doing bru? Do ur red team stuff and stop reading this!", "While you read this you are being hacked. Haha!", "All shells belongs to me!"]
    print("\n")
    Log.data("Coded by Matteo Nista <dev@matteonista.it>")
    Log.data("Github: @Mattewn99")
    Log.data("Instagram: @mattewn99")
    Log.data("Telegram: @ThailandiaBoy")
    Log.data("www.matteonista.it")
    print("\n")
    Log.phrases(random.choice(start))
    print("=" * 50)
    print("\n")

def createProfile(configProfileFolder):
    Screen.clear()
    Screen.welcomeAscii()
    print("\n")
    Log.warning("Create a new Profile")
    Log.error("Type 'GO BACK' to go back")
    print("\n")
    user = input("Username: ")
    if(user == 'GO BACK'):
        start()
    passw = input("Password: ")

    config = configparser.ConfigParser()

    config['Instagram'] = {}
    config['Instagram']['username'] = user
    config['Instagram']['password'] = passw

    with open(configProfileFolder + user + '_settings.ini', 'a') as configfile:
        config.write(configfile)
    start()

def deleteProfile(configProfileFolder):
    Screen.clear()
    Screen.welcomeAscii()
    print("\n")
    Log.warning("Delete Profile")
    print("\n")
    profiles = []
    i = 1
    for f in os.listdir(configProfileFolder):
         profiles.append(f)
         Log.info(str(i) + ". " + f.replace("_settings.ini", ""))
         i += 1
    Log.error(str(i) + ". Go Back")
    choice = int(input("\n=> "))
    if(choice == i):
        start()
    else:
        print("\n")
        Log.error(profiles[choice - 1])
        os.remove(configProfileFolder + profiles[choice - 1])
        try:
            os.remove('config/' + profiles[choice - 1].replace("_settings.ini", "") + '_uuid_and_cookie.json')
            os.remove('config/' + profiles[choice - 1].replace("_settings.ini", "") + '.checkpoint')
        except:
            pass
        time.sleep(1)
        start()

def multiProfile():
    global username, password
    configProfileFolder = "./config/profiles/"
    filesCount = sum([len(files) for r, d, files in os.walk(configProfileFolder)])
    if(filesCount == 0):
        Log.warning("0 Profiles Found...")
        Log.success("1. Create Profile")
        Log.error("2. Exit")
        choice = int(input("\n=> "))
        if(choice == 1):
            createProfile(configProfileFolder)
        else:
            close()
    else:
        print("\n")
        Log.warning("Select your account")
        print("\n")
        Log.success("1. Create Profile")
        profiles = []
        i = 2
        for f in os.listdir(configProfileFolder):
             profiles.append(f)
             Log.info(str(i) + ". " + f.replace("_settings.ini", ""))
             i += 1
        Log.error(str(i) + ". Delete Profile")
        Log.error(str(i + 1) + ". Exit")
        choice = int(input("\n=> "))
        if(choice == 1):
            createProfile(configProfileFolder)
        elif(choice == i):
            deleteProfile(configProfileFolder)
        elif(choice == i + 1):
            close()
        else:
            config = configparser.ConfigParser()
            user = profiles[choice - 2]
            config.read(configProfileFolder + user)
            username = config['Instagram']['username']
            password = config['Instagram']['password']
            Log.success(username)
            print("\n")

def close():
    Log.phrases("\nGoodbye...")
    sys.exit(0)

bot = instabot.Bot()

def login():
    passwordToPrint = ""

    for i in range(len(password)):
        passwordToPrint += "*"
    print("=" * 50)
    print("\n")
    Log.warning("Logging in...")
    print("\n")
    Log.info("Username: " + username)
    Log.info("Password: " + passwordToPrint)
    print("\n")
    if(useProxy):
        try:
            bot.login(username = username, password = password, proxy = proxy_url)
        except AssertionError:
            os.remove('config/' + username + '_uuid_and_cookie.json')
            bot.login(username = username, password = password, proxy = proxy_url)
    else:
        try:
            bot.login(username = username, password = password)
        except AssertionError:
            os.remove('config/' + username + '_uuid_and_cookie.json')
            bot.login(username = username, password = password)        
    Log.success("Logged In as " + username)
    print("\n")

def scrapeHashtag():
    global popularPost
    print("=" * 50)
    print("\n")
    labelBuffer = input("Hashtag: ")
    label = labelBuffer.replace("#", "")
    Screen.clear()
    Log.success("Analyzing #" + label)
    popularPost = Instagram.searchHashtag(label)
    print("\n")
    Log.info("Owner: @" + popularPost["owner"])
    Log.info("Likes: " + str(popularPost["likes"]))
    print("\n")
    print("=" * 50)

def post():
    caption = '''
Tag your friends
• ➖➖➖➖➖➖➖➖➖➖
🎈Double Tap ❤
🎈Share and TAG your buddies who love to travel
➖➖➖➖➖➖➖➖➖➖
🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
‼ Follow @{myAccount}
‼ Follow @{myAccount}
‼ Follow @{myAccount}
🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
Credit : @{pictureOwner}
.
.
{hashtags}
'''.format(myAccount = username, pictureOwner = popularPost["owner"], hashtags = ' '.join(popularPost["hashtags"]))
    print("\n")
    Log.info("Posting " + popularPost["path"])
    print("\n")
    bot.upload_photo(popularPost["path"], caption = caption)
    Log.success("Posted!")
    os.remove(popularPost["path"] + '.REMOVE_ME')


def start():
    welcome()
    multiProfile()

def main():
    start()
    login()
    scrapeHashtag()
    post()
    close()

if __name__ == '__main__':
    main()
