import numpy as np
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load dataset
#anime_data = pd.read_csv('cleaned_anime.csv')

# if it doesn't exist
def create_sim():
    anime_data = pd.read_csv('cleaned_anime.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(anime_data['genre'].values.astype('U'))
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return anime_data,sim

# defining a function that recommends 10 most similar movies
def rcmd(m):
    m = m.lower()
    # check if data and sim are already assigned
    try:
        anime_data.head()
        sim.shape
    except:
        anime_data, sim = create_sim()
    # check if the movie is in our database or not
    if m not in anime_data['name'].unique():
        return('This anime is not in our database.\nPlease check if you spelled it correct.')
    else:
        # getting the index of the movie in the dataframe
        i = anime_data.loc[anime_data['name']==m].index[0]

        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

        # taking top 1- movie scores
        # not taking the first index since it is the same movie
        lst = lst[1:4]

        # making an empty list that will containg all 10 movie recommendations
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(anime_data['name'][a])
        return l


    

# Flask + Swagger
from flask import Flask, render_template, request
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

@app.route('/')
def base_route():
    return "Welcome to Anirudh's Content Based Anime Recommendation System. You can test with /recommend?title=Naruto or /recommend?title=Gintama"

@app.route('/recommend', methods = ['GET'])
def recommend():
    """
    parameters:
    -   name: title
        in: query
        type: string
        required: true
    """
    title = request.args.get('title') # Get the title name from the user
    r = rcmd(title) # Top 3 similar Anime
    return f'The top 3 recommendations for you are {r}'

if __name__ == '__main__':
    uvicorn.run(app)
    #app.run(debug = True)

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')

# print("[top 10 ]")
# for stat in top_stats[:10]:
#     print(stat)
