import json
import matplotlib.pyplot as plt
from collections import Counter

# Load the data from the JSON file
with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract genres from the data
genres = []
for book in data:
    genres.extend(book['genres'])

# Count occurrences of each genre
genre_counts = Counter(genres)

# Sort genres by count for better visualization
sorted_genres = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))

# Prepare labels and sizes for the pie chart
labels = list(sorted_genres.keys())
sizes = list(sorted_genres.values())

# Create the pie chart
plt.figure(figsize=(10, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # This makes the pie chart circular.
plt.title('Genre Distribution Across All Books')
plt.show()
