import monary
from numpy import matrix
from pandas import DataFrame
from pymongo import Connection

DBNAME = 'kaggle-wp'

def get_monary(conn=None, dbname=DBNAME, _cache={}):
    if dbname not in _cache:
        _cache[dbname] = conn or monary.Monary()
    return [_cache[dbname], dbname]

def get_pymongo(dbname=DBNAME, _cache={}, *args, **kwargs):
    if dbname not in _cache:
        _cache[dbname] = Connection()[dbname]
    return _cache[dbname]

def get_tu():
    conn, dbname = get_monary()
    columns = ['blog', 'inTestSet', 'post_id', 'uid', 'like_dt']
    arrs = conn.query(dbname, 'tu2', {}, columns, ['int32']*4+['date'])
    df = matrix(arrs).transpose()
    return DataFrame(df, columns = columns)

def get_tp(conn=None):
    conn, dbname = get_monary()
    print "not implemented, but here's the tp collection using pymongo driver"
    return get_pymongo.tp
    #columns = []
    #arrs = conn.query(dbname, '


