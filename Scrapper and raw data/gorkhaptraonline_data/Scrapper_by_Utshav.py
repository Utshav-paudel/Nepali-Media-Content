import requests
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
# function to get article content 
def get_article(url):
    article_class = "blog-details"  # Update2: class of article
    date_class = "mr-3 font-size-16"  # Update3: class of date
    location_class = "updated-time updated-time_location"  # Update4: class of location

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article_body= soup.find_all("div", class_=article_class)[3].text.strip()
        article_date = soup.find("span", class_=date_class).text.strip()
        # Trying to find article author and location
        try:
            article_location_author = soup.find_all("div", class_=article_class)[3]
            article_author = article_location_author.find("b").text.split()[:2]
            article_author = ''.join(article_author)
            article_location = article_location_author.find("b").text.split()[3]
            article_location= ''.join(article_location)
        except Exception as e:
            print(f"Error occurred while finding author and location: {e}")
            article_author = None
            article_location = None
        article_content = [article_body, article_date, article_location,article_author]  # List containing article body, date, and location
        return article_content
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return None

# Data list
data = []
for i in range(2,4):
    url = f"https://gorkhapatraonline.com/categories/province-two?page={i}"
    try:
        # Making a request for parsing the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all articles on the page
        articles = soup.find_all("div",class_="item-content d-flex flex-column align-items-start justify-content-center")
        # Loop to get elements from the current page
        for article in articles:
            try:
                article_title = article.find("a").text.strip()  # Update5: article tag for title
                article_url = article.find("a")["href"]  # Update6: article content link
                full_article_url = f"{article_url}"  # Update7: article content link update with the website
                article_content = get_article(article_url)  # Call function to get article content, date, location

                # Append data to the list
                data.append([article_title, *article_content])  # List to append articles
            except Exception as e:
                print(f"Error occurred while processing article: {e}")
                data.append([article_title, None, None, None, None])  # If there's an error, add None values for article content, date, and location
    except Exception as e:
        print(f"Error occurred while processing page: {e}")
    


# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=["Article Title", "Article Content", "Date", "Location", "Author"])
print(df)

# Save the DataFrame to a CSV file
df.to_csv('gorkhapatra_province_2_data.csv', encoding='utf-8', index=False)
