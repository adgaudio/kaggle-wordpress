from pylab import plot, subplot, draw
#ion()

from monary import Monary
from numpy import matrix
from pandas import DataFrame
from pymongo import Connection

from BeautifulSoup import BeautifulSoup
import nltk


#####
# Database
#####

DBNAME = 'kaggle-wp'

def get_monary(conn=None, dbname=DBNAME, _cache={}):
    if dbname not in _cache:
        _cache[dbname] = conn or Monary()
    return [_cache[dbname], dbname]

def get_pymongo(dbname=DBNAME, _cache={}, *args, **kwargs):
    if dbname not in _cache:
        _cache[dbname] = Connection(*args, **kwargs)[dbname]
    return _cache[dbname]

def get_tu():
    conn, dbname = get_monary()
    columns = ['blog', 'inTestSet', 'post_id', 'uid', 'like_dt']
    arrs = conn.query(dbname, 'tu2', {}, columns, ['int32']*4+['date'])
    df = matrix(arrs).transpose()
    return DataFrame(df, columns = columns)

def get_tp(conn=None):
    conn, dbname = get_monary()
    print "not implemented, bumt here's the tp collection using pymongo driver"
    return get_pymongo.tp
    #columns = []
    #arrs = conn.query(dbname, '

#####
# Plotting
#####
def subplots(grid=[2,2], clear_subplot=True):
    """ Iteratively draw pylab subplots in a grid
    Ex:

    >>> import pylab ; pylab.ion()
    >>> p = subplots(grid=[1,2])
    >>> for x in range(5):
            p.send([range(10), range(10), 'r-'])
            p.send([[1,2,3], [1,3,2], 'b^'])
            subplt = p.send([range(10), range(10), 'b^'])
            subplt.set_title('hello') ; pylab.draw()
    """
    # initialized coroutine by wrapping in closure
    def _subplots():
        n = -1
        ax = None
        while True:
            n = (n+1) % (grid[0] * grid[1])
            subplot_args = grid + [n]
            plot_args = (yield ax)
            ax = subplot(*subplot_args)
            if clear_subplot: ax.clear()
            plot(*plot_args)
            draw()
    coroutine = _subplots()
    coroutine.next()
    return coroutine

#####
# Tools
#####
def limited(generator, num_iters=10):
    """Limit a generator to num_iters"""
    for n,x in enumerate(generator):
        if n >= num_iters:
            break
        yield x

#####
# Analyzing post content
#####
def get_parsed_content(yield_with_post_id=False, **pymongo_find_kwargs):
    if not pymongo_find_kwargs: pymongo_find_kwargs = {'skip': 8050, 'limit': 10}
    db = get_pymongo()
    for post_data in db.tp2.find(fields=['post_id', 'content'], **pymongo_find_kwargs):
        print post_data
        content = post_data['content']
        parsed = BeautifulSoup(content)
        if yield_with_post_id:
            yield (post_data['post_id'], parsed)
        else: yield parsed

def most_popular_posts(df = None, db = None, yield_with_post_id=False):
    """Yields post_ids sorted by most likes"""
    if not df: df = get_tu()
    if not db: db = get_pymongo()
    post_ids = df.post_id.value_counts().index
    for pid in post_ids:
        content = db.tp2.find_one({'post_id': pid}, fields=['content'])['content']
        parsed = BeautifulSoup(content)
        if yield_with_post_id: 
            yield (pid, parsed)
        else: yield parsed


#gen = most_popular_posts()
#for x in limited(gen):
def describe_content_tags():
    print 'find most popular tags in the first XXX most popular posts'
    gen = most_popular_posts()
    dist = nltk.FreqDist(tag.name 
            for parsed in limited(gen, 1000)
            for tag in parsed.findAll())
    dist.plot()

    print 'count # youtube links in first XXX most popular posts'
    gen = most_popular_posts()
    num_youtube_links = []
    for parsed in limited(gen, 1000):
        for tag in parsed.findAll('a'):
            url = dict(tag.attrs).get('href', '')
            if 'youtube' in url:
                print url
        #aggregate.  seriously, I'm being tired and lazy...
        num_youtube_links.append(sum(1
            for tag in parsed.findAll('a') 
            if 'youtube' in dict(tag.attrs).get('href', '')))
    return num_youtube_links

def tokenize_words(parsed):
    words = nltk.word_tokenize(parsed.text)
    freq_dist = nltk.FreqDist(words)
    return freq_dist

#t = get_parsed_content()
#print 'parsed stuff in t'

