from os import system
from cda import cda
from episodebrowser import EpisodeBrowser
from searchbrowser import SearchBrowser
from watchanimeapi import watchanime
import re


def clear(): system('clear')


def chose_quality(qualities):
    quality = ''
    while quality not in qualities.keys():
        print(' '.join(qualities.keys()))
        quality = input('wybierz jakość: ')
        clear()
    return qualities[quality]


def player(episode):
    try:
        player_data = cda.get_video_data(watchanime.parse_player(episode.link)[-1])
    except IndexError:
        print('Nie ma dostępnych playerów :(')
        return None
    quality = chose_quality(player_data['video']['qualities'])
    url = cda.get_video_url(player_data, quality)
    system(f'mpv {url}')


def browse_episodes(anime):
    browser = EpisodeBrowser(anime)
    print(browser.display_current_page())
    command = ''
    while command not in (':q', ':quit'):
        command = input()

        match command:
            case index if re.fullmatch(r':\d+', index):
                clear()
                player(browser.get_episode(int(index[1:])))
                command = ':q'

            case ':next':
                clear()
                print(browser.display_next_page())

            case ':prev':
                clear()
                print(browser.display_previous_page())

            case ':q' | ':quit':
                print('wracanie do wyszukiwarki')

            case _:
                print('Komenda nie istnieje :(')


def search(search):
    browser = SearchBrowser(search)
    command = ''
    print(browser.display_current_page())
    while command not in (':q', ':quit'):
        command = input()

        match command:
            case index if re.fullmatch(r':\d+', index):
                clear()
                browse_episodes(browser.get_anime(int(index[1:])))
                command = ':q'

            case ':next':
                clear()
                print(browser.display_next_page())

            case ':prev':
                clear()
                print(browser.display_previous_page())

            case ':q' | ':quit':
                print('Opuszczanie wyszukiwarki')

            case _:
                print('Komenda nie istnieje :(')

def help():
    clear()
    print('Witamy w pomocy programu anime cli')
    print('Dostępne komendy:\n')
    print('wyjście :q albo :quit')
    print('Wyszukanie ?nazwa anime')
    print('Aby otworzyć pozycje w wyszukiwarce napisz :numer pozycji w tabelce')
    print('poprzednia strona :prev')
    print('następna strona :next\n')
    print('Aby wrócic do programu kliknij enter')
    input()
    clear()
