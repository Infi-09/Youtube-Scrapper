import requests
from bs4 import BeautifulSoup 

YOUTUBE_LINK = 'https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'

response = requests.get(YOUTUBE_LINK)

print('Status Code', response.status_code)

with open('trending.html', 'w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')

print('Doc Title: ', doc.title.text)

videoDivs = doc.find_all('div', class_='ytd-video-renderer')

print(f'Found {len(videoDivs)} videos')