import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import List, Dict
import re
import os

# Configure logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scraper.log'
)

class BookScraper:
    """A class to scrape book data from books.toscrape.com and save it to a CSV file."""
    
    def __init__(self, base_url: str = "http://books.toscrape.com"):
        """Initialize the scraper with the base URL and headers."""
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.books_data: List[Dict] = []

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch a webpage and return its parsed content.

        Args:
            url (str): The URL of the page to fetch.

        Returns:
            BeautifulSoup: Parsed HTML content of the page, or None if the request fails.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad status codes
            logging.info(f"Successfully fetched {url}")
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_book(self, book: BeautifulSoup) -> Dict:
        """Parse individual book data from a book HTML element.

        Args:
            book (BeautifulSoup): The HTML element containing book data.

        Returns:
            Dict: Dictionary with title, price, rating, and genre (if available).
        """
        try:
            title = book.find('h3').find('a')['title'].strip()
            price = book.find('p', class_='price_color').text.strip()
            # Convert price to float, removing currency symbol
            price = float(re.sub(r'[^\d.]', '', price))
            # Convert rating from class name (e.g., 'star-rating Three') to numeric
            rating_class = book.find('p', class_='star-rating')['class']
            rating = next((r for r in rating_class if r != 'star-rating'), None)
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_map.get(rating, 0)
            # Genre not directly available on main page; set as None for now
            return {'title': title, 'price': price, 'rating': rating, 'genre': None}
        except (AttributeError, KeyError) as e:
            logging.warning(f"Error parsing book data: {e}")
            return None

    def get_genre(self, book_url: str) -> str:
        """Fetch the genre of a book from its detail page.

        Args:
            book_url (str): The URL of the book's detail page.

        Returns:
            str: The genre of the book, or None if not found.
        """
        soup = self.fetch_page(book_url)
        if soup:
            try:
                # Genre is in breadcrumb navigation
                breadcrumb = soup.find('ul', class_='breadcrumb')
                genre = breadcrumb.find_all('li')[-2].text.strip()  # Second-to-last item is genre
                return genre
            except AttributeError:
                logging.warning(f"Genre not found for {book_url}")
        return None

    def scrape_page(self, page_num: int) -> None:
        """Scrape book data from a single page.

        Args:
            page_num (int): The page number to scrape.
        """
        url = f"{self.base_url}/catalogue/page-{page_num}.html"
        soup = self.fetch_page(url)
        if not soup:
            return

        books = soup.find_all('article', class_='product_pod')
        for book in books:
            book_data = self.parse_book(book)
            if book_data:
                # Fetch genre from book detail page
                book_link = book.find('h3').find('a')['href']
                book_url = f"{self.base_url}/catalogue/{book_link}"
                book_data['genre'] = self.get_genre(book_url)
                self.books_data.append(book_data)
                logging.info(f"Scraped book: {book_data['title']}")
            time.sleep(1)  # Delay to avoid overwhelming the server

    def scrape(self, max_pages: int = 2) -> None:
        """Scrape book data from multiple pages.

        Args:
            max_pages (int): Maximum number of pages to scrape.
        """
        logging.info(f"Starting scrape for {max_pages} pages")
        for page in range(1, max_pages + 1):
            self.scrape_page(page)
            time.sleep(2)  # Delay between pages for ethical scraping
        logging.info(f"Scraped {len(self.books_data)} books")

    def save_to_csv(self, filename: str = "books_data.csv") -> None:
        """Save scraped data to a CSV file.

        Args:
            filename (str): The name of the CSV file to save.
        """
        if not self.books_data:
            logging.warning("No data to save")
            return

        df = pd.DataFrame(self.books_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        logging.info(f"Data saved to {filename}")

def main():
    """Main function to run the scraper."""
    scraper = BookScraper()
    scraper.scrape(max_pages=2)  # Scrape 2 pages for demo purposes
    scraper.save_to_csv("books_data.csv")

if __name__ == "__main__":
    main()
