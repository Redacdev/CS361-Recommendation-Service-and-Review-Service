import requests
import json

RECOMMENDATION_SERVICE_URL = "127.0.0.1"


def get_recommendations_for_game(game_title):
    """Requests game recommendations from the microservice via POST."""
    data = {
        "game_title": game_title
    }
    try:
        # Use the 'json' parameter for requests to automatically set Content-Type
        response = requests.post(RECOMMENDATION_SERVICE_URL, json=data)
        response.raise_for_status()

        result = response.json()
        print(f"\n--- Recommendations for '{game_title}' ---")
        if result['recommendations']:
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"{i}. {rec}")
        else:
            print("Service returned no recommendations.")

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"\n--- Recommendations for '{game_title}' ---")
            print(f"Error: Game title '{game_title}' not found in the dataset.")
        else:
            print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")


if __name__ == '__main__':
    # --- Integration Demonstration ---
    print("Running Recommendation Service Client Test...")

    # Test with a known game title from your dataset (e.g., an AppID from your CSV)
    # Replace '252490' with a valid AppID or Name from your cleaned_games.csv file if needed
    get_recommendations_for_game("252490")

    # Test with a non-existent game title
    get_recommendations_for_game("NonExistentGame123")
