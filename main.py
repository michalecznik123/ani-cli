from cli import search, help
from re import fullmatch


def main():
    command = ''
    while command not in (':q', ':quit'):
        print('Witamy w programie anime cli')
        print('Aby wyszukać anime napisz ?nazwa anime')
        print('Aby uzyskać liste komend napisz :help')
        command = input()
        match command:
            case ':q' | 'quit':
                print('Dziękujemy za używanie programu')
            case search_value if fullmatch(r'^\?.+', search_value):
                search(search_value[1:])
            case ':next' | ':prev':
                print('Komendy obsługiwane tylko w trybie wyszukiwania')
            case ':help':
                help()
            case _:
                print('komenda nie istnieje')


if __name__ == '__main__':
    main()