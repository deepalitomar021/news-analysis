
# News Analysis Web Application

This is a Flask-based web application for analyzing news articles from the Times of India. The application allows users to submit news URLs, extract and analyze the news text, and view the analysis results. It also includes user authentication via Google OAuth and an admin login for viewing submission history.

## Live Demo 

Live Link

## Features

- **User Authentication**: Users can log in using their Google account.
- **News Text Extraction**: Extracts news text from Times of India articles.
- **Extracted Text Cleaning**: Removes html tags, links and other unnecessary data from the extracted text.
- **Text Analysis**: Analyzes the extracted news text for the number of sentences, words, stopwords, and part-of-speech tags.
- **Submission History**: Admin users can view the history of submitted news articles and their analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/deepalitomar021/news-analysis.git
   cd news-analysis
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database and update the connection details in `main.py`.

4. Run the Flask application:
   ```bash
   python main.py
   ```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Log in using your Google account.
3. Submit a news URL from the Times of India for analysis.
4. View the analysis results on the dashboard.
5. Admin users can log in to view the submission history.

## Project Structure

- `main.py`: The main Flask application file.
- `templates/`: Contains the HTML templates for the web pages.
- `static/`: Contains static files such as CSS and JavaScript.
- `requirements.txt`: Lists the required Python packages.

## Dependencies

- Flask
- Authlib
- Requests
- BeautifulSoup
- NLTK
- Psycopg2

