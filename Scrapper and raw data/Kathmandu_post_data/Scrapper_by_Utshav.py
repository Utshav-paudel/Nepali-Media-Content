import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# importing necessary libraries
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

# Set up the web driver (e.g., ChromeDriver)
driver = webdriver.Chrome()

# Navigate to the website
url = "https://kathmandupost.com/national/province-no-5"
driver.get(url)

try:
    # Define a loop to click the "Load More" button until it's no longer available
    while True:
        # Wait for the "Load More" button to be clickable
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mainContent"]/main/div/div[2]/div[1]/span/span'))
        )

        # Click the "Load More" button to load additional content
        load_more_button.click()

        # Add a timer to wait for a few seconds before moving to the next page
        # time.sleep(3)  # Adjust the sleep time (in seconds) as needed

except Exception as e:
            # Handle any exceptions and break the loop when the "Load More" button is no longer available
            print(f"Error: {e}")

# Placeholder for your data scraping
        
# URL of the website to be scraped
url = "https://kathmandupost.com/national/province-no-5"

# Making a request for parsing the website
r = requests.get(url)
time.sleep(1)                              # so that website is not overlaoded
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Data list
data = []
# Function to extract article content
def get_article_content(url):
    article_class = "subscribe--wrapperx"                           # Update2: class of article
    date_class = "updated-time"                                     # Update3: class of date
    location_class = "updated-time updated-time_location"           # Update4: class of location

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article_body = soup.find("div", class_=article_class).text.strip()
        article_date = soup.find("div", class_=date_class).text.strip()
        article_location = soup.find("div", class_=location_class).text.strip()
        article_content = [article_body, article_date, article_location]  # List containing article body, date, and location
        return article_content
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return None
more_news_divs = soup.find_all("div",class_="block--morenews")
for more_news_div in more_news_divs:
    articles = more_news_div.find_all("article")
    # Loop to get elements
    for article in articles:
        try:
            article_title = article.find("h3").text.strip()                # Update5: article tag for title
            article_author = article.find("span").find("a").text.strip()   # Update6: article tag for author
            article_url = article.find("a")["href"]                        # Update6: article content link
            full_article_url = f"https://kathmandupost.com{article_url}"   # Update7: article content link update with the website
            article_content = get_article_content(full_article_url)        # Call function to get article content, date, location
            
            # Append data to the list
            data.append([article_title, *article_content, article_author])                 # List to append articles
        except Exception as e:
            print(f"Error occurred while processing article: {e}")
            data.append([article_title, None, None, None, None])  # If there's an error, add None values for article content, date, and location

# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=["Article Title", "Article Content", "Date", "Location","Author"])
print(df)

# Save the DataFrame to a CSV file (append mode)
with open('kathmandupost_province5.csv', 'a', encoding='utf-8', newline='') as f:
                df.to_csv(f, header=f.tell() == 0, index=False)

# Example: Get the current page source after all the "Load More" clicks
page_source = driver.page_source
# print(page_source)

# Close the web driver after scraping is complete
driver.quit()
