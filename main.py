from pymongo import Connection
from pymongo.objectid import ObjectId

conn = Connection()
db = conn['kaggle-wp']

def get_posts_for_users():
    users = [{u'_id': ObjectId('4fe7793a71bb31c62927f17b'),
     u'likes': [{u'post_id': u'918345'},
      {u'post_id': u'1664133'},
      {u'post_id': u'1724823'},
      {u'post_id': u'130559'},
      {u'post_id': u'1855905'}]}]

    #users = db.tu.find({}, {'likes.post_id': 1}) #TODO: ENABLE
    for user in users:
        posts = (p['post_id'] for p in user['likes'])
        for post in posts:
            uids = db.tpt.find({'post_id': post}, {'likes.uid': 1})
            uids = (p['uid'] for p in uids)
            yield (user['uid'], post, uids)






#get_all_for(db.tu, 'likes.post_id')

#def get_all_for(collection, embedded_field):
    #f1, f2 = embedded_field.split('.', 1)
    #collection.find({f1








