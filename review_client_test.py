import requests
import json

REVIEW_SERVICE_URL = "127.0.0.1"

def post_new_review(user_id, game_title, rating, comment):
    """Submits a new review to the microservice via POST."""
    data = {
        "user_id": user_id,
        "game_title": game_title,
        "rating": rating,
        "comment": comment
    }
    try:
        response = requests.post(f"{REVIEW_SERVICE_URL}/add", json=data)
        response.raise_for_status()
        result = response.json()
        print(f"POST Success (Status: {result['status']}): {result['message']}")
    except requests.exceptions.RequestException as e:
        print(f"POST Error: {e}")

def get_game_reviews(game_title):
    """Retrieves reviews for a specific game via GET."""
    try:
        response = requests.get(f"{REVIEW_SERVICE_URL}/{game_title}")
        response.raise_for_status()
        reviews = response.json()
        print(f"\n--- Approved Reviews for '{game_title}' ---")
        if reviews:
            for review in reviews:
                print(f"User {review['user_id']} rated it {review['rating']}/5: '{review['comment']}'")
        else:
            print("No approved reviews found.")
    except requests.exceptions.RequestException as e:
        print(f"GET Error: {e}")

if __name__ == '__main__':
    # --- Integration Demonstration ---
    print("Running Review Service Client Test with Moderation...")

    # 1. Post valid reviews
    post_new_review(user_id=101, game_title="Elden Ring", rating=5, comment="A masterpiece of open-world design!")
    post_new_review(user_id=102, game_title="Elden Ring", rating=4, comment="Difficult, but very rewarding.")

    # 2. Post a review that should be rejected (contains a word in BAD_WORDS)
    post_new_review(user_id=999, game_title="Elden Ring", rating=1, comment="This game contains a bad word!")

    # 3. Retrieve approved reviews for Elden Ring (the rejected one should NOT appear)
    get_game_reviews("Elden Ring")
