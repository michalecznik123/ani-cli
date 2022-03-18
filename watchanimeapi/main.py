from bs4 import BeautifulSoup
import requests
from watchanimeapi import common, models
import re
from typing import List


def parse_anime_card(soup: BeautifulSoup) -> models.AnimeModel:
    kind = soup.find('span', {'class': 'badge'}).get_text()
    card_title = soup.find('h5', {'class': 'card-title'})
    title = card_title.get_text().strip()
    anime_url = 'https://ogladajanime.pl' + card_title.find('a').get('href')
    description = soup.find('p', {'class': 'card-text'}).get_text().strip()
    return models.AnimeModel(anime_url, title, description, kind)


def parse_page(soup: BeautifulSoup) -> List[models.AnimeModel]:
    cards = soup.find_all('div', {'class': 'anime-item'})
    anime_on_page = []
    for card in cards:
        anime_on_page.append(parse_anime_card(card))
    return anime_on_page


def get_page_amount(search):
    payload = f'action=search_anime&search={search}&search_type=name&page=1'
    url = "https://ogladajanime.pl/command_manager.php"
    r = requests.request("POST", url, headers=common.HEADERS, data=payload)
    soup = BeautifulSoup(r.json()['data'], 'lxml')
    regex = re.compile(r"\\?action=search_anime&search_type=name&page=.+")
    page_links = [int(a.get_text()) for a in soup.find_all('a', {'href': regex})]
    if len(page_links):
        return max(page_links)
    else:
        return 0


class Search:
    def __init__(self, search: str):
        self.search = search
        self.page_amount = get_page_amount(search)
        self.pages = [None] * (self.page_amount + 1)
        self.page = 0

    def get_page(self, page_number) -> List[models.AnimeModel]:
        if page_number < 0:
            page_number = (self.page_amount + page_number) % self.page_amount
        if page_number > 0:
            page_number = page_number % self.page_amount
        if self.pages[page_number] is None:
            payload = f'action=search_anime&search={self.search}&search_type=name&page={page_number + 1}'
            url = "https://ogladajanime.pl/command_manager.php"
            r = requests.request("POST", url, headers=common.HEADERS, data=payload)
            soup = BeautifulSoup(r.json()['data'], 'lxml')
            self.pages[page_number] = parse_page(soup)
        return self.pages[page_number]

    def get_next_page(self) -> List[models.AnimeModel]:
        self.page += 1
        return self.get_page(self.page)

    def get_previous_page(self) -> List[models.AnimeModel]:
        self.page -= 1
        return self.get_page(self.page)


def parse_player(url: str) -> List[str]:
    r = requests.get(url, headers=common.HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    links = []
    for player in soup.find_all('tr'):
        if len(player.contents) > 6:
            if player.contents[5].text == 'cda':
                data = player.contents[7].find('button').get('onclick')
                episode_id, player_id = re.search("changePlayer\\((?P<player_data>.*)\\);", data)['player_data'].split(
                    ',')
                url = f'https://ogladajanime.pl/player_data.php?action=get_player&url_id={player_id}&episode_id=' \
                      f'{episode_id} '
                links.append(requests.get(url).text)
                print('new_episode')
    return links


def parse_episode_list(anime_id: int, anime_url: str, start_index=0) -> List[models.Episode]:
    data = f'action=get_episodes&start_index={start_index}&reversed=0&anime_id={anime_id}'
    r = requests.post('https://ogladajanime.pl/command_manager.php', headers=common.HEADERS, data=data)
    soup = BeautifulSoup(r.json()['data'], 'lxml')
    episodes = []
    for episode in soup.find_all('tr'):
        number = int(episode.contents[0].text)
        title = episode.contents[2].text
        is_filer = episode.find('span').text
        url = f'{anime_url}{number}'
        episodes.append(models.Episode(title, number, is_filer, parse_player(url)))
    return episodes


class Anime(models.AnimeModel):
    def __init__(self, anime: models.AnimeModel):
        r = requests.get(anime.url, headers=common.HEADERS)
        self.anime_id = re.search(r'CurrentAnimeId = (?P<anime_id>.+);', r.text)['anime_id']
        self.start_index = -30
        super().__init__(anime.url, anime.title, anime.description, anime.type)

    def get_next_page(self):
        self.start_index += 30
        episodes = parse_episode_list(self.anime_id, self.url, start_index=self.start_index)
        if len(episodes) < 30:
            self.start_index = -30
        if len(episodes) == 0:
            return None
        return episodes
