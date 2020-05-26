import pandas as pd
#Utilizing the OOP paradigm we create simple objects of Movirs and Users

class User:
    def __init__(self, userId = 0, ratings = {}):
        self.userId = userId
        self.ratings = ratings
    
    def setRatings(self, ratings):
        self.ratings = ratings
    
    def getRating(self, movieId):
        return self.ratings
    
class Movie:
    def __init__(self, movieTitle = 0, watchers = [], genre = []):
        self.movieTitle = movieTitle
        self.watchers = watchers
        self.genre = genre
    
    def setWatchers(self, watchers):
        self.watchers = watchers
    
    def setGenre(self, genre):
        self.genre = genre
        

#create a class for loading datasets
class loadDatasets:
    #Initialize class variables
    def __init__(self, movies_file_name = 'u.item', users_file_name = 'u.data'):
        # assigning the variables to the object in this constructor
        self.movies_file_name = movies_file_name
        self.users_file_name = users_file_name
        self.usersRatings = self.GetUserRating()
        self.movies = self.loadMovies()
        
    def loadMovies(self):
         # Get movie titles
            try:
                #i = 0
                movies = {}
                loadedData = pd.read_csv(self.movies_file_name,sep='|', names=["MovieId", "MovieTitle", "ReleaseDate", "Unknown","IMDB_site",
                                                             "0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"],
                                                              encoding = "ISO-8859-1")
                for id,movie in loadedData.iterrows():
                    
                    genre = [movie["0"],movie["1"],movie["2"],movie["3"],movie["4"],movie["5"],movie["6"],movie["7"],
                             movie["8"],movie["9"],movie["10"],movie["11"],movie["12"],movie["13"],movie["14"],movie["15"],movie["16"],movie["17"],movie["18"]]
                    # set the id in the dictionary to map an nested dictionary of title and genre setting all the genre to integer
                    movies[movie["MovieId"]] = {'title': movie["MovieTitle"], 'genre' : genre}
                return movies
            except IOError as ioerr:
                    print('File error: ' + str(ioerr))
    
    def GetUserRating(self):
        # Get movie titles
        try:
            userxRating = []
            users = {}
            loadedData = pd.read_csv(self.users_file_name,sep='\t', names=["UserId", "MovieId", "Rating", "Unknown"])
            # using panda to read the file into a dataframe
            for id,movie in loadedData.iterrows():
                if(movie["UserId"] in users):
                    #if the user exists then set the value if the movie id (index 1) to the rating (index 2)
                    users[movie["UserId"]][movie["MovieId"]] = float(movie["Rating"])
                else:
                    # Create a new
                    users[movie["UserId"]] = {movie["MovieId"] : float(movie["Rating"])}
            return users
        except IOError as ioerr:
            print('File error: ' + str(ioerr))
            
    def loadUserPreferenceData(self):
        # initialize the user_preference dictionary to be returned
        user_preference = []
        #set the movies to the dictionary of movies read from the u.item dataset
        movies = self.movies
        #set the user ratings to the dictionary of users read from the u.data dataset
        userRatings = self.usersRatings
        
        #loop through the users in the dictionary highlighting the userId and movieRatings
        for userId,movieRatings in userRatings.items():
            ratings = {}
            
            # loop through the list of movie ratings for the user
            for movieId,rating in movieRatings.items():
                user = User( userId = userId)
                # Get the corresponding Movie using the Movie Id from the movies dictionary
                movie = movies[movieId]
                # set the mpvie title as the key for the movie rating for the user_preference nested dictionary and the ratsing as the value
                ratings[movie["title"]] = rating
                # pass the ratings dictionary as the value for the user_preference dictionary with the userId as the key
                user.setRatings(ratings)
                user_preference.append(user)           
        return user_preference
    
    def GetUser(self, userId, userPreference):
        for user in userPreference:
            if user.userId == userId:
                return user
    
    def GetMovie(self, movieTitle, movie_genre_watchers):
        for movie in movie_genre_watchers:
            if movie.movieTitle == movieTitle:
                return movie
    
    def GetMovieTitle(self, movieId):
        return self.movies[movieId]['title']
    
    def loadMovieAndWatchers(self):
        # initialize the movie_genres_and_watchers dictionary to be returned
        movie_genres_and_watchers = []
        # initialize the response form the GetUserRating as the value for the usersxRatings
        usersxRatings = self.usersRatings
    
        # loop throught the loaded movies and highlight the key and values 
        for movieId,movieInfo in self.movies.items():
            users = []
            # loop through the usersxRatings dictionary highlighting the userId and values
            for userId,userMovies in usersxRatings.items():
                # set a condition to check if the key (the movieId) exists in the list of rated movies by the user
                if movieId in userMovies.keys():
                    # append the user to the list of watchers for that movie
                    users.append(userId)
            # Instantiate a movie object
            movie = Movie(movieInfo["title"], users, movieInfo["genre"])
            
            # add the Movie object to the list of objects
            movie_genres_and_watchers.append(movie)

        return movie_genres_and_watchers