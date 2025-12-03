# Recommendation Service and Review Service
A recommendation microservice and a reviews microservice.

### Note: The .csv file used in the example and applied in the service was from a dataset on Kaggle which I applied some pre-processing to. For recommendation service please verify column names with your dataset and make appropriate updates.

### Installing Requirements for Review/Moderation Service:
   - Enter Git Bash, or another terminal of your choice, and navigate to the directory of this repo.
   - Enter 'pip install -r req_rev_mod.txt' to install requirements.

This document provides details on the implementation, integration, and functionality of two independent microservices: the Review/Moderation Service and the Recommendation Service.
## 1. The Review/Moderation Service
This service manages user-submitted reviews for video games, storing them in a dedicated database and applying a simple moderation filter.
   - Port: 5002
   - Database: reviews.db (SQLite)
   - Key Files: review_service.py: Contains the Flask application, SQLAlchemy model, moderation logic, and API endpoints.

### Implementation Details
The service defines a Review model with a status column (pending, approved, rejected). A simple built-in function checks incoming comments for inappropriate words.
  - Pre-moderation: Reviews are automatically flagged based on their content before being stored.
  - Public Visibility: The public GET endpoint (/api/reviews/<game_title>) only returns reviews that have the status approved.

### API Endpoints and Integration
The service exposes two primary endpoints:
| Endpoint | Method	| Description | Example Request Body|
| :--- | :--- | :--- | :--- |
| /api/reviews/add | POST | Submits a new review; applies moderation check and sets status.	| {"user_id": 1, "game_title": "Elden Ring", "rating": 5, "comment": "Great game!"} |
| /api/reviews/<game_title> | GET | Retrieves all approved reviews for a specific game. | N/A | 

### Integration Example (Python Client):

```python
import requests

SERVICE_URL = "127.0.0.1"

# Example POST request to submit a review (will be approved)
review_data = {"user_id": 101, "game_title": "Elden Ring", "rating": 5, "comment": "A masterpiece."}
response = requests.post(f"{SERVICE_URL}/add", json=review_data)
print(f"Submission Status: {response.json()['status']}") # Output: approved

# Example GET request to retrieve approved reviews
response = requests.get(f"{SERVICE_URL}/Elden Ring")
print(f"Approved Reviews: {len(response.json())}")
```

### Installing Requirements for Recommendation Service:
   - Enter Git Bash, or another terminal of your choice, and navigate to the directory of this repo.
   - Enter 'pip install -r req_rec.txt' to install requirements.

## 2. The Recommendation Service
This service provides game recommendations based on content-based filtering (cosine similarity using TF-IDF vectors). The machine learning model is loaded into memory only once when the service starts up.
   - Port: 5004
   - Data Source: cleaned_games.csv
   - Key Files:
      - recommendation_service_app.py: Flask application that wraps the core logic in an API.
      - recommendation_service.py: The underlying class containing the pandas/sklearn logic.

### Implementation Details
The separation of this service allows the heavy processing power required to load the ML model and dataframes to be isolated from the main web application, improving frontend performance and scalability.

### API Endpoints and Integration
The service exposes one primary endpoint:

| Endpoint | Method	| Description | Example Request Body|
| :--- | :--- | :--- | :--- |
| /api/recommend | POST | Requests recommendations for a specific game title (AppID). | {"game_title": "Elden Ring"} |

### Integration Example (Python Client):
```python
    import requests

    SERVICE_URL = "127.0.0.1"

    # Example POST request to get recommendations for a specific game
    # Use a game title/AppID present in your 'cleaned_games.csv' file
    response = requests.post(SERVICE_URL, json={'game_title': 'Elden Ring'})

    if response.status_code == 200:
        recommendations = response.json()['recommendations']
        print(f"Recommendations found: {recommendations}")
    else:
        print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
```