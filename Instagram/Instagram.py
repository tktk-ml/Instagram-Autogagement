from utils.log import Log
import random
import requests
import json
import re
from datetime import datetime


class Instagram:
    def searchHashtag(label):
        proxy = {
        	'http': '',
        	'https': ''
        }
        #Create User Agent
        USER_AGENTS_FILE = 'Instagram/user-agents.txt'
        user_agent = []
        with open(USER_AGENTS_FILE) as f:
            for u in f.readline():
                u = u.strip()
                if '#' in u:
                    continue
                user_agent.append(u)
        user_agent_single = random.choice(user_agent)

        #Scrape
        ig_url_hashtags = "https://www.instagram.com/explore/tags/" + label + "/?__a=1"
        response = requests.get(ig_url_hashtags, proxies=proxy, headers = {'User-Agent': user_agent_single}, allow_redirects = False).json()

        count = response['graphql']['hashtag']['edge_hashtag_to_media']['count']
        posts = response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']
        countPosts = len(posts)
        popularPosts = []
        i = countPosts - 9

        maxLikes = 0
        makLikesPost = ''

        for i in range(countPosts):
            popularPosts.append(posts[i])
        for post in popularPosts:
            likeCount = post["node"]["edge_liked_by"]["count"]
            if(likeCount > maxLikes):
                maxLikes = likeCount
                maxLikesPost = post

        displayUrl = post["node"]["display_url"]
        shortcode = post["node"]["shortcode"]
        timestamp = post["node"]["taken_at_timestamp"]
        date_object = datetime.fromtimestamp(timestamp)

        #Hashtags
        popularHashtags = []
        caption = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
        hashtags_in_caption = re.findall("#(\w+)", caption)
        for ht in hashtags_in_caption:
            popularHashtags.append('#' + ht)

        #Get Username From Pic
        responseUser = requests.get("https://www.instagram.com/p/" + shortcode + "/?__a=1", proxies=proxy, headers = {'User-Agent': user_agent_single}, allow_redirects = False).json()
        ownerUsername = responseUser["graphql"]["shortcode_media"]["owner"]["username"]

        #Download Image
        img_data = requests.get(displayUrl).content

        with open('pics/' + ownerUsername + '.jpg', 'wb') as handler:
            handler.write(img_data)

        customResponse = {}

        customResponse["owner"] = ownerUsername
        customResponse["likes"] = maxLikes
        customResponse["date"] = date_object
        customResponse["path"] = 'pics/' + ownerUsername + '.jpg'
        customResponse["target"] = label
        customResponse["hashtags"] = popularHashtags

        return customResponse
