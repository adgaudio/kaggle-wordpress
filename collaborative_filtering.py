from pymongo import Connection
from pymongo.helpers import bson

from collections import Counter

conn = Connection()
db = conn['kaggle-wp']


#def score_likes_by(uids=['30629226']):
    #"""Given neighbors, find posts they liked and score posts by most popular"""
    #cur = db.tpt.find({'likes.uid': {'$in': uids}}, {'post_id': 1, 'likes.uid': 1})
    #cur.batch_size(5000)

    #uids = set(uids)
    ## slow and stupid scoring
    #posts = ((len([uids.intersection(y['uid']) for y in x['likes']]), x['post_id']) for x in cur)
    #posts = sorted(posts, reverse=True) 
    #return posts

def score_likes_by(uids=['30629226']):
    """Given neighbors, find posts they liked and score posts by most frequently occurring"""
    cur = db.tu.find({'uid': {'$in': uids}}, {'likes.post_id': 1})
    post_ids = (like['post_id'] for user in cur for like in user['likes'])
    histogram = Counter(post_ids)
    return histogram

#print score_likes_by()

def get_neighbors_for(user = {
         u'_id': bson.ObjectId('4fe7793a71bb31c62927f17b'),
         u'likes': [{u'post_id': u'918345'},
                      {u'post_id': u'1664133'},
                      {u'post_id': u'1724823'},
                      {u'post_id': u'130559'},
                      {u'post_id': u'1855905'}],
         u'uid': u'30629226'}):

    post_ids = [ p['post_id'] for p in user['likes'] ]
    posts_liked_by_user = db.tpt.find({'post_id': {'$in': post_ids}}, {'likes.uid': 1})
    posts_liked_by_user.batch_size(5000)
    uids = [ like['uid'] for post in posts_liked_by_user for like in post['likes'] ]
    return uids
#print list(get_neighbors_for())

def main(use_test=True):
    """Collaborative filtering algorithm"""
    recommended_posts = {}
    users = db.tu.find({'inTestSet': use_test or {'$in': [True, False]}}, {'uid': 1, 'likes.post_id': 1})
    for n, user in enumerate(users):
        uids = get_neighbors_for(user)
        print uids
        posts = score_likes_by(uids)
        print len(posts)
        recommended_posts[user['uid']] = posts
        if n > 40:
            break
    return recommended_posts
d = main()
print "check variable d"



#visually check data in main()
        #print data
        #dist= sorted(data.values(), reverse=True)
        ##dist= sorted(Counter(data.values()).items(), reverse=True)[:50]
        #print
        #print dist
        #import pylab
        ##pylab.plot([x[0] for x in dist], [x[1] for x in dist], 'r.')
        #pylab.plot(range(len(dist)), dist, 'b.')

        #break
