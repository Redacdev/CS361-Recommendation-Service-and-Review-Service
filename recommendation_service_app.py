from flask import Flask, request, jsonify
# Assuming your original class is in recommendation_service.py
from recommendation_service import RecommendationService
import os

# --- Service Configuration ---
recommendation_app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
recommender = None  # Initialize as None, then load globally

# Initialize the recommendation service (loads model data when app starts)
try:
    data_path = os.path.join(basedir, 'cleaned_games.csv')
    recommender = RecommendationService(data_path=data_path)
    print("Recommendation Service: Model loaded successfully.")
except Exception as e:
    print(f"Recommendation Service Error: Failed to load model data - {e}")


# --- Service API Endpoint ---

@recommendation_app.route('/api/recommend', methods=['POST'])
def get_recommendations_api():
    """
    API endpoint to receive a game title and return recommendations.
    Accepts JSON: {'game_title': 'Desired Game Name'}
    Returns JSON: {'recommendations': ['Rec Game 1', 'Rec Game 2']}
    """
    if recommender is None:
        return jsonify({'error': 'Recommendation service is currently unavailable (Model failed to load).'}), 503

    data = request.get_json()
    game_title = data.get('game_title')

    if not game_title:
        return jsonify({'error': 'Missing game_title in request body'}), 400

    recommendation_titles = recommender.get_recommendations(game_title)

    if not recommendation_titles:
        return jsonify({'recommendations': []}), 404

    return jsonify({'recommendations': recommendation_titles}), 200


if __name__ == '__main__':
    recommendation_app.run(port=5004, debug=True)
