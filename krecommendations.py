# import the necessary libraries
from math import sqrt
from random import shuffle

import pandas as pd
import numpy as np


# class which contains all the necessary methods for creating the recommender system:
class KRecommender:
    # constructor which introduces the datafiles:
    def __init__(self, data_file='u.data', item_file='u.item'):
        # create headings for the u.data file
        self.data_headings = ['user_id', 'movie_id', 'rating', 'timestamp']
        # create headings for the u.item file
        self.item_headings = ['movie_id', 'movie_title', 'release_date', 'NaN', 'imdb', 'unknown', 'Action',
                              'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama',
                              'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-fi', 'Thriller',
                              'War', 'Western']
        # set self.data_file equal to data_file
        self.data_file = data_file
        # set self.item_file equal to item_file
        self.item_file = item_file

        self.movie_preferences = self.load_item_preferences()
        self.user_preferences = self.load_user_preferences()

    # method for loading the user preference data:
    def load_user_preferences(self):
        # return and structure the user preferences dataset from the provided file (u.data by default)
        return pd.read_csv(self.data_file, sep='\t', names=self.data_headings, encoding='latin-1')

    # method for loading the movie related data:
    def load_item_preferences(self):
        # return and structure the movies dataset from the provided file (u.item by default)
        return pd.read_csv(self.item_file, sep='|', names=self.item_headings, encoding='latin-1')

    # method for obtaining the cosine similarity between users:
    def cosine_score(self, user1, user2):
        # user1 & user2 : user ids of two users between which similarity score is to be calculated
        # set all of user1's preference info as a
        a = self.user_preferences.loc[self.user_preferences.user_id == user1]
        # set all of user2's preference info as b
        b = self.user_preferences.loc[self.user_preferences.user_id == user2]
        # find intersection of the movie ids for user 1 and user 2 (aka create a set)
        s = np.intersect1d(a.movie_id, b.movie_id)
        # find the value of the numerator (sum of the values of a multiplied by b)
        numerator = sum(a.loc[a.movie_id == x, 'rating'].values[0] * b.loc[b.movie_id == x, 'rating'].values[0] for x in s)
        # find the value of the first half of the denominator (sqrt of the sum of the values of a squared)
        user1_sos = sqrt(sum(a.loc[a.movie_id == x, 'rating'].values[0] ** 2 for x in a.movie_id.values.tolist()))
        # find the value of the second half of the denominator (sqrt of the sum of the values of b squared)
        user2_sos = sqrt(sum(b.loc[b.movie_id == x, 'rating'].values[0] ** 2 for x in b.movie_id.values.tolist()))
        # divide the numerator value by the multiplied denominator values
        result = numerator / (user1_sos * user2_sos)
        # return the result
        return result

    # method for obtaining the pearson similarity between users:
    def pearson_score(self, user1, user2):
        # user1 & user2 : user ids of two users between which similarity score is to be calculated.
        # set all of user1's preference info as a
        a = self.user_preferences.loc[self.user_preferences.user_id == user1]
        # set all of user2's preference info as b
        b = self.user_preferences.loc[self.user_preferences.user_id == user2]
        # find intersection of the movie ids for user 1 and user 2 (aka create a set)
        s = np.intersect1d(a.movie_id, b.movie_id).tolist()

        # if there are 0 movies in common, return -1 since they have no correlation
        if len(s) == 0:
            return -1

        # get ratings for each user for movies in s (the set)
        ai = a.loc[a.movie_id.isin(s), 'rating'].values
        bi = b.loc[b.movie_id.isin(s), 'rating'].values

        # If users have equivalent data, return 1
        if np.array_equiv(ai, bi):
            return 1
        # disable divide by zero errors and NaN to keep from cluttering output. This is expected for certain cases.
        np.seterr(divide='ignore', invalid='ignore')
        # Use Numpy to generate the pearson correlation
        nz = np.corrcoef(ai, bi)[1, 0]
        # Reset errors back to default to prevent missing other, unrelated ones
        np.seterr()
        # Return score
        return nz

    # method for obtaining the euclidean similarity between users:
    def euclidean_score(self, user1, user2):
        # user1 & user2 : user ids of two users between which similarity score is to be calculated.
        # set all of user1's preference info as a
        a = self.user_preferences.loc[self.user_preferences.user_id == user1]
        # set all of user2's preference info as b
        b = self.user_preferences.loc[self.user_preferences.user_id == user2]
        # find intersection of the movie ids for user 1 and user 2 (aka create a set)
        s = np.intersect1d(a.movie_id, b.movie_id)
        # calculates the square root of the sum of the squared difference between a and b
        return int(sqrt(sum(
            ((a.loc[a.movie_id == x, 'rating'].values[0]
              - b.loc[b.movie_id == x, 'rating'].values[0]) ** 2)
            for x in s)))

    # method for obtaining the jaccard similarity between users:
    def jaccard_score(self, user1, user2):
        # user1 & user2 : user ids of two users between which similarity score is to be calculated.
        # set all of user1's preference info as a
        a = self.user_preferences.loc[self.user_preferences.user_id == user1]
        # set all of user2's preference info as b
        b = self.user_preferences.loc[self.user_preferences.user_id == user2]

        # find size of the intersection of the movie ids for user 1 and user 2
        inter = len(np.intersect1d(a.movie_id, b.movie_id))
        # find size of the union of the movie ids for user 1 and user 2
        uni = len(np.union1d(a.movie_id, b.movie_id))
        # return intersection size divided by union size
        return inter / uni

    # method for obtaining the manhattan similarity between users:
    def manhattan_score(self, user1, user2):
        # user1 & user2 : user ids of two users between which similarity score is to be calculated.
        # set all of user1's preference info as a
        a = self.user_preferences.loc[self.user_preferences.user_id == user1]
        # set all of user2's preference info as b
        b = self.user_preferences.loc[self.user_preferences.user_id == user2]
        # find intersection of the movie ids for user 1 and user 2 (create a set)
        s = np.intersect1d(a.movie_id, b.movie_id)
        # return the sum of the absolute value of the difference in values between a and b
        return sum(
            abs(a.loc[a.movie_id == x, 'rating'].values[0]
                - b.loc[b.movie_id == x, 'rating'].values[0]) for x in s)

    # Method for getting the most similar users to the target user:
    def get_most_similar_users_to_user(self, user1, number_of_users, metric='pearson'):
        # notes:
        # parameter user1- Targeted User
        # parameter number_of_users- number of most similar users to return
        # parameter metric- metric to be used to calculate inter-user similarity score. ('pearson' by default)
        # return list of tuples [(score, user_id)]
        # Get distinct user ids and set as user_ids
        user_ids = self.user_preferences.user_id.unique().tolist()
        # Conditions that allow the program user to change which metric to use and attach a string of the metric to the appropriate method:
        if metric == 'cosine':
            similarity_score = [(self.cosine_score(user1, nth_user), nth_user) for nth_user in
                                user_ids[:100] if
                                nth_user != user1]
        elif metric == 'euclidean':
            similarity_score = [(self.euclidean_score(user1, nth_user), nth_user) for nth_user in
                                user_ids[:100] if
                                nth_user != user1]
        elif metric == 'pearson':
            similarity_score = [(self.pearson_score(user1, nth_user), nth_user) for nth_user in
                                user_ids[:100] if
                                nth_user != user1]
        elif metric == 'jaccard':
            similarity_score = [(self.jaccard_score(user1, nth_user), nth_user) for nth_user in
                                user_ids[:100] if
                                nth_user != user1]
        else:
            similarity_score = [(self.manhattan_score(user1, nth_user), nth_user) for nth_user in
                                user_ids[:100]
                                if nth_user != user1]
        # Sort the scores in descending order
        similarity_score.sort()
        similarity_score.reverse()
        # Returning the top most 'number_of_users' similar users to a target user
        return similarity_score[:number_of_users]

    # Method for getting the movie recommendations for the target user:
    def get_movie_recommendations_for_user(self, user_id, comparisons=200, recommendations=10, metric='pearson'):
        # Notes:
        # parameter user_id- Targeted User
        # parameter comparisons - Number of other users from which to generate recommendations
        # parameter recommendations - Number of recommendations to return
        # parameter metric- Metric to be used to calculate movie preference similarity score. ('pearson' by default)
        # return list of recommended movie titles

        # Get distinct user ids and set as user_ids
        user_ids = self.user_preferences.user_id.unique().tolist()
        # Shuffle list to prevent comparing to the same n users each time
        shuffle(user_ids)
        # Sum of user similarity scores per movie
        similarty_score_total = {}
        # Total similarity score based on user ratings per movie
        comparison_score_total = {}

        for target_user in user_ids[:comparisons]:
            if target_user == user_id:
                continue

            # Conditions that allow the program user to change which metric to use
            # and attach a string of the metric to the appropriate method:
            if metric == 'cosine':
                score = self.cosine_score(user_id, target_user)
            elif metric == 'euclidean':
                score = self.euclidean_score(user_id, target_user)
            elif metric == 'pearson':
                score = self.pearson_score(user_id, target_user)
            elif metric == 'jaccard':
                score = self.jaccard_score(user_id, target_user)
            else:
                score = self.manhattan_score(user_id, target_user)
            # do not consider users having zero or less similarity score:
            if score <= 0:
                continue
            # Get the weighted similarity score and sum of similarities between both the users:
            for movie_id in self.get_all_movies_for_user(target_user):
                # Only considering not watched/rated movies:
                if self.validate_movie_id(user_id, movie_id):
                    comparison_score_total[movie_id] = 0
                    comparison_score_total[movie_id] += self.get_rating_for_user(target_user, movie_id) * score
                    similarty_score_total[movie_id] = 0
                    similarty_score_total[movie_id] += score

        # Normalize ratings dividing recommended_score by the similarity sum and ranking the movies in descending order
        ranking = []
        for movie, score in comparison_score_total.items():
            r = score / similarty_score_total[movie]
            ranking.append((r, movie))

        # Sort (ascending) rankings
        ranking.sort()
        # Reverse to get the highest rankings
        ranking.reverse()

        # convert movie_ids to titles
        recommended_movies = [self.get_movie_title(movie_id) for score, movie_id in ranking[:recommendations]]
        # return the top 'number_of_movies' based on similarity score (any metric)
        return recommended_movies

    # Determine if movie and rating are valid to use for recommendation scoring and ranking
    def validate_movie_id(self, user_id, movie_id):
        ids = self.user_preferences.loc[(self.user_preferences.user_id == user_id), 'movie_id'].tolist()
        return movie_id not in ids or self.get_rating_for_user(user_id, movie_id) == 0

    # Get the movie's rating (1 - 5) for a user based on movie_id
    def get_rating_for_user(self, user_id, movie_id):
        a = self.user_preferences.loc[
            (self.user_preferences.user_id == user_id) & (self.user_preferences.movie_id == movie_id), 'rating']
        return a.iloc[0]

    # Get a list of all movies for a user_id
    def get_all_movies_for_user(self, user_id):
        return self.user_preferences.loc[(self.user_preferences.user_id == user_id), 'movie_id'].tolist()

    # Get the title of a movie from a movie_id
    def get_movie_title(self, movie_id):
        return self.movie_preferences.loc[(self.movie_preferences.movie_id == movie_id), 'movie_title'].iloc[0]