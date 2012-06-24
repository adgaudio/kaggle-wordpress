import urllib2, json, copy
from urllib import urlencode
from recommendations import *
import sys, os
import webbrowser

ACCESS_TOKEN = None
#replace above line with something like:
#ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

APP_ID = '343180059059629'

def get(url):
    global ACCESS_TOKEN
    data = ''
    try:
        data = json.loads(urllib2.urlopen('%s?access_token=%s' % (url,ACCESS_TOKEN)).read())
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
    return data

def get_likes(userid):
    return get('https://graph.facebook.com/%d/likes' % int(userid))['data']

def get_friends(userid):
    return get('https://graph.facebook.com/%d/friends' % int(userid))['data']

    
users = {}
me = None

def run():    
    global users, me
    me = get('https://graph.facebook.com/me')
    if raw_input("Is this you: %s? [yes,no]:  " % str(me['name'])) == 'yes':
        print 'Fetching you first, then your friends and their likes.'
        friends = get_friends(me['id'])
        print 'You have %d friends.' % len(friends)
        users_temp = copy.copy(friends)
        users_temp.insert(0,me)

        # want a dictionary of names with value of dictionary of likes
        i = 0
        all_likes = {}
        for user in users_temp:
            i += 1
            print '%d.) %s' % (i,user['name'])
            users[user['name']] = {}#initialize empty likes
            likes = get_likes(user['id'])
            for like in likes:
                users[user['name']][like['name']] = 1.0#user liked it
                all_likes.setdefault(like['name'],1)#add to dictionary      

        # Go through each user and fill in missing 'likes'
        for user_likes in users.values():
            for like in all_likes:
                if like not in user_likes:
                    user_likes[like] = 0.0
        print 'Completely done making the lists. Run your compatibility code!'
    else:
        print 'Please update the access token so that it reflects you.'
        os._exit(0)


if ACCESS_TOKEN is None:
    webbrowser.open('https://www.facebook.com/dialog/oauth?'+
                urlencode({'client_id':APP_ID,
                            'redirect_uri':'http://kratsg.caltech.edu/public_html/fb/?getAccessToken'}))

    print 'Need Access Token! We opened the browser so you can copy/paste access token into the python file'
    os._exit(0)
else:
    print 'Everything appears to be running ok.'
    run()


