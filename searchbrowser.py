from watchanimeapi import watchanime
from tabulate import tabulate


class SearchBrowser:
    search_engine = watchanime.Search

    def __init__(self, search):
        self.search = self.search_engine(search)

    def display_next_page(self):
        page = self.search.get_next_page()
        display_data = [anime.get_short_info() for anime in page]
        table = tabulate(display_data,
                         showindex=True,
                         headers=('tytuł', 'rodzaj'))
        return f'{self.search.page}/{self.search.page_amount}\n{table}'

    def display_previous_page(self):
        page = self.search.get_previous_page()
        display_data = [anime.get_short_info() for anime in page]
        table = tabulate(display_data,
                         showindex=True,
                         headers=('tytuł', 'rodzaj'))
        return f'{self.search.page}/{self.search.page_amount}\n{table}'

    def display_current_page(self):
        page = self.search.get_current_page()
        display_data = [anime.get_short_info() for anime in page]
        table = tabulate(display_data,
                         showindex=True,
                         headers=('tytuł', 'rodzaj'))
        return f'{self.search.page}/{self.search.page_amount}\n{table}'

    def get_anime(self, index):
        anime = self.search.get_current_page()
        if index >= len(anime):
            return 'Anime o takim numerze nie jest na stronie'
        return watchanime.Anime(anime[index])
