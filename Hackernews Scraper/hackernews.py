from bs4 import BeautifulSoup
import requests

page = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(page.text, 'lxml')
links = soup.select('.storylink')
votes = soup.select('.score')
hn = []
for (link,vote) in zip(links,votes):
    a = link.getText()
    b = vote.getText()


print(hn)


