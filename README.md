# Web Scraper with Streamlit Dashboard

This project is a Python-based web scraper that collects book data (title, price, rating, and genre) from [books.toscrape.com](http://books.toscrape.com) and visualizes it in an interactive Streamlit dashboard. It showcases skills in web scraping, data processing, and data visualization using popular Python libraries.

## Features
- **Web Scraping**: Scrapes book data ethically using `requests` and `BeautifulSoup`, with delays to respect server limits.
- **Data Processing**: Cleans and structures data using `pandas`, saving it to a CSV file.
- **Data Visualization**: Displays interactive charts (average price by genre, price vs. rating) and a table of top-rated books using `Streamlit` and `Plotly`.
- **Modular Code**: Organized into reusable classes and functions with error handling and logging.
- **Ethical Considerations**: Includes delays (1s per book, 2s per page) to avoid overloading the target server.

## Project Structure
├── book_scraper.py    # Web scraper script
├── dashboard.py       # Streamlit dashboard script
├── books_data.csv     # Output CSV file (generated after running scraper)
├── scraper.log        # Log file for scraping process
├── requirements.txt   # Project dependencies
└── README.md          # This file

## Prerequisites
- Python 3.8+
- Git

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Create a virtual environment (optional but recommended):
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
bashpip install -r requirements.txt


Usage
1. Run the Scraper:
bashpython book_scraper.py
This scrapes book data from the first 2 pages of books.toscrape.com and saves it to books_data.csv. Modify max_pages in book_scraper.py to scrape more pages.
2. Launch the Dashboard:
bashstreamlit run dashboard.py
This opens a browser with the interactive dashboard showing:
Bar chart of average book prices by genre.
Scatter plot of book prices vs. ratings.
Table of the top 10 highest-rated books.

Dependencies
See requirements.txt:
textrequests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
streamlit==1.25.0
plotly==5.15.0

Ethical Scraping

The scraper includes delays (1 second per book, 2 seconds per page) to respect the server's resources.
It adheres to the website's robots.txt (checked at http://books.toscrape.com/robots.txt).
For production use, always verify the target site's terms of service.

Challenges and Solutions
Challenge: Some book pages load dynamically.
Solution: Used BeautifulSoup for static content, as the target site does not require JavaScript rendering. For dynamic sites, selenium could be added.

Challenge: Missing or malformed data.
Solution: Implemented error handling in parse_book to skip invalid entries and log issues.

Challenge: Creating an engaging visualization.
Solution: Used Plotly for interactive charts and Streamlit for a user-friendly dashboard.

Future Improvements
Add a CLI with argparse to customize scraping parameters (e.g., number of pages).
Implement unit tests with pytest for robustness.
Deploy the dashboard to Streamlit Cloud or Heroku.
Add automation with schedule to run the scraper periodically.

Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements.

License
MIT License. See LICENSE for details.

Author
Hugo Perez - github.com/hpzalv
