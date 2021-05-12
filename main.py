import numpy as np
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load dataset
anime_data = pd.read_csv('cleaned_anime.csv')

# TF-IDF vectorizer Matrix from Pickle
with open('tfv_matrix', 'rb') as f:
    tfv_matrix = pickle.load(f)

# Compute the sigmoid kernel
sigmoid_matrix = sigmoid_kernel(tfv_matrix, tfv_matrix)

# Indices to find the anime
indices = pd.Series(anime_data.index, index = anime_data['name']).drop_duplicates()

# Recommendation Function

def give_rec(title, sig = sigmoid_matrix):
    # Get index corresponding to original title
    idx = indices[title]

    # Get the pairwise similarity Scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the animes
    sig_scores = sorted(sig_scores, key = lambda x: x[1], reverse=True)

    # Anime indices
    anime_indices = [i[0] for i in sig_scores]

    recommendation = pd.DataFrame({'Anime name' : anime_data['name'].
        iloc[anime_indices].values,
        'Rating' : anime_data['rating'].iloc[anime_indices].values})

    return  recommendation['Anime name'][0], recommendation['Anime name'][1], recommendation['Anime name'][2]




    

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
    first, second, third = give_rec(title) # Top 3 similar Anime
    return f'The top 3 recommendations for you are {first}, {second} and {third}'

if __name__ == '__main__':
    app.run(debug = True)

