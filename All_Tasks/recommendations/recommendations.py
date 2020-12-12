#!/usr/bin/env python3

""" recommendations.py

A dictionary of movie critics and their ratings of a small set of movies
taken from the Book 'Kollektive Intelligenz'.

Converted to Python3 by war 20191117

:author:    wolf
:created:   2019.11.17
"""

from math import sqrt
# TODO: upgrade to numpy utilisation
import numpy as np

# preferences used during these examples
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
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
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


def similarity_distance(preferences, person1, person2):
    """Returns a euclidian-distance based similarity score for person1 and person2"""

    # Get the list of shared_items
    similarities = {}

    for item in preferences[person1]:
        if item in preferences[person2]:
            similarities[item] = 1

    # if they have no ratings in common, return 0
    if len(similarities) == 0:
        return 0

    # Add up the squares of all the differences
    a = [pow(preferences[person1][item] - preferences[person2][item], 2)
                          for item in preferences[person1] if item in preferences[person2]]
    sum_of_squares = sum([pow(preferences[person1][item] - preferences[person2][item], 2)
                          for item in preferences[person1] if item in preferences[person2]])

    # calculate similarity as growing for better fit
    # 1 / ( 1 + sum_of_squares) will be one if interests are identical
    similarity = 1 / (1 + sqrt(sum_of_squares))

    return similarity


def similarity_pearson(preferences, person1, person2):
    """Returns the Pearson correlation coefficient for p1 and p2"""

    # Get the list of mutually rated items
    similarities = {}
    for item in preferences[person1]:
        if item in preferences[person2]:
            similarities[item] = 1

    # if they are no ratings in common, return 0
    if len(similarities) == 0:
        return 0

    # Sum calculations
    n = len(similarities)

    # Sums of all the preferences
    sum1 = sum([preferences[person1][i] for i in similarities])
    sum2 = sum([preferences[person2][i] for i in similarities])

    # Sums of the squares
    sum1Sq = sum([pow(preferences[person1][i], 2) for i in similarities])
    sum2Sq = sum([pow(preferences[person2][i], 2) for i in similarities])

    # Sum of the products
    pSum = sum([preferences[person1][i] * preferences[person2][i] for i in similarities])

    # Calculate r (Pearson score)
    numerator = pSum - (sum1 * sum2 / n)
    denominator = sqrt((sum1Sq - (pow(sum1, 2) / n)) * (sum2Sq - (pow(sum2, 2) / n)))
    # prevent division by zero, Pearson coefficient = 0
    if denominator == 0:
        return 0

    r = numerator / denominator

    return r


def topMatches(preferences, person, n=5, similarity=similarity_pearson):
    """Returns the best matches for person from the preferences dictionary.

    Number of results and similarity function are optional params.
    """

    if person not in preferences:
        return 'User not found'

    # find all matches in the data pool, sort them and rank them top-down
    matches = [(similarity(preferences, person, other), other) for other in preferences if other != person]
    matches.sort()
    matches.reverse()

    # return just the top n matches
    return matches[0:n]


