from pymongo import Connection
import datetime

conn = Connection()
db = conn['kaggle-wp']

def unwind_likes_from(dct):
    dct.pop('_id')
    likes = dct.pop('likes')
    for like in likes:
        like.update(dct)
        like = cast_vals_to_int(like)
        yield like

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
    yield dct

def data_munge(old_coll, db, new_coll, strategy=unwind_likes_from):
    new_coll.drop()
    cur = old_coll.find()
    #cur.batch_size(5000)
    new_data = []
    for n, elem in enumerate(cur):
        new_data.extend([x for x in strategy(elem)])

        if (n) % 5000 == 0:
            print len(new_data)
            print 'batch inserting'
            try:
                new_coll.insert(new_data)
            except:
                print 'failed batch insert... inserting individually'
                for x in new_data:
                    new_coll.insert(x)
            new_data = []

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
