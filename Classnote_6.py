from bs4 import BeautifulSoup
import requests

url = "https://optical.toys//"
response = requests.get(url)

if response.status_code == 200:
    print("The response was successful")
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    paths = soup.find_all('path', attrs={'d': True})
    print(paths)
    for h2 in soup.find_all('h2'):
        print(h2.text)
    for styles in soup.find_all('style'):
        print(styles.text)
    for p in soup.find_all('p'):
        print(p.text)
    for img in images:
        print(img['src'])
else:
    print("The request failed")