# Novel Discover - AI Book Recommender

A modern Flask application with AI-powered book recommendations using Google Books API.

**Author**: Timothy Johnson  
**Date**: January 2026

## 🌟 Overview

Novel Discover is an intelligent book recommendation system that uses AI-powered similarity analysis to suggest books based on your reading preferences. Unlike basic keyword matching, it analyzes themes, genres, and writing styles to provide curated recommendations.

## ✨ Features

### 🤖 AI-Powered Recommendations
- **Intelligent Similarity Analysis**: Goes beyond simple genre matching
- **Curated Categories**: Recommendations grouped into "Top Pick", "Similar Genre", and "New Vibe"
- **Multi-factor Matching**: Considers themes, writing style, and reader appeal

### 📚 Comprehensive Book Information
- **Rich Metadata**: Titles, authors, categories, ratings, and descriptions
- **Cover Images**: Display book covers with graceful fallbacks
- **Structured Presentation**: Clean, card-based interface for easy browsing

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Elements**: Real-time search with loading states
- **Visual Feedback**: Clear error handling and success indicators

### 🔌 Robust API Architecture
- **RESTful Endpoints**: Clean API design with JSON responses
- **CORS Support**: Ready for frontend integration
- **Health Monitoring**: Built-in service health checks

## 🏗️ Architecture

### Backend Structure

book-recommender/ <br>
├── backend/<br>
│   ├── app.py              # Main Flask application<br>
│   ├── recommender.py      # AI recommendation logic<br>
│   └── requirements.txt    # Python dependencies<br>
├── frontend/<br>
│   ├── index.html          # Main web interface<br>
│   ├── style.css           # CSS styles<br>
│   ├── index.css           # Additional CSS<br>
│   └── script.js           # JavaScript application<br>
└── README.md               # Documentation<br>


### API Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/recommend` | POST | Get AI-powered recommendations | `{"book": "Book Title"}` | JSON with recommendations |
| `/api/health` | GET | Service health check | None | Service status |
| `/` | GET | Web interface | None | HTML page |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:

    git clone https://github.com/MrTimmyJ/book-recommender.git
    cd book-recommender

2. Install dependencies:

    cd backend
    python3 -m venv venv
    source venv/bin/activate  # Mac/Linux
    # venv\Scripts\activate   # Windows
    
    pip install -r requirements.txt
    python app.py

🪪 License

© 2026 Timothy Johnson. All Rights Reserved.<br>
This project and its code may not be copied, modified, or reused without permission.
