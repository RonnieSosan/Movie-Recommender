import math
from scipy import spatial
from scipy import stats
import matplotlib.pyplot as plt


# create class for similarity metrics
class SimilarityMetrics:
    def __init__(self, isShowCommonMovies = False):
        self.isShowCommonMovies = isShowCommonMovies
    
    def GetCommonMovieRatings(self, userOne, userTwo):
        # initialize the userOneMovies to a set of movies rated by user_one
        userOneMovies = set(userOne.ratings)
        # initialize the userTwoMovies to a set of movies rated by user_two
        userTwoMovies = set(userTwo.ratings)
        # intersect user one_movies in user_two to get their common movies
        commonMovies = userOneMovies.intersection(userTwoMovies)
        # initialize list of ratings for buth user_one and user_two movie rating
        userOneMovieRatings = []
        userTwoMovieRatings = []
    
        for movie in commonMovies:
            userOneMovieRatings.append(userOne.ratings[movie])
            userTwoMovieRatings.append(userTwo.ratings[movie])
            if self.isShowCommonMovies == True:
                print("Movie: {0}, User1 Rating: {1}, User2 Rating: {2}".format(movie, userOne.ratings[movie], userTwo.ratings[movie]))
        return (userOneMovieRatings, userTwoMovieRatings)
    
    def GetUncommonMovies(self, targetUser, userTwo):
        # initialize the userOneMovies to a set of movies rated by user_one
        targetUserMovies = set(targetUser.ratings)
        # initialize the userTwoMovies to a set of movies rated by user_two
        userTwoMovies = set(userTwo.ratings)
        # intersect user one_movies in user_two to get their common movies
        commonMovies = targetUserMovies.intersection(userTwoMovies)
        
        # initialize list of ratings for both target_user and user_two movie rating common to the users
        for movie in commonMovies:
            #remove the movies from the list in the comparing users, leaving the movies not watched by the target user
            userTwoMovies.remove(movie)
        return list(userTwoMovies)
    
    def cosine_similarity(self, userOne, UserTwo):
        # get the ratings of commonly watched movie by user one and two
        (userOneRatings, userTwoRatings) = self.GetCommonMovieRatings(userOne, UserTwo)
        
        # Check if the ratings are emptyy, meaning they have no commonly watched movies
        if userOneRatings == [] or userTwoRatings == []:
                return math.nan
        return 1 - spatial.distance.cosine(userOneRatings, userTwoRatings)
    
    def manhattan_similarity(self, userOne, UserTwo):
        # get the ratings of commonly watched movie by user one and two
        (userOneRatings, userTwoRatings) = self.GetCommonMovieRatings(userOne, UserTwo)
        
        # Check if the ratings are emptyy, meaning they have no commonly watched movies
        if userOneRatings == [] or userTwoRatings == []:
                return math.nan
        # since this calculates the distance we would then get the similarity
        man_dist = spatial.distance.cityblock(userOneRatings, userTwoRatings)
        
        #this is to eradicate the zero effect when the distance is 0 meaning they are exactly in the same location i.e completely similar
        if man_dist == 0: man_dist = man_dist + 1
        return 1/(man_dist)
    
    def euclidean_similarity(self, userOne, UserTwo):
         # get the ratings of commonly watched movie by user one and two
        (userOneRatings, userTwoRatings) = self.GetCommonMovieRatings(userOne, UserTwo) 
        
        # Check if the ratings are emptyy, meaning they have no commonly watched movies
        if userOneRatings == [] or userTwoRatings == []:
                return math.nan
        # since this calculates the distance we would then get the similarity
        euc_dist = spatial.distance.euclidean(userOneRatings, userTwoRatings)
        
        #this is to eradicate the zero effect when the distance is 0 meaning they are exactly in the same location i.e completely similar
        if euc_dist == 0: euc_dist = euc_dist + 1
        return 1/(euc_dist)
    
    def jaccard_similarity(self, userOne, UserTwo):
         # get the ratings of commonly watched movie by user one and two
        (userOneRatings, userTwoRatings) = self.GetCommonMovieRatings(userOne, UserTwo) 
        
        # Check if the ratings are emptyy, meaning they have no commonly watched movies
        if userOneRatings == [] or userTwoRatings == []:
                return math.nan
        
        return abs(1- spatial.distance.jaccard(userOneRatings, userTwoRatings))
    
    def pearson_similarity(self, userOne, UserTwo):
        # get the ratings of commonly watched movie by user one and two
        (userOneRatings, userTwoRatings) = self.GetCommonMovieRatings(userOne, UserTwo)
        
        # Check if the ratings are emptyy, meaning they have no commonly watched movies
        if userOneRatings == [] or userTwoRatings == []:
                return math.nan

        #using the pearsons correlation from scipy statistics library
        (corr, p_value) = stats.pearsonr(userOneRatings, userTwoRatings)
        return abs(corr)
    
    def movie_cosine_similarity(self, movieOneGenre, movieTwoGenre):
        # calculating cosine similarity using scipy spartian library
        return 1 - spatial.distance.cosine(movieOneGenre, movieTwoGenre)
    
    def Movie_Similarity(self, movieOne, movieTwo, func):
        #The function passed in as an arguement for implementing the movie similarity is called
        return func(movieOne.genre, movieTwo.genre)
   
    def TopUsersSimilarToTarget(self, user_preference, targetUser, function, userCount):
        user_similarity = {}
        
        for sampleUser in user_preference:
            #checks if the current user id in the loop is the same as the target user, skip if true
            if targetUser.userId == sampleUser.userId:
                continue
            
            #setv the value of the similarity score to the variable
            similarityScore = function(targetUser, sampleUser)
            # use math.isnan() instead of numpy.isnan() since the math function takes a lot less memory than numpy
            if math.isnan(similarityScore):
                continue
            user_similarity[sampleUser.userId] = similarityScore
            
        sortedList = {id: score for id, score in sorted(user_similarity.items(), key=lambda item: item[1], reverse=True)}
        return {id:score for id,score in [x for x in sortedList.items()][0:userCount]}
    
 
    def TopMoviesSimilarToTarget(self, movie_genre_watchers, targetMovie, function, movieCount):
        movie_Similarity = {}
        
        for sampleMovie in movie_genre_watchers:
            if targetMovie.movieTitle == sampleMovie.movieTitle:
                continue
            
            similarityScore = function(sampleMovie.genre, targetMovie.genre)
            # use math.isnan() instead of numpy.isnan() since the math function takes a lot less memory than numpy
            if math.isnan(similarityScore):
                continue
            movie_Similarity[sampleMovie.movieTitle] = similarityScore
            
        sortedList = {id: score for id, score in sorted(movie_Similarity.items(), key=lambda item: item[1], reverse=True)}
        return {id:score for id,score in [x for x in sortedList.items()][0:movieCount]}
    
    def GetRecommendedMovies(self,targetUser, user_preference, movie_genre_watchers, numberOfMovies):
        uncommonMoviesPool = []
        recommendedMovies = {}
        
        # get the top ten most similar users to the target user
        topUsers = self.TopUsersSimilarToTarget(user_preference, targetUser, self.cosine_similarity, 10)
        
        #loop through the list of users most similar to the target user
        for userId in topUsers.keys():
            #get the use from the list of users
            user = [x for x in user_preference if x.userId == userId][0]
            # get the list of uncommon movies between the target user and the comparing user to know movies not yet seen by the target user
            uncommonMoviesForUser = self.GetUncommonMovies(targetUser, user)
            for movie in uncommonMoviesForUser:
                if movie not in uncommonMoviesPool:
                    uncommonMoviesPool.append([x for x in movie_genre_watchers if x.movieTitle == movie][0])
                    
        #Get top rated movie, showing the movies the user likes the most
            
        # get the average rating of the user and select the top rated movies
        averageRating = sum([x for key,x in targetUser.ratings.items()])/ len(targetUser.ratings)
        topRatedMovies = {id: score for id, score in sorted(targetUser.ratings.items(), key=lambda item: item[1], reverse=True) if score >= averageRating}
            
        # now we have gotten the recommendable movies for the target user
            
        #loop through each top rated movies by the target user
        for title in topRatedMovies:
            targetMovie = [x for x in movie_genre_watchers if x.movieTitle == title][0]
            #get the list of movies in order of their relation to the target movie i.e the movie most rated by the target user, loop through the list of movies derived
            for Id,score in self.TopMoviesSimilarToTarget(uncommonMoviesPool, targetMovie, self.movie_cosine_similarity, 5).items():
                #check if the movie already exists in the dictionary
                if Id not in recommendedMovies.keys():
                    recommendedMovies[Id] = score
        
        # sort the list of recommended movies in descending order by the similarity score i,e the top movie would have the highest similarity score
        sortedList = {id: score for id, score in sorted(recommendedMovies.items(), key=lambda item: item[1], reverse=True)}
        # return the top n movies recommended to the user using the number set as n by the user
        return {id:score for id,score in [x for x in sortedList.items()][0:numberOfMovies]}
    
    def PlotSimilarities(self, targetUser, ComparingUsers):
        # initialise the various lists for the similarity scores of the various users
        cosine_similarity = []
        manhattan_similarity = []
        jaccard_similarity = []
        euclidean_similarity = []
        pearson_similarity = []
        
        try:
            #loop through the list of the comparing users
            for i in range(len(ComparingUsers)):
                # the similarity score using each similarity metric between users in both lists at index i 
                cosine_similarity.append(self.cosine_similarity(targetUser, ComparingUsers[i]))
                manhattan_similarity.append(self.manhattan_similarity(targetUser, ComparingUsers[i]))
                euclidean_similarity.append(self.euclidean_similarity(targetUser, ComparingUsers[i]))
                jaccard_similarity.append(self.jaccard_similarity(targetUser, ComparingUsers[i]))
                pearson_similarity.append(self.pearson_similarity(targetUser, ComparingUsers[i]))

            # set the sixe of the plot
            plt.figure(figsize=(20,10))
            # add each graph to the plot
            plt.plot(cosine_similarity, "r-o", label = "cosine similarity")
            plt.plot(manhattan_similarity, "b-x", label = "manhattan similarity")
            plt.plot(euclidean_similarity, "g-+", label = "euclidean similarity")
            plt.plot(jaccard_similarity, "c-*", label = "jaccard similarity")
            plt.plot(pearson_similarity, "k-h", label = "pearson similarity")
            #label the y axis as similarity score
            plt.ylabel("Similarity Score")
            # set the legend to the best possible fit
            plt.legend(loc="best")
        
            #show plot
            plt.show()
        except:
            print("Error while plotting graph")
        
        
        
            