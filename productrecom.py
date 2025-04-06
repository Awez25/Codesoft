import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
class ProductRecommender:
    def __init__(self, user_data):
        """
        Initializes the system with a user-product ratings dataset.
        """
        self.user_data = pd.DataFrame(user_data).fillna(0) 
        self.user_similarity = None
    def calculate_similarity(self):
        """
        Computes cosine similarity between all users.
        """
         # Create a matrix of user ratings
        user_matrix = self.user_data.iloc[:, 1:].values  
        self.user_similarity = cosine_similarity(user_matrix)
    def recommend_products(self, target_user, top_n=3):
        """
        Recommends products for the given user based on similar users.
        """
        if target_user not in self.user_data['User'].values:
            return f"User '{target_user}' not found in database."
        target_index = self.user_data[self.user_data['User'] == target_user].index[0]
        similarity_scores = self.user_similarity[target_index]
        weighted_ratings = np.dot(similarity_scores, self.user_data.iloc[:, 1:].values)
        target_user_ratings = self.user_data.iloc[target_index, 1:]
        recommendations = {
            product: score for product, score in zip(self.user_data.columns[1:], weighted_ratings)
            if target_user_ratings[product] == 0
        }
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return sorted_recommendations[:top_n]
# Sample dataset (extendable to product categories)
user_data = [
    {"User": "Yuvan", "Laptop": 5, "Smartphone": 4, "Headphones": 3, "Shoes": 2},
    {"User": "Yadu", "Laptop": 4, "Headphones": 5, "Camera": 5, "Backpack": 3},
    {"User": "Adithya", "Smartphone": 5, "Headphones": 4, "Laptop": 4, "Jacket": 3},
    {"User": "Dhruv", "Laptop": 5, "Camera": 4, "Smartwatch": 5, "Shoes": 4},
    {"User": "Matthew", "Smartphone": 4, "Camera": 3, "Laptop": 5, "Backpack": 4}
]
# Initialize and use the system
recommender = ProductRecommender(user_data)
recommender.calculate_similarity()
target_user = "Yuvan"
recommendations = recommender.recommend_products(target_user)
# Display recommendations
print(f"Recommendations for '{target_user}':")
for product, score in recommendations:
    print(f" {product} | Estimated Interest Score: {score:.2f}")