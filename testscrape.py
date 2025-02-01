import requests
from bs4 import BeautifulSoup
import re
import pygame
import time

def scrape_google_finance(ticker):
    try:
        # Construct URL for the stock ticker
        url = f'https://www.google.com/finance/quote/{ticker}:NASDAQ?hl=en'
        
        # Headers to mimic a browser request, preventing some blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        
        # Fetch the page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the current price
        price_element = soup.find('div', class_='YMlKec fxKbKc')
        if price_element:
            price = price_element.text
            # Clean the price string (remove currency symbol if present, e.g., '$')
            price = re.sub(r'[^\d\.]', '', price)
            return float(price)
        else:
            return None  # Price not found or element structure changed
        
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 320, 240
screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
pygame.display.set_caption('NVIDIA Stock Price Display')

image = pygame.image.load('DisplayTest.png')
# Scale the image to fit the window if necessary
#image = pygame.transform.scale(image, (width, height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)
nvidia_ticker = "NVDA"

# Font setup
font = pygame.font.Font(None, 36)

# Last update time
last_update = time.time()

# Initial price
current_price = scrape_google_finance(nvidia_ticker)
current_price2 = scrape_google_finance("TSLA")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # When mouse is clicked, set last_update to 10 minutes in the past
            last_update = time.time() - 600  # 600 seconds = 10 minutes    for event in pygame.event.get():
            running = False

    # Check if 5 minutes have passed
    if time.time() - last_update > 600:  # 300 seconds = 5 minutes
        current_price = scrape_google_finance(nvidia_ticker)
        current_price2 = scrape_google_finance("TSLA")
        last_update = time.time()

    # Drawing
    screen.blit(image, (0, 0))
    price_text = font.render(f"NVDA: ${current_price:.2f}", True, BLUE)
    screen.blit(price_text, (50,50))
    price_text = font.render(f"TSLA: ${current_price2:.2f}", True, BLUE)
    screen.blit(price_text, (50,100))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
