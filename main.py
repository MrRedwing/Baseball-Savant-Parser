from download import validate
from static import savant_site_static

if __name__ == "__main__":
    url = input('Url: ')
    batter = validate('Batter (y / n): ')
    while True:
        sort_type = input('Sort type (basic, recent, latest): ').lower().strip()
        if sort_type == 'basic' or sort_type == 'recent' or sort_type == 'latest':
            break
        print('Invalid input ')
    savant_site_static(url, batter, sort_type)