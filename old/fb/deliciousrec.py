from pydelicious import get_popular, get_userposts, get_urlposts
from recommendations import *
import time

def initializeUserDict(tag,count=5):
    user_dict = {}
    all_items = {}
    # get the top count' popular posts
    for p1 in get_popular(tag=tag)[0:count]:
        # find all users who posted this
        for p2 in get_urlposts(p1['href']):
            user = p2['user']
            user_dict.setdefault(user,{})
            # get user posts
            for i in range(3):
                try:
                    posts = get_userposts(user)
                    break
                except:
                    print "Failed user "+user+", retrying"
                    time.sleep(4)
            for post in posts:
                url = post['href']
                user_dict[user][url] = 1.0
                all_items[url] = 1

    #fill in missing items with 0
    [ratings.setdefault(item,0.0) for item in all_items for ratings in user_dict.values()]
                
    return user_dict