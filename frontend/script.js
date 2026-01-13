class BookRecommender {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const recommendBtn = document.getElementById('recommendBtn');
        const bookInput = document.getElementById('bookInput');
        const tryAnotherBtn = document.getElementById('tryAnotherBtn');

        recommendBtn.addEventListener('click', () => this.getRecommendations());
        bookInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.getRecommendations();
            }
        });
        
        if (tryAnotherBtn) {
            tryAnotherBtn.addEventListener('click', () => this.resetSearch());
        }
    }

    async getRecommendations() {
        const bookTitle = document.getElementById('bookInput').value.trim();
        
        if (!bookTitle) {
            this.showError('Please enter a book title');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch(`${this.apiBase}/recommend`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ book: bookTitle })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to get recommendations');
            }

            if (data.error) {
                throw new Error(data.error);
            }

            this.displayResults(data);
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    displayResults(data) {
        // Display user's book
        document.getElementById('userBookTitle').textContent = data.user_book.title;
        document.getElementById('userBookAuthor').textContent = `by ${data.user_book.authors?.join(', ') || 'Unknown Author'}`;
        document.getElementById('userBookDescription').textContent = 
            data.user_book.description || 'No description available';

        // Display recommendations
        this.displayBook('topPick', data.recommendations.top_pick);
        this.displayBook('sameGenre', data.recommendations.same_genre_different_style);
        this.displayBook('diffVibe', data.recommendations.different_genre_same_vibes);

        this.showResults();
    }

    displayBook(prefix, book) {
        // Title and author
        document.getElementById(`${prefix}Title`).textContent = book.title;
        document.getElementById(`${prefix}Author`).textContent = `by ${book.authors?.join(', ') || 'Unknown Author'}`;

        // Image and placeholder
        const imageElement = document.getElementById(`${prefix}Image`);
        const placeholderElement = document.getElementById(`${prefix}Placeholder`);
        
        if (book.image) {
            imageElement.src = book.image;
            imageElement.style.display = 'block';
            if (placeholderElement) placeholderElement.style.display = 'none';
        } else {
            imageElement.style.display = 'none';
            if (placeholderElement) placeholderElement.style.display = 'flex';
        }

        // Rating
        const ratingElement = document.getElementById(`${prefix}Rating`);
        if (book.averageRating) {
            ratingElement.innerHTML = `<i class="fas fa-star"></i> ${book.averageRating}/5`;
            ratingElement.style.display = 'inline-flex';
        } else {
            ratingElement.style.display = 'none';
        }

        // Genre
        const genreElement = document.getElementById(`${prefix}Genre`);
        if (book.categories && book.categories.length > 0) {
            genreElement.textContent = book.categories[0];
            genreElement.style.display = 'inline-block';
        } else {
            genreElement.style.display = 'none';
        }

        // Description
        document.getElementById(`${prefix}Description`).textContent = 
            book.description || 'No description available';
    }

    resetSearch() {
        document.getElementById('bookInput').value = '';
        document.getElementById('bookInput').focus();
        this.hideResults();
        this.hideError();
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('recommendBtn').disabled = true;
        document.getElementById('recommendBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Searching...</span>';
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('recommendBtn').disabled = false;
        document.getElementById('recommendBtn').innerHTML = '<i class="fas fa-magic"></i><span>Find Similar</span>';
    }

    showError(message) {
        const errorElement = document.getElementById('error');
        document.getElementById('errorMessage').textContent = message;
        errorElement.classList.remove('hidden');
    }

    hideError() {
        document.getElementById('error').classList.add('hidden');
    }

    showResults() {
        document.getElementById('results').classList.remove('hidden');
    }

    hideResults() {
        document.getElementById('results').classList.add('hidden');
    }
}

// Initialize the app when page loads
document.addEventListener('DOMContentLoaded', () => {
    new BookRecommender();
});