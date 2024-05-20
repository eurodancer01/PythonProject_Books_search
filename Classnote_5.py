from bs4 import BeautifulSoup
import requests

url="http://optical.toys"

print(url)

response=requests.get(url)

if response.status_code==200:
    print("Successful")
    soup = BeautifulSoup(response.text, 'html.parser')
    texts=soup.find_all('txt')
    paths=soup.find_all('path', attrs={'d':True})
    print(paths)
    for text in texts:
        print(text)
else:
    print("Failed")