def getRecommendations(preferences, person, similarity=similarity_pearson, n=5):
    """Gets recommendations for a person by using a weighted average of every other user's rankings"""

    totals = {}
    simSums = {}
    for other in preferences:
        # don't compare me to myself
        if other == person:
            continue
        sim = similarity(preferences, person, other)

        # ignore scores of zero or lower
        if sim <= 0:
            continue

        for item in preferences[other]:
            # only score movies I haven't seen yet
            if item not in preferences[person] or preferences[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += preferences[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()

    return rankings[0:n]


def transformPrefs(preferences):
    """Transform rows and columns in the preferences matrix
    so that we get the items and then their individual rating
    """
    result = {}
    for person in preferences:
        for item in preferences[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = preferences[person][item]
    return result


def topScores(preferences, n=None):
    """Calculates the total score of each item and returns a reverse-sorted dict"""

    scores = [(sum([rating for rating in preferences[item].values()]), item) for item in preferences.keys()]
    scores.sort()
    scores.reverse()
    if n:
        scores = scores[:n]
    top_scores = {movie: rating for (rating, movie) in scores}

    return top_scores


def calculateSimilarItems(preferences, n=10, similarity=similarity_distance):
    """Create a dictionary of items showing which other items they are most similar to."""

    result = {}

    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(preferences)
    count = 0
    for item in itemPrefs:
        # Status updates for large datasets
        count += 1
        if count % 100 == 0:
            print("{0} / {1}".format(count, len(itemPrefs)))

        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=similarity)
        result[item] = scores

    return result


def getRecommendedItems(preferences, itemMatch, user, n=10):
    """Based on similar items get recommendations

    :param preferences:     preference matrix as used above
    :param itemMatch:       similarity matrix as calculated by calculateSimilarItems
    :param user:            user for which the preferences should be selected
    :returns ranking:       ranking of similar items based on user preferences
    """

    userRatings = preferences[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (user_item, rating) in userRatings.items():

        # Loop over items similar to this one
        for (similarity, match_item) in itemMatch[user_item]:

            # Ignore if this user has already rated this item
            if match_item in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(match_item, 0)
            scores[match_item] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(match_item, 0)
            totalSim[match_item] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()

    return rankings[0:n]


def loadMovieLens(path='../data/movielens-100k'):
    """Get movie preferences"""

    # Get movie titles
    movies = {}

    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    # Load data
    preferences = {}

    for line in open(path + '/u.data'):
        (user, movie_id, rating, ts) = line.split('\t')
        preferences.setdefault(user, {})
        preferences[user][movies[movie_id]] = float(rating)

    return preferences


def read_csv(file='films.csv'):
    """Read rating file and prepare a dictionary for comparison"""

    result = {}
    films = {}

    with open(file, 'r') as f:
        # last name used to determine user switch
        l_name = ''
        for line in f:
            # get username, film and rating
            name, film, rating = line.replace('"','').strip().split(';')
            # do not record films not seen
            if not float(rating):
                continue

            # if we find a new user, we need to store the old values
            if l_name != name:
                # except for the first, empty user ...
                if l_name:
                    # save the
                    result[l_name] = films
                    films = {}
                l_name = name
                result.setdefault(name,{})
                films.setdefault(film, float(rating))
            else:
                films[film] = float(rating)

        # write the last user
        result[name] = films
    return result


if __name__ == '__main__':

    print('Compare Toby and Mick with Euclide: {0}'.format(similarity_distance(critics, 'Toby', 'Mick LaSalle')))
    print('Compare Toby and Mick with Pearson: {0}'.format(similarity_pearson(critics, 'Toby', 'Mick LaSalle')))

    print('Compare Toby and Michael with Pearson: {0}'.format(similarity_pearson(critics, 'Toby', 'Michael Phillips')))


    # user based recommendations
    print("Who matches Toby's taste best ?")
    print('With Euclide:\n{0}'.format(
            topMatches(critics, 'Toby', n=3, similarity=similarity_distance)))
    print('With Pearson:\n{0}'.format(
            topMatches(critics, 'Toby', n=3, similarity=similarity_pearson)))

    print('Which film can we recommend to Toby ?')
    print('With Pearson:\n{0}'.format(
            getRecommendations(critics, 'Toby')))
    print('With Euclide:\n{0}'.format(
            getRecommendations(critics, 'Toby', similarity=similarity_distance)))

    print("Which films are similar to 'Superman Returns' ?")
    movies = transformPrefs(critics)
    print('With Pearson:\n{0}'.format(
            topMatches(movies, 'Superman Returns', similarity=similarity_pearson)))
    print('With Euclide:\n{0}'.format(
            topMatches(movies, 'Superman Returns', similarity=similarity_distance)))
    print('Euclidian distance does not perform well...')

    print("And who would be interested in 'Just My Luck' ?")
    print(getRecommendations(movies, 'Just My Luck'))

    # item based recommendations
    print('Which items are similar ?')
    similar_items_distance = calculateSimilarItems(critics)
    similar_items_pearson = calculateSimilarItems(critics, similarity=similarity_pearson)
    print('With Euclide:\n{0}'.format(similar_items_distance))
    print('With Pearson:\n{0}'.format(similar_items_pearson))

    print('Which similar items based on his/her preferences can we recommend to Toby ?')
    print('With Euclide:\n{0}'.format(
            getRecommendedItems(critics, similar_items_distance, 'Toby')))
    print('With Pearson:\n{0}'.format(
            getRecommendedItems(critics, similar_items_pearson, 'Toby')))

    movielens = loadMovieLens()
    print(movielens['87'])

    print(movies['Snakes on a Plane'])
    print(movies['You, Me and Dupree'])