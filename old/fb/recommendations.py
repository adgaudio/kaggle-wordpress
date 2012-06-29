from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def get_si(prefs,p1,p2):
    return [ item for item in prefs[p1] if item in prefs[p2] ]

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,p1,p2):
    #Get the list of shared_items
    si = get_si(prefs,p1,p2)

    # If no ratings in common, return 0
    if not si:
        return 0
    
    # Add up the squares of all the differences
    ss = sum([pow(prefs[p1][item]-prefs[p2][item],2) for item in si])
    
    return 1/(1+ss)
    
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
    si = get_si(prefs,p1,p2)

    # If no ratings in common, return 0
    if not si:
        return 0

    n = len(si)
    
    # Add up all the preferences
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])

    # Sum up the squares
    ss1 = sum([pow(prefs[p1][item],2) for item in si])
    ss2 = sum([pow(prefs[p2][item],2) for item in si])

    # Sum up the products
    ps = sum([prefs[p1][item]*prefs[p2][item] for item in si])

    # Calculate the Pearson score (correlation coefficient)
    num = ps - (sum1*sum2)/n
    den = sqrt((ss1 - pow(sum1,2)/n)*(ss2 - pow(sum2,2)/n))
    if den == 0:
        return 0

    r = num/den
    return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def get_topMatches(prefs,person,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) for other in prefs if other != person]

    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores

# Gets recommendations for a person by using a weighted average
# of every other user's rankings

def get_recommendations(prefs,person,similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs,person,other)

        # ignore scores of zero or lower
        if sim <= 0:
            continue

        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:

                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
               
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # Create the normalized list
    rankings = [(total/simSums[item],item) for item,total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result
