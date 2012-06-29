import monary
from numpy import matrix
from pandas import DataFrame

conn = monary.Monary()

dbname = 'kaggle-wp'

columns = ['blog', 'inTestSet', 'post_id', 'uid', 'like_dt']
arrs = conn.query(dbname, 'tu2', {}, columns, ['int32']*4+['date'])
df = matrix(arrs).transpose()
df = DataFrame(df, columns = columns)


