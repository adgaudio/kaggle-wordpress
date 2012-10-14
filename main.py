import pylab
pylab.ion()

from monary import Monary
import numpy
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

def get_tu(_cache=[]):
    if not _cache:
        conn, dbname = get_monary()
        columns = ['blog', 'inTestSet', 'post_id', 'uid', 'like_dt']
        arrs = conn.query(dbname, 'tu2', {}, columns, ['int32']*4+['date'])
        df = numpy.matrix(arrs).transpose()
        df = DataFrame(df, columns = columns)
        _cache.append(df)
    return _cache[0].copy(deep=True)

def get_tp(conn=None):
    conn, dbname = get_monary()
    print "not implemented, bumt here's the tp collection using pymongo driver"
    return get_pymongo.tp
    #columns = []
    #arrs = conn.query(dbname, '

#####
# Plotting
#####
def subplots(grid=[2,2], figure_index=1, clear_subplot=True):
    """ Iteratively draw pylab subplots in a grid.
    You may need to set pylab.ion() to do this interactively
    Examples:

    >>> import pylab ; pylab.ion()
    >>> p = subplots(grid=[1,2])
    >>> for x in range(5):
            p.send([range(10), range(10), 'r-'])
            p.send({'args':[[1,2,3], [1,3,2]],
                    'kwargs': {'marker': 'o', 'color': 'green'}})
            subplt = p.send([range(10), range(10), 'b^'])
            subplt.set_title('hello') ; pylab.draw()
    """
    # initialized coroutine by wrapping in closure
    def _subplots():
        pylab.figure(figure_index)
        n = -1
        ax = None
        while True:
            n = (n+1) % (grid[0] * grid[1])
            grid_size_w_index = grid + [n]

            plot_params = (yield ax)
            if isinstance(plot_params, dict):
                plot_kwargs = plot_params.get('kwargs', {})
                plot_args = plot_params.get('args', ())
            else:
                plot_args = plot_params
                plot_kwargs = {}
            ax = pylab.subplot(*grid_size_w_index)
            if clear_subplot: ax.clear()
            pylab.plot(*plot_args, **plot_kwargs)
            pylab.draw()
    coroutine = _subplots()
    coroutine.next()
    return coroutine

def plot_labeled_histogram(dist, fig):
    """Create labeled histograms using subplots()
    Given a dict or nltk.FreqDist. Yea, this is ridiculous :)"""
    tag_ids = {}
    for key in dist.keys():
        tag_ids[key] = len(tag_ids)
    x = [tag_ids[key] for key in dist.keys()]
    y = dist.values()
    fig.send({'args':( x, y ), 'kwargs': {'linestyle':'', 'marker':'^'}})
    pylab.xticks([tag_ids[key] for key in dist.keys()], 
            [key for key in dist.keys()],
            rotation=90)

#####
# Tools
#####
def limited(generator, num_iters=10):
    """Limit a generator to num_iters. 
    If num_iters == None, assume infinite generator"""
    if num_iters == None: num_iters = float('inf')
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

def most_popular_content(df = None, db = None, yield_with_post_id=False, _cache={}):
    """Yields parsed content of posts sorted by most likes"""
    if not df: df = get_tu()
    if not db: db = get_pymongo()
    if 'value_counts().index' not in _cache:
        _cache['value_counts().index'] = df.post_id.value_counts().index
    post_ids = _cache['value_counts().index']

    for pid in post_ids:
        try:
            content = db.tp2.find_one({'post_id': pid}, fields=['content'])['content']
        except:
            print "pid %s exists in tu but not in tp" % pid
            continue
        parsed = BeautifulSoup(content)
        if yield_with_post_id: 
            yield ( pid, parsed )
        else: yield parsed

def describe_content_html_tags(batch_size=1000, num_batches=4, plot_=True):
    """find frequency distribution of html tags
    in the first XXX most popular posts"""
    gen = most_popular_content()
    if plot_: fig = subplots([2,1])
    dists = []
    for _ in range(num_batches):
        dist = nltk.FreqDist(tag.name 
                for parsed in limited(gen, batch_size)
                for tag in parsed.findAll())
        if plot_: plot_labeled_histogram(dist, fig)
        dists.append(dist)
    return dists

def _count_youtube_links(num, plot_=True):
    print 'count # youtube links in first XXX most popular posts'
    gen = most_popular_content()
    num_youtube_links = numpy.zeros(num)
    for n, parsed in enumerate(limited(gen, num)):
        #debug:
        for tag in parsed.findAll('a'):
            url = dict(tag.attrs).get('href', '')
            if 'youtube' in url:
                print url
        num_youtube_links[n] = sum(1
            for tag in parsed.findAll('a') 
            if 'youtube' in dict(tag.attrs).get('href', ''))
    if plot_: pylab.plot(num_youtube_links) # hopefully this looks like a normal distribution
    return num_youtube_links

def describe_content(num=1000):
    dist=describe_content_html_tags(num)
    num_youtube_links = _count_youtube_links(num)
    return dist, num_youtube_links


def tokenize_words(parsed):
    words = nltk.word_tokenize(parsed.text)
    freq_dist = nltk.FreqDist(words)
    return freq_dist

#t = get_parsed_content()
#print 'parsed stuff in t'

