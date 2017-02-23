import requests
from bs4 import BeautifulSoup

word = '4wUPASp2hfY'
def get_backlinks(word):
    if word[0] == '-':
        word = word[1:]
    r = requests.get('http://www.google.com/search?q=' + word)
    print('http://www.google.com/search?q=' + word)
    print(r)
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.find('div',{'id':'resultStats'}).text)
    return int(soup.find('div',{'id':'resultStats'}).text.split()[1].replace(',',''))