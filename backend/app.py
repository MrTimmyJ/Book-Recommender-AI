from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import BookRecommender
import os

app = Flask(__name__)
CORS(app)

# Initialize the AI recommender
recommender = BookRecommender()

@app.route('/api/recommend', methods=['POST'])
def recommend_books():
    data = request.get_json()
    book_title = data.get('book', '').strip()
    
    if not book_title:
        return jsonify({"error": "Please enter a book title"}), 400
    
    print(f"📚 Recommendation request for: {book_title}")
    
    try:
        recommendations = recommender.get_recommendations(book_title)
        return jsonify(recommendations)
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": "Server error. Please try again."}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "AI Book Recommender",
        "version": "2.0.0"
    })

if __name__ == '__main__':
    print("🚀 AI Book Recommender Started!")
    print("📍 Endpoint: POST /api/recommend")
    app.run(debug=True, host='0.0.0.0', port=5000)