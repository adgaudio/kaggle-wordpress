from pymongo import Connection
import datetime

conn = Connection()
db = conn['kaggle-wp']

def unwind_likes_from(dct):
    dct.pop('_id')
    likes = dct.pop('likes')
    for like in likes:
        like.update(dct)
        like = cast_vals_to_int(like)[0]
    return likes

def cast_vals_to_int(dct):
    for k in dct:
        if k not in ['content', '_id', 'language', 'title', 
                'url', 'tags', 'blogname', 'categories', 'likes']:
            try:
                dct[k] = int(dct[k])
            except:
                try:
                    dct[k] = datetime.datetime.strptime(dct[k], '%Y-%m-%d %H:%M:%S')
                except:
                    pass
    return [ dct ]

def insert(collection, data):
    try:
        collection.insert(data)
    except:
        print 'failed batch insert... inserting individually'
        for x in data:
            collection.insert(x)
    return len(data)

def data_munge(old_coll, db, new_coll, strategy=unwind_likes_from):
    new_coll.drop()
    cur = old_coll.find()
    #cur.batch_size(5000)
    new_data = []
    total = 0
    for n, elem in enumerate(cur):
        new_data.extend(strategy(elem))

        if (n) % 5000 == 0 and n != 0:
            cnt = insert(new_coll, new_data)
            total += cnt
            print 'batch inserting'
            print cnt
            new_data = []
    cnt = insert(new_coll, new_data)
    total += cnt
    print 'batch inserting'
    print cnt
    print '\n---\ntotal inserted:'
    print total

def create_tu2(db):
    data_munge(db.tu, db, db.tu2)

def create_tpt2(db):
    data_munge(db.tpt, db, db.tpt2)

def create_tp2(db):
    data_munge(db.tp, db, db.tp2, strategy=cast_vals_to_int)

if __name__ == '__main__':
    print 'creating collection tu2'
    print create_tu2(db)
    print
    print 'creating collection tpt2'
    print create_tp2(db)
