import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, unquote
import time
import logging
from pathlib import Path

class CatImageScraper:
    def __init__(self, output_dir="cat_images"):
        """Initialize the scraper with an output directory."""
        self.output_dir = output_dir
        self.setup_logging()
        self.setup_directory()
        
        # Use a responsible user agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Educational-Bot; +http://example.com)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_directory(self):
        """Create output directory if it doesn't exist."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def download_image(self, img_url, filename):
        """Download an image from a URL."""
        try:
            response = requests.get(img_url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            # Check if the response is actually an image
            if 'image' in response.headers.get('content-type', ''):
                file_path = os.path.join(self.output_dir, filename)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.logger.info(f"Successfully downloaded: {filename}")
                return True
            else:
                self.logger.warning(f"URL {img_url} is not an image")
                return False
                
        except Exception as e:
            self.logger.error(f"Error downloading {img_url}: {str(e)}")
            return False

    def get_image_urls_from_wikimedia(self, url):
        """Extract image URLs from Wikimedia Commons category page."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the gallery div that contains the images
            gallery = soup.find('div', class_='mw-category')
            if not gallery:
                self.logger.error("Could not find gallery section")
                return []
            
            # Find all links to file pages
            image_links = []
            for link in gallery.find_all('a'):
                if 'File:' in link.get('href', ''):
                    image_links.append('https://commons.wikimedia.org' + link['href'])
            
            return image_links
            
        except Exception as e:
            self.logger.error(f"Error getting image links: {str(e)}")
            return []

    def get_full_resolution_url(self, file_page_url):
        """Get the full resolution image URL from a Wikimedia Commons file page."""
        try:
            response = requests.get(file_page_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the full resolution image link
            full_res_div = soup.find('div', class_='fullImageLink')
            if full_res_div and full_res_div.find('a'):
                return 'https:' + full_res_div.find('a')['href']
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting full resolution URL: {str(e)}")
            return None

    def scrape_wikimedia_commons(self, category_url):
        """Scrape cat images from Wikimedia Commons category page."""
        try:
            # Get all image page URLs from the category
            image_pages = self.get_image_urls_from_wikimedia(category_url)
            self.logger.info(f"Found {len(image_pages)} image pages")
            
            downloaded_count = 0
            for idx, page_url in enumerate(image_pages):
                # Get the full resolution image URL
                full_res_url = self.get_full_resolution_url(page_url)
                if not full_res_url:
                    continue
                
                # Generate filename from the URL
                filename = f"cat_{idx}_{int(time.time())}.jpg"
                
                # Download the image
                if self.download_image(full_res_url, filename):
                    downloaded_count += 1
                
                # Be nice to the server
                time.sleep(2)
            
            self.logger.info(f"Downloaded {downloaded_count} images")
            return downloaded_count
            
        except Exception as e:
            self.logger.error(f"Error scraping {category_url}: {str(e)}")
            return 0

def main():
    # Initialize scraper
    scraper = CatImageScraper()
    
    # Wikimedia Commons category URL for cat photographs
    url = "https://commons.wikimedia.org/wiki/Category:Cats_in_art"
    
    print(f"\nScraping images from: {url}")
    total_downloads = scraper.scrape_wikimedia_commons(url)
    print(f"\nTotal images downloaded: {total_downloads}")

if __name__ == "__main__":
    main()