import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import re

class BookRecommender:
    def __init__(self):
        print("🚀 Initializing Real AI Book Recommender...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ AI Model Ready")
    
    def search_google_books(self, query, max_results=10):
        """Search Google Books API"""
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            'q': query,
            'maxResults': max_results,
            'orderBy': 'relevance'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return data.get('items', [])
        except Exception as e:
            print(f"❌ API Error: {e}")
            return []
    
    # def get_smart_recommendations(self, user_book_title):
    #     """Main AI recommendation engine"""
    #     print(f"🎯 Smart search for: {user_book_title}")
        
    #     # Step 1: Understand the user's book
    #     user_books = self.search_google_books(user_book_title, 3)
    #     if not user_books:
    #         return {"error": "❌ Book not found. Try a more specific title."}
        
    #     user_book = self.extract_book_info(user_books[0])
        
    #     # Step 2: Multiple search strategies
    #     all_candidates = []
        
    #     # Strategy 1: Same author
    #     if user_book['authors'] and user_book['authors'][0] != 'Unknown':
    #         author_books = self.search_google_books(f"inauthor:{user_book['authors'][0]}", 6)
    #         all_candidates.extend(author_books)
        
    #     # Strategy 2: Similar books by embedding
    #     user_text = f"{user_book['title']} {user_book['description']}"
    #     user_embedding = self.model.encode([user_text])[0]
        
    #     # Search for books in same categories
    #     if user_book['categories']:
    #         for category in user_book['categories'][:2]:
    #             category_books = self.search_google_books(f"subject:{category}", 8)
    #             all_candidates.extend(category_books)
        
    #     # Strategy 3: General fiction search as fallback
    #     general_books = self.search_google_books("fiction bestsellers", 10)
    #     all_candidates.extend(general_books)
        
    #     # Step 3: Process and rank candidates
    #     unique_books = self.remove_duplicates(all_candidates)
    #     filtered_books = [book for book in unique_books 
    #                      if book.get('volumeInfo', {}).get('title', '').lower() != user_book_title.lower()]
        
    #     # Step 4: AI-powered ranking
    #     ranked_books = self.rank_books_by_relevance(user_embedding, filtered_books)
        
    #     return ranked_books[:6]

    # def get_smart_recommendations(self, user_book_title):
    #     """Main AI recommendation engine - FIXED VERSION"""
    #     print(f"🎯 Smart search for: {user_book_title}")
        
    #     # Step 1: Get user's book to understand it
    #     user_books = self.search_google_books(user_book_title, 2)
    #     if not user_books:
    #         return {"error": "❌ Book not found. Try a more specific title."}
        
    #     user_book = self.extract_book_info(user_books[0])
    #     print(f"📖 Found user book: {user_book['title']} by {user_book['authors'][0]}")
        
    #     # Step 2: Get popular books in similar genres (NOT about the same book)
    #     all_candidates = []
        
    #     # Common similar book mappings (manual but effective)
    #     similar_books_map = {
    #         "harry potter": ["Percy Jackson", "Artemis Fowl", "The Chronicles of Narnia", "His Dark Materials", "The Magicians"],
    #         "the hobbit": ["The Lord of the Rings", "The Chronicles of Narnia", "Eragon", "The Wheel of Time", "Game of Thrones"],
    #         "dune": ["Foundation", "The Left Hand of Darkness", "Hyperion", "The Martian", "Ender's Game"],
    #         "gone girl": ["The Girl on the Train", "The Silent Patient", "Sharp Objects", "The Woman in the Window", "Big Little Lies"],
    #         "the hunger games": ["Divergent", "The Maze Runner", "Red Rising", "The Giver", "Battle Royale"]
    #     }
        
    #     # Try to find similar books from our mapping first
    #     user_book_lower = user_book_title.lower()
    #     found_similar = False
        
    #     for key, similar_titles in similar_books_map.items():
    #         if key in user_book_lower:
    #             print(f"🔍 Using similarity mapping for: {key}")
    #             for similar_title in similar_titles:
    #                 similar_books = self.search_google_books(similar_title, 3)
    #                 all_candidates.extend(similar_books)
    #             found_similar = True
    #             break
        
    #     # If no mapping found, search by genre
    #     if not found_similar and user_book['categories']:
    #         print(f"🔍 Searching by genre: {user_book['categories'][0]}")
    #         # Search for popular books in the same genre
    #         genre_books = self.search_google_books(f"subject:{user_book['categories'][0]} fiction", 15)
    #         all_candidates.extend(genre_books)
        
    #     # Always add some general popular fiction as fallback
    #     popular_books = self.search_google_books("bestselling fiction", 10)
    #     all_candidates.extend(popular_books)
        
    #     # Step 3: Filter out bad results
    #     filtered_books = []
    #     seen_titles = set()
        
    #     for book in all_candidates:
    #         book_info = self.extract_book_info(book)
    #         title_lower = book_info['title'].lower()
            
    #         # Skip if it's the same book or about the same book
    #         if (title_lower == user_book_lower or 
    #             user_book['authors'][0].lower() in title_lower or
    #             user_book_lower in title_lower):
    #             continue
                
    #         # Skip educational/analysis books
    #         if any(keyword in title_lower for keyword in ['study guide', 'analysis', 'companion', 'conversations with', 'history of']):
    #             continue
                
    #         # Skip if we've seen it
    #         if book_info['title'] not in seen_titles:
    #             filtered_books.append(book_info)
    #             seen_titles.add(book_info['title'])
        
    #     print(f"✅ Filtered to {len(filtered_books)} good recommendations")
        
    #     # Step 4: Use AI to rank the good candidates
    #     if len(filtered_books) > 1:
    #         user_text = f"{user_book['title']} {user_book['description']}"
    #         user_embedding = self.model.encode([user_text])[0]
            
    #         scored_books = []
    #         for book in filtered_books:
    #             book_text = f"{book['title']} {book['description']}"
    #             book_embedding = self.model.encode([book_text])[0]
                
    #             similarity = np.dot(user_embedding, book_embedding) / (
    #                 np.linalg.norm(user_embedding) * np.linalg.norm(book_embedding)
    #             )
                
    #             # Boost popular/highly rated books
    #             rating_boost = book.get('averageRating', 0) / 5.0
    #             total_score = (0.7 * similarity) + (0.3 * rating_boost)
                
    #             scored_books.append((book, total_score))
            
    #         scored_books.sort(key=lambda x: x[1], reverse=True)
    #         return [book for book, score in scored_books]
        
    #     return filtered_books

    # def get_smart_recommendations(self, user_book_title):
    #     """REAL AI recommendation engine - works for ANY book"""
    #     print(f"🎯 AI search for: {user_book_title}")
        
    #     # Step 1: Get user's book with author for better context
    #     search_query = user_book_title
    #     user_books = self.search_google_books(search_query, 3)
        
    #     if not user_books:
    #         return {"error": "❌ Book not found. Try 'Title by Author' format."}
        
    #     user_book = self.extract_book_info(user_books[0])
    #     print(f"📖 Found: '{user_book['title']}' by {user_book['authors'][0]}")
        
    #     # Step 2: Use AI to understand the book's essence
    #     user_book_analysis = self.analyze_book_content(user_book)
    #     print(f"🔍 AI Analysis: {user_book_analysis['primary_genre']} book, {user_book_analysis['mood']} mood")
        
    #     # Step 3: Smart search strategies based on AI analysis
    #     all_candidates = []
        
    #     # Strategy 1: Search by similar themes/mood
    #     theme_query = f"{user_book_analysis['primary_genre']} {user_book_analysis['mood']} fiction"
    #     theme_books = self.search_google_books(theme_query, 12)
    #     all_candidates.extend(theme_books)
        
    #     # Strategy 2: Search by same author's other works
    #     if user_book['authors'][0] != 'Unknown':
    #         author_books = self.search_google_books(f"inauthor:{user_book['authors'][0]}", 8)
    #         all_candidates.extend(author_books)
        
    #     # Strategy 3: Search popular books in the same genre
    #     if user_book_analysis['primary_genre']:
    #         genre_books = self.search_google_books(f"subject:{user_book_analysis['primary_genre']}", 10)
    #         all_candidates.extend(genre_books)
        
    #     # Strategy 4: Search award-winning books in similar categories
    #     award_query = f"award winning {user_book_analysis['primary_genre']} fiction"
    #     award_books = self.search_google_books(award_query, 8)
    #     all_candidates.extend(award_books)
        
    #     # Step 4: AI-Powered Filtering & Ranking
    #     good_recommendations = self.ai_filter_and_rank(user_book, user_book_analysis, all_candidates)
        
    #     print(f"✅ AI found {len(good_recommendations)} quality recommendations")
    #     return good_recommendations

    # def get_smart_recommendations(self, user_book_title):
    #     """PURE AI recommendation engine - NO AUTHOR SEARCH"""
    #     print(f"🎯 AI search for: {user_book_title}")
        
    #     # Step 1: Get user's book
    #     user_books = self.search_google_books(user_book_title, 3)
    #     if not user_books:
    #         return {"error": "❌ Book not found. Try 'Title by Author' format."}
        
    #     user_book = self.extract_book_info(user_books[0])
    #     print(f"📖 Found: '{user_book['title']}' by {user_book['authors'][0]}")
        
    #     # Step 2: Use AI to understand the book
    #     user_book_analysis = self.analyze_book_content(user_book)
    #     print(f"🔍 AI Analysis: {user_book_analysis['primary_genre']} book, {user_book_analysis['mood']} mood")
        
    #     # Step 3: Smart search strategies (NO AUTHOR SEARCH)
    #     all_candidates = []
        
    #     # Strategy 1: Search by similar themes/mood
    #     theme_query = f"{user_book_analysis['primary_genre']} {user_book_analysis['mood']} fiction"
    #     theme_books = self.search_google_books(theme_query, 20)
    #     all_candidates.extend(theme_books)
        
    #     # Strategy 2: Search popular books in the same genre
    #     if user_book_analysis['primary_genre']:
    #         genre_books = self.search_google_books(f"subject:{user_book_analysis['primary_genre']}", 15)
    #         all_candidates.extend(genre_books)
        
    #     # Strategy 3: Search award-winning books
    #     award_query = f"award winning {user_book_analysis['primary_genre']} fiction"
    #     award_books = self.search_google_books(award_query, 10)
    #     all_candidates.extend(award_books)
        
    #     # Step 4: AI-Powered Filtering & Ranking
    #     good_recommendations = self.ai_filter_and_rank(user_book, user_book_analysis, all_candidates)
        
    #     print(f"✅ AI found {len(good_recommendations)} quality recommendations")
    #     return good_recommendations

    def get_smart_recommendations(self, user_book_title):
        """SMART AI recommendation engine - KEEP author search but filter series"""
        print(f"🎯 AI search for: {user_book_title}")
        
        # Step 1: Get user's book
        user_books = self.search_google_books(user_book_title, 3)
        if not user_books:
            return {"error": "❌ Book not found. Try 'Title by Author' format."}
        
        user_book = self.extract_book_info(user_books[0])
        print(f"📖 Found: '{user_book['title']}' by {user_book['authors'][0]}")
        
        # Step 2: Use AI to understand the book
        user_book_analysis = self.analyze_book_content(user_book)
        print(f"🔍 AI Analysis: {user_book_analysis['primary_genre']} book, {user_book_analysis['mood']} mood")
        
        # Step 3: Smart search strategies
        all_candidates = []
        
        # Strategy 1: Search by similar themes/mood
        theme_query = f"{user_book_analysis['primary_genre']} {user_book_analysis['mood']} fiction"
        theme_books = self.search_google_books(theme_query, 20)
        all_candidates.extend(theme_books)
        
        # Strategy 2: Search by same author's OTHER WORKS (SMART FILTERED)
        if user_book['authors'][0] != 'Unknown':
            author_books = self.search_google_books(f"inauthor:{user_book['authors'][0]}", 12)
            
            # SMART FILTER: Only keep books that are DIFFERENT stories
            filtered_author_books = []
            for book in author_books:
                book_info = self.extract_book_info(book)
                
                # Use AI to check if it's a DIFFERENT story (not same series)
                if self.is_different_story(user_book, book_info):
                    filtered_author_books.append(book)
            
            print(f"📚 Author filter: {len(author_books)} → {len(filtered_author_books)} different stories")
            all_candidates.extend(filtered_author_books)
        
        # Strategy 3: Search popular books in the same genre
        if user_book_analysis['primary_genre']:
            genre_books = self.search_google_books(f"subject:{user_book_analysis['primary_genre']}", 15)
            all_candidates.extend(genre_books)
        
        # Strategy 4: Search award-winning books
        award_query = f"award winning {user_book_analysis['primary_genre']} fiction"
        award_books = self.search_google_books(award_query, 10)
        all_candidates.extend(award_books)
        
        # Step 4: AI-Powered Filtering & Ranking
        good_recommendations = self.ai_filter_and_rank(user_book, user_book_analysis, all_candidates)
        
        print(f"✅ AI found {len(good_recommendations)} quality recommendations")
        return good_recommendations

    def is_different_story(self, user_book, candidate_book):
        """Use AI + title analysis to detect DIFFERENT stories vs SAME series"""
        user_title = user_book['title'].lower()
        candidate_title = candidate_book['title'].lower()
        
        # Quick checks for obvious same series
        if self.obviously_same_series(user_title, candidate_title):
            return False
        
        # Use AI to check content similarity
        user_desc = user_book['description'] or user_title
        candidate_desc = candidate_book['description'] or candidate_title
        
        user_embedding = self.model.encode([user_desc])[0]
        candidate_embedding = self.model.encode([candidate_desc])[0]
        
        similarity = np.dot(user_embedding, candidate_embedding) / (
            np.linalg.norm(user_embedding) * np.linalg.norm(candidate_embedding)
        )
        
        # If descriptions are very similar (>75%), probably same series
        return similarity < 0.75

    def obviously_same_series(self, title1, title2):
        """Quick detection for obvious same-series books"""
        # Remove common words and compare remaining words
        common_words = {'the', 'and', 'of', 'a', 'in', 'to'}
        words1 = set(title1.split()) - common_words
        words2 = set(title2.split()) - common_words
        
        # Count matching significant words (length > 3)
        significant_matches = len([word for word in words1 & words2 if len(word) > 3])
        
        # If 2+ significant words match, probably same series
        if significant_matches >= 2:
            return True
        
        # Check for numbered series indicators
        series_indicators = [
            ('book', 'book'), ('volume', 'volume'), ('part', 'part'),
            ('#1', '#2'), ('i', 'ii'), ('1', '2')
        ]
        
        for indicator1, indicator2 in series_indicators:
            if indicator1 in title1 and indicator2 in title2:
                return True
        
        return False

    def analyze_book_content(self, book):
        """Use AI to understand what the book is REALLY about"""
        title = book['title']
        description = book['description']
        categories = book['categories']
        
        analysis_text = f"{title} {description}"
        
        # Genre detection
        genre_scores = {}
        genre_keywords = {
            'fantasy': ['magic', 'dragon', 'wizard', 'kingdom', 'quest', 'elf', 'mythical'],
            'science fiction': ['space', 'alien', 'future', 'technology', 'spaceship', 'robot', 'dystopian'],
            'mystery': ['detective', 'murder', 'clue', 'crime', 'investigation', 'suspect'],
            'thriller': ['suspense', 'danger', 'chase', 'conspiracy', 'action', 'tense'],
            'horror': ['scary', 'ghost', 'supernatural', 'fear', 'dark', 'haunted', 'terror'],
            'romance': ['love', 'relationship', 'passion', 'marriage', 'heart', 'dating'],
            'historical': ['history', 'past', 'ancient', 'war', 'period', 'century'],
            'young adult': ['teen', 'young adult', 'coming of age', 'school', 'first love']
        }
        
        analysis_lower = analysis_text.lower()
        for genre, keywords in genre_keywords.items():
            score = sum(1 for keyword in keywords if keyword in analysis_lower)
            genre_scores[genre] = score
        
        # Mood detection
        mood_keywords = {
            'dark': ['dark', 'gritty', 'violent', 'bleak', 'horror', 'terror', 'fear'],
            'adventure': ['adventure', 'quest', 'journey', 'expedition', 'action', 'chase'],
            'mysterious': ['mystery', 'secret', 'puzzle', 'enigma', 'clue', 'investigation'],
            'emotional': ['love', 'heart', 'passion', 'relationship', 'family', 'friendship'],
            'epic': ['epic', 'kingdom', 'battle', 'war', 'legend', 'destiny']
        }
        
        mood_scores = {}
        for mood, keywords in mood_keywords.items():
            score = sum(1 for keyword in keywords if keyword in analysis_lower)
            mood_scores[mood] = score
        
        primary_genre = max(genre_scores, key=genre_scores.get) if genre_scores else 'fiction'
        primary_mood = max(mood_scores, key=mood_scores.get) if mood_scores else 'adventure'
        
        return {
            'primary_genre': primary_genre,
            'mood': primary_mood,
            'embedding': self.model.encode([analysis_text])[0]
        }

    def ai_filter_and_rank(self, user_book, user_analysis, candidate_books):
        """AI-powered filtering and ranking of recommendations"""
        filtered_books = []
        seen_titles = set()
        
        user_title_lower = user_book['title'].lower()
        user_author_lower = user_book['authors'][0].lower() if user_book['authors'][0] != 'Unknown' else ""
        
        for book_item in candidate_books:
            book_info = self.extract_book_info(book_item)
            title_lower = book_info['title'].lower()
            
            # Skip if it's the same book
            if title_lower == user_title_lower:
                continue
                
            # Skip books ABOUT the same book/author
            if (user_author_lower and user_author_lower in title_lower and 
                any(keyword in title_lower for keyword in ['companion', 'guide', 'analysis', 'conversations'])):
                continue
                
            # Skip educational/academic books
            skip_keywords = ['study guide', 'textbook', 'academic', 'companion', 'analysis', 'criticism']
            if any(keyword in title_lower for keyword in skip_keywords):
                continue
                
            # Skip if no description (usually not good books)
            if not book_info.get('description'):
                continue
                
            # Skip if we've seen it
            if book_info['title'] not in seen_titles:
                filtered_books.append(book_info)
                seen_titles.add(book_info['title'])
        
        # AI Ranking: Use multiple factors
        if len(filtered_books) > 1:
            scored_books = []
            
            for book in filtered_books:
                # Factor 1: Content similarity (AI embeddings)
                book_analysis = self.analyze_book_content(book)
                content_similarity = np.dot(user_analysis['embedding'], book_analysis['embedding']) / (
                    np.linalg.norm(user_analysis['embedding']) * np.linalg.norm(book_analysis['embedding'])
                )
                
                # Factor 2: Genre match
                genre_match = 1.0 if book_analysis['primary_genre'] == user_analysis['primary_genre'] else 0.3
                
                # Factor 3: Book quality (ratings)
                quality_score = book.get('averageRating', 3) / 5.0
                
                # Factor 4: Popularity (more ratings = more popular)
                popularity_score = min(book.get('ratingsCount', 0) / 1000, 1.0)
                
                # Combined score
                total_score = (
                    0.5 * content_similarity +      # Content match (most important)
                    0.2 * genre_match +            # Genre similarity
                    0.2 * quality_score +          # Book quality
                    0.1 * popularity_score         # Popularity
                )
                
                scored_books.append((book, total_score))
            
            # Sort by AI-calculated score
            scored_books.sort(key=lambda x: x[1], reverse=True)
            return [book for book, score in scored_books]
        
        return filtered_books
    
    def rank_books_by_relevance(self, user_embedding, candidate_books):
        """Rank books by AI similarity"""
        scored_books = []
        
        for book_item in candidate_books:
            book_info = self.extract_book_info(book_item)
            
            # Skip if missing critical info
            if not book_info.get('description') or book_info['title'] == 'Unknown':
                continue
            
            # Calculate similarity
            book_text = f"{book_info['title']} {book_info['description']}"
            book_embedding = self.model.encode([book_text])[0]
            
            similarity = np.dot(user_embedding, book_embedding) / (
                np.linalg.norm(user_embedding) * np.linalg.norm(book_embedding)
            )
            
            # Boost score for highly rated books
            rating_boost = book_info.get('averageRating', 0) / 5.0
            
            total_score = (0.7 * similarity) + (0.3 * rating_boost)
            
            scored_books.append((book_info, total_score))
        
        # Sort by total score
        scored_books.sort(key=lambda x: x[1], reverse=True)
        return [book for book, score in scored_books]
    
    def remove_duplicates(self, books):
        """Remove duplicate books by title"""
        seen_titles = set()
        unique_books = []
        
        for book in books:
            title = book.get('volumeInfo', {}).get('title', '')
            if title and title not in seen_titles:
                unique_books.append(book)
                seen_titles.add(title)
        
        return unique_books
    
    def extract_book_info(self, book_item):
        """Extract clean book information"""
        volume_info = book_item.get('volumeInfo', {})
        
        # Clean description
        description = volume_info.get('description', '')
        if description:
            description = re.sub('<[^<]+?>', '', description)
            description = description[:200] + '...' if len(description) > 200 else description
        
        return {
            'title': volume_info.get('title', 'Unknown'),
            'authors': volume_info.get('authors', ['Unknown']),
            'description': description,
            'categories': volume_info.get('categories', []),
            'image': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'averageRating': volume_info.get('averageRating', 0),
            'ratingsCount': volume_info.get('ratingsCount', 0),
            'pageCount': volume_info.get('pageCount', 0),
            'publishedDate': volume_info.get('publishedDate', '')[:4]
        }
    
    def get_recommendations(self, user_book_title):
        """Public method to get recommendations"""
        similar_books = self.get_smart_recommendations(user_book_title)
        
        if isinstance(similar_books, dict) and 'error' in similar_books:
            return similar_books
        
        if len(similar_books) < 3:
            return {"error": "Not enough quality recommendations. Try another book!"}
        
        # Get user book info
        user_books = self.search_google_books(user_book_title, 1)
        user_book_info = self.extract_book_info(user_books[0]) if user_books else {"title": user_book_title}
        
        return {
            "user_book": user_book_info,
            "recommendations": {
                "top_pick": similar_books[0],
                "same_genre_different_style": similar_books[2],
                "different_genre_same_vibes": similar_books[4] if len(similar_books) > 4 else similar_books[1]
            }
        }