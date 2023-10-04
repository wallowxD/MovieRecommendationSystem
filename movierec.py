import numpy as np
import pandas as pd

links_df = pd.read_csv('data/links.csv')
movies_df = pd.read_csv('data/movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')
tags_df = pd.read_csv('data/tags.csv')

movies_rate_df = movies_df.merge(ratings_df, on='movieId')

movie_title = input('Input your fav movie name (with release year): ')

movie_in_db = movies_rate_df['title'] == movie_title

if not np.any(movie_in_db):
    # Find the most similar titles
    similar_name = []
    added_titles = []
    movie_title_words = [w.strip() for w in movie_title.lower().split(' ')]


    # Find similar titles
    for title in movies_rate_df['title'].values:
        points = 0

        for word in title.lower().split(' '):
            if word in movie_title_words:
                points += 1

        # Don't add the same title
        if title not in added_titles:
            similar_name.append((title, points,))
            added_titles.append(title)

    # Choose the biggest pointed five
    del added_titles, movie_title_words
    similar_name = sorted(similar_name, key=lambda x: x[1], reverse=True)[:5]

    # Ask user for input
    print("We can't find your movie in our database.")
    print('Here are some movies with similiar titles')
    print('-' * 50)
    print('Index\tMovie title')

    for i, title in enumerate(similar_name):
        print('(' + str(i + 1) + '):\t' + title[0]) 
    
    print('-' * 50)
    print()
    print('Please choose the index for one of the movie above. (Choose index 0 to exit)')
    movie_index = input('Movie index: ')

    try:
        movie_index = int(movie_index)
    except ValueError:
        print('Wrong index, please input a number from 1 to 5.')
        exit(1)

    if movie_index == 0:
        exit()
    else:
        movie_title = similar_name[movie_index - 1][0]

rec_movies = []

movies_db = movies_rate_df[movies_rate_df['title'] == movie_title].sort_values(by='rating', ascending=False)

#10 people rated this movie highest
for userId in movies_db.iloc[:10]['userId'].values:
    #list of rated movies of this user
    rate_movies = movies_rate_df[movies_rate_df['userId'] == userId]
    #3 highest rated movies of this user, excluding the movie from input
    rate_movies = rate_movies[rate_movies['title'] != movie_title].sort_values(by='rating', ascending=False).iloc[:3]
    
    rec_movies.extend(list(rate_movies['title'].values))

rec_movies = np.unique(rec_movies)
    
#Soft movies in the recommend list by genres similarity
input_genres = movies_rate_df[movies_rate_df['title'] == movie_title].iloc[0]['genres'].split('|')
similar_genre_counter = {}

for movie in rec_movies:
    movie_genres = movies_rate_df[movies_rate_df['title'] == movie].iloc[0]['genres'].split('|')
    sgc = 0
    
    for genre in input_genres:
        if genre in movie_genres:
            sgc += 1
    
    similar_genre_counter[movie] = sgc
    
    
rec_movies = sorted(similar_genre_counter, key=lambda x: similar_genre_counter[x], reverse=True)
print('\nWe have found these movies for you: \n')
print('-' * 50)

for movie in rec_movies:
    print(movie)
