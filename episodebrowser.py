from watchanimeapi import watchanime
from tabulate import tabulate


class EpisodeBrowser:
    def __init__(self, anime: watchanime.Anime):
        self.anime = anime
        self.current_page = self.anime.get_current_page()

    def display_next_page(self):
        page = self.anime.get_next_page()
        display_data = [episode.get_summary() for episode in page]
        return tabulate(display_data,
                        showindex=True,
                        headers=('Numer Odcinka', 'Tytuł', 'Filer'))

    def display_previous_page(self):
        page = self.anime.get_previous_page()
        display_data = [episode.get_summary() for episode in page]
        return tabulate(display_data,
                        showindex=True,
                        headers=('Numer Odcinka', 'Tytuł', 'Filer'))

    def display_current_page(self):
        page = self.anime.get_current_page()
        display_data = [episode.get_summary() for episode in page]
        return tabulate(display_data,
                        showindex=True,
                        headers=('Numer Odcinka', 'Tytuł', 'Filer'))

    def get_episode(self, index):
        if index >= len(self.current_page):
            return 'Anime o takim numerze nie jest na stronie'
        return self.current_page[index]