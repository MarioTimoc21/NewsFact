# News Fact-Checker

## Project Goal

The goal of this project is to create a news fact-checking system that analyzes the credibility of news stories by comparing the content of articles and identifying similar articles from trusted sources. This tool will allow users to input a URL for a news article, and the system will extract relevant information, compare it with articles from various sources, and determine how credible the story is. 

Eventually, the project should include a robust filtering system, allowing it to evaluate the reliability of different news sources, leveraging both machine learning and trusted data sources like [MediaBias](https://mediabiasfactcheck.com/) and other external services.

## Requirements and Setup

To get started, make sure you have the following:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MarioTimoc21/NewsFact.git
   cd NewsFact
   ```

2. **Set up environment variables**:

   Create a `.env` file in the directory of the project and add the following keys:

   ```ini
   NEWSAPI_KEY=your_newsapi_key
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_google_custom_search_engine_id
   ```

   * Get a NewsAPI key by signing up at [NewsAPI](https://newsapi.org/).
   * Get a Google API key and Custom Search Engine ID from [Google Custom Search](https://developers.google.com/custom-search/v1/overview).

3. **Install Dependencies**:

   In order to run this project, you need to install the necessary Python dependencies. You can do this by creating a requirements.txt file.
   
   To create the requirements.txt file manually, use the following:

   ```txt
   fastapi
   requests
   beautifulsoup4
   readability-lxml
   langdetect
   nltk
   spacy
   python-dotenv
   uvicorn
   ```

   After creating the requirements.txt file, install the dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the dependencies needed to run the project.

4. **Run the application**:

   Once the dependencies are installed, you can run the FastAPI server with the following command:

   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API Documentation**:

   Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive API documentation.

## Contributing

The project is a work in progress, and new functionalities, improvements, and ideas are always welcome! If you have any ideas or suggestions, feel free to open a pull request or issue.

Whether you want to add new features, improve the accuracy of the fact-checking algorithm, or enhance the news source credibility evaluation, your contribution is greatly appreciated!

Steps to Contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes.
4. Commit and push your changes.
5. Open a pull request to the main branch.

We look forward to your contributions!
