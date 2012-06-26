from pymongo import Connection
from pymongo.helpers import bson

conn = Connection()
db = conn['kaggle-wp']


def score_likes_by(uids=['30629226']):
    cur = db.tpt.find({'likes.uid': {'$in': uids}}, {'post_id': 1, 'likes.uid': 1})
    posts = sorted(((len(x['likes']), x['post_id']) for x in cur), reverse=True) # slow and stupid
    return posts
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
    uids = [ like['uid'] for post in posts_liked_by_user for like in post['likes'] ]
    return uids
#print list(get_neighbors_for())

def main():
    """Collaborative filtering algorithm"""
    recommended_posts = {}
    users = db.tu.find({}, {'uid': 1, 'likes.post_id': 1}) #TODO: ENABLE
    for n, user in enumerate(users):
        uids = get_neighbors_for(user)
        posts = score_likes_by(uids)
        recommended_posts[user['uid']] = posts
        if n > 3:
            break
    return recommended_posts
d = main()
print "check variable d"



#get_all_for(db.tu, 'likes.post_id')

#def get_all_for(collection, embedded_field):
    #f1, f2 = embedded_field.split('.', 1)
    #collection.find({f1


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
