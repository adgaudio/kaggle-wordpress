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
      {u'post_id': u'1855905'}],
     u'uid': u'30629226'}]

    #users = db.tu.find({}, {'uid': 1, 'likes.post_id': 1}) #TODO: ENABLE
    for user in users:
        post_ids = (p['post_id'] for p in user['likes'])

        for post_id in post_ids:
            posts_cursor = db.tpt.find({'post_id': post_id}, {'likes.uid': 1})
            uids = (p['uid'] for p in posts_cursor.next()['likes'])
            yield (user['uid'], post_id, uids)






#get_all_for(db.tu, 'likes.post_id')

#def get_all_for(collection, embedded_field):
    #f1, f2 = embedded_field.split('.', 1)
    #collection.find({f1








