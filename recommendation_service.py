import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationService:
    def __init__(self, data_path='cleaned_games.csv'):
        # Ensure 'cleaned_games.csv' is accessible relative to where this class is instantiated (e.g., in the root dir)
        self.df = pd.read_csv(data_path)
        # Ensure features are treated as strings
        self.df['combined_features'] = self.df['combined_features'].astype(str)
        # Initialize the vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
        # Prepare the TFIDF matrix upon initialization
        self._prepare_engine()

    def _prepare_engine(self):
        # Fit and transform the combined features data
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])

    def get_recommendations(self, game_title, num_results=3):
        """
        Calculates cosine similarity-based recommendations for a given game title.

        Args:
            game_title (str): The AppID of the target game.
            num_results (int): The number of recommendations to return.

        Returns:
            list: A list of AppIDs (strings) that are recommended.
        """
        # Note: The original code used game_title which looks like an AppID based on the usage
        # 'AppID' is likely the unique identifier/title used in your CSV file.
        if game_title not in self.df['AppID'].values:
            return []

        # Get the index of the game that matches the input game_title (AppID)
        game_idx = self.df[self.df['AppID'] == game_title].index[0]

        # Calculate similarity ONLY between the target game and ALL other games
        target_game_vector = self.tfidf_matrix[game_idx:game_idx + 1]
        cosine_sim_scores = cosine_similarity(target_game_vector, self.tfidf_matrix).flatten()

        # Combine indices and scores into a list of tuples and sort
        sim_scores = list(enumerate(cosine_sim_scores))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sort by score (x[1])

        # Get the top N results, skipping index 0 (which is the game itself, having a score of 1.0)
        sim_scores = sim_scores[1:num_results + 1]
        game_indices = [i[0] for i in sim_scores]  # Extract only the index part (i[0])

        # Return the AppIDs/titles corresponding to those indices
        return self.df['AppID'].iloc[game_indices].tolist()
