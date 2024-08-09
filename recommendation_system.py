import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.preprocessing import StandardScaler

movies_data = {
    'title': ['Inception', 'The Matrix', 'Avatar', 'Interstellar', 'The Dark Knight'],
    'genre': ['Action Sci-Fi', 'Action Sci-Fi', 'Action Sci-Fi', 'Action Sci-Fi', 'Action']
}

ratings_data = {
    'user': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
    'item': ['Inception', 'The Matrix', 'Avatar', 'Inception', 'The Matrix', 'Avatar', 'Interstellar', 'The Dark Knight'],
    'rating': [5, 3, 4, 2, 5, 4, 5, 4]
}

movies_df = pd.DataFrame(movies_data)
ratings_df = pd.DataFrame(ratings_data)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['genre'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_content_based_recommendations(title, num_recommendations=3):
    idx = movies_df.index[movies_df['title'] == title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]
    movie_indices = [i[0] for i in sim_scores]
    return movies_df.iloc[movie_indices]

user_item_matrix = ratings_df.pivot_table(index='user', columns='item', values='rating').fillna(0)
scaler = StandardScaler()
user_item_matrix_scaled = scaler.fit_transform(user_item_matrix)
user_similarity = cosine_similarity(user_item_matrix_scaled)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def get_collaborative_recommendations(user_id, num_recommendations=3):
    if user_id not in user_similarity_df.index:
        return []
    
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    similar_users = similar_users.drop(user_id)
    
    similar_users_ratings = ratings_df[ratings_df['user'].isin(similar_users.index)]
    user_weights = similar_users.to_dict()
    
    def weighted_rating(item_ratings):
        weighted_sum = 0
        total_weight = 0
        for _, row in item_ratings.iterrows():
            weight = user_weights.get(row['user'], 0)
            weighted_sum += row['rating'] * weight
            total_weight += weight
        return weighted_sum / total_weight if total_weight != 0 else 0
    
    item_ratings = similar_users_ratings.groupby('item').apply(weighted_rating)
    top_recommendations = item_ratings.sort_values(ascending=False).head(num_recommendations)
    
    return top_recommendations

print("Content-Based Recommendations for 'Inception':")
print(get_content_based_recommendations(title='Inception'))

print("\nCollaborative Filtering Recommendations for 'Alice':")
recommendations = get_collaborative_recommendations(user_id='Alice')
for item, rating in recommendations.items():
    print(f"{item}: {rating:.2f}")
