from pymongo import Connection
import datetime

conn = Connection()
db = conn['kaggle-wp']


def _unwind_likes_from_collection(old_coll, db, new_coll):
    new_coll.drop()
    cur = old_coll.find()
    #cur.batch_size(5000)
    new_data = []
    for n, elem in enumerate(cur):
        elem.pop('_id')
        likes = elem.pop('likes')
        for m, like in enumerate(likes):
            like.update(elem)
            like = cast_vals_to_int(like)
            new_data.append(like)
        if (n+m) % 5000 == 0:
            print 'batch inserting'
            new_coll.insert(new_data)
            new_data = []

def create_tu2(db):
    _unwind_likes_from_collection(db.tu, db, db.tu2)

def create_tpt2(db):
    _unwind_likes_from_collection(db.tpt, db, db.tpt2)

def cast_vals_to_int(dct):
    for k in dct:
        try:
            dct[k] = int(dct[k])
        except:
            try:
                dct[k] = datetime.datetime.strptime(dct[k], '%Y-%m-%d %H:%M:%S')
            except:
                pass
    #print dct
    return dct

print 'creating collection tu2'
print create_tu2(db)
print
print 'creating collection tpt2'
print create_tpt2(db)
