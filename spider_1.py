#coding=utf-8
import requests
import codecs
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250'


def download_page(url):

    return requests.get(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }).content

def parse_html(html):
    soup = BeautifulSoup(html ,'lxml')
    movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})
    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):
        deatil = movie_li.find('div', attrs={'class':'hd'})
        movie_name = deatil.find('span', attrs = {'class':'title'}).getText()
        movie_name_list.append(movie_name)
    next_page = soup.find('span',attrs={'class':'next'}).find('a')

    if next_page:

        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list ,None


def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb' ,encoding= 'utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))




if __name__ == '__main__':
    main()