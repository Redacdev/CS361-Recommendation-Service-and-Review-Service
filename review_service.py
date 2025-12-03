from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

# --- Service Configuration ---
review_app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
review_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'reviews.db')
review_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
review_db = SQLAlchemy(review_app)

# A simple list for demonstration purposes
BAD_WORDS = {}

def check_for_profanity(text):
    """Checks if the text contains any words from the BAD_WORDS set."""
    words = text.lower().split()
    return any(word in BAD_WORDS for word in words)

# --- Service Model ---
class Review(review_db.Model):
    id = review_db.Column(review_db.Integer, primary_key=True)
    user_id = review_db.Column(review_db.Integer, nullable=False)
    game_title = review_db.Column(review_db.String(100), nullable=False)
    rating = review_db.Column(review_db.Integer, nullable=False) # 1 to 5 stars
    comment = review_db.Column(review_db.Text, nullable=False)
    timestamp = review_db.Column(review_db.DateTime, default=datetime.datetime.utcnow)
    # New column for moderation status: 'pending', 'approved', 'rejected'
    status = review_db.Column(review_db.String(20), default='pending', nullable=False)

    def to_dict(self):
        """Converts the Review object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'game_title': self.game_title,
            'rating': self.rating,
            'comment': self.comment,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }

# --- Service API Endpoints ---

@review_app.route('/api/reviews/add', methods=['POST'])
def add_review():
    """Adds a new review to the database, applying a moderation check."""
    data = request.get_json()
    required_fields = ['user_id', 'game_title', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing data. Required fields are: user_id, game_title, rating, or comment.")

    # Determine the status based on content
    review_status = 'approved' # Default to approved
    if check_for_profanity(data['comment']):
        review_status = 'rejected'
        print(f"Review rejected due to inappropriate content: '{data['comment']}'")

    new_review = Review(
        user_id=data['user_id'],
        game_title=data['game_title'],
        rating=data['rating'],
        comment=data['comment'],
        status=review_status # Use the determined status
    )
    review_db.session.add(new_review)
    review_db.session.commit()

    message = "Review submitted successfully and is approved." if review_status == 'approved' else "Review submitted but was rejected due to content policy."
    return jsonify({'message': message, 'id': new_review.id, 'status': review_status}), 201

@review_app.route('/api/reviews/<game_title>', methods=['GET'])
def get_reviews(game_title):
    """Retrieves only *approved* reviews for a specific game title."""
    reviews = Review.query.filter_by(game_title=game_title, status='approved').order_by(Review.timestamp.desc()).all()
    # If an admin route is needed later, they could view all statuses, but public API only shows 'approved'
    return jsonify([review.to_dict() for review in reviews]), 200

def init_review_db():
    """Ensures the database and tables are created when the app starts."""
    with review_app.app_context():
        # WARNING: If you are running this after the previous code,
        # you need to delete the old 'reviews.db' file first for the new column 'status' to be added.
        review_db.create_all()

if __name__ == '__main__':
    init_review_db()
    review_app.run(port=5002, debug=True)
