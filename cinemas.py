import bs4
import requests
import time

TOP = 10
AFISHA_URL = 'http://www.afisha.ru/msk/schedule_cinema/'
KINOPOISK_SEARCH_URL = 'https://www.kinopoisk.ru/index.php?first=yes&what=&kp_query='

def fetch_afisha_page():
    request_to_afisha = requests.get(AFISHA_URL).content
    return request_to_afisha


def parse_afisha_list(raw_html):
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    movies = []
    for film in soup.find_all('div', class_="object s-votes-hover-area collapsed"):
        if not is_it_arthouse(film):
            movies.append((film.find('div',{'class': "m-disp-table"} )).find('a').text)
    return movies


def is_it_arthouse(soup_film):
    if len(soup_film.find_all('tr')) < 15:
        return True
    else:
        return False


def fetch_movie_info(movie_title):
    url_search = '{0}{1}'.format(KINOPOISK_SEARCH_URL, movie_title)
    r = requests.get(url_search, timeout=10).content
    soup = bs4.BeautifulSoup(r, 'html.parser')
    average_rating = soup.find('span', class_='rating_ball').text
    voters_score = soup.find('span', class_='ratingCount').text
    time.sleep(5) #timeout, because Kinopoisk prefers to ban your IP(DDOS protect)
    return (movie_title, float(average_rating), voters_score)


def output_movies_to_console(movies):
    top_rating_films = sorted(movies, key=lambda movie: movie[1], reverse=True)
    for movie in top_rating_films[:TOP]:
        print('Фильм {} имеет {} голосов со средней оценкой {}'\
              .format(movie[0],movie[2],movie[1]))


if __name__ == '__main__':
    movies = parse_afisha_list(fetch_afisha_page())
    movies_info = []
    for movie in movies:
        movies_info.append(fetch_movie_info(movie))
    output_movies_to_console(movies_info)
