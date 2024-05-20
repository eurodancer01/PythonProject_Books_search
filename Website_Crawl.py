import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def scrape_books(base_url):
    current_page = 1
    books_data = []
    while True:
        url = f"{base_url}page-{current_page}.html"
        response = requests.get(url)
        if response.status_code != 200:
            break  # Stop if we reach an invalid page

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.findAll('article', class_='product_pod')

        for book in books:
            title = book.find('h3').find('a')['title']
            price = book.find('p', class_='price_color').text
            rating = book.find('p', class_='star-rating')['class'][
                1]  # Class list includes 'star-rating' and the rating
            books_data.append({'Title': title, 'Price': price, 'Rating': rating})

        next_button = soup.find('li', class_='next')
        if not next_button:
            break  # Exit loop if there's no "next" button
        current_page += 1

    return pd.DataFrame(books_data)


base_url = 'http://books.toscrape.com/catalogue/'
books_df = scrape_books(base_url)

books_df['Price'] = books_df['Price'].replace('[^0-9.]', '', regex=True).astype(float)

# Map textual ratings to numerical
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
books_df['Rating'] = books_df['Rating'].map(rating_map)
print(books_df.head(10))
books_df.info()
# Display the first few entries



#Histogram
plt.figure(figsize=(8, 4))
sns.histplot(data=books_df, x='Price', bins=5, kde=True)
plt.title('Distribution of Book Price(Books.toScrape.com)')
plt.xlabel('Price (£)')
plt.ylabel('Count')
plt.show()

#Bar chart
avg_price_by_rating = books_df.groupby('Rating')['Price'].mean().reset_index()
plt.figure(figsize=(8, 4))
sns.barplot(data=avg_price_by_rating, x='Rating', y='Price')
plt.title('Average Price by Rating(Books.toScrape.com)')
plt.xlabel('Rating')
plt.ylabel('Average Price (£)')
plt.show()

#Box plot
plt.figure(figsize=(8, 4))
sns.boxplot(data=books_df, x='Rating', y='Price')
plt.title('Price Distribution by Rating(Books.toScrape.com)')
plt.xlabel('Rating')
plt.ylabel('Price (£)')
plt.show()

#Swarm plot
sns.swarmplot(data=books_df, x='Rating', y='Price', palette='coolwarm')
plt.title('Book Prices by Rating(Books.toScrape.com)')
plt.xlabel('Rating')
plt.ylabel('Price')
plt.show()
