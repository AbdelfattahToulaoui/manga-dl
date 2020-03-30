from .scrapers import *
import argparse
import re
import sys

def parse_range(range):
    m = re.match('([0-9\.]+)-([0-9\.]+)', range)
    if not m:
        print('Not a valid range %s' % range, file=sys.stderr)
        sys.exit(1)
    
    try:
        min,max = float(m.group(1)), float(m.group(2))
    except:
        print('Range must consist of two valid numbers', file=sys.stderr)
        sys.exit(1)
    
    return min, max

def main():
    parser = argparse.ArgumentParser(description='Downloads manga from various websites.')
    
    parser.add_argument('command', action='store', choices=['d','l','c'],
                        help='Either d for download, l for list of mangas, or c for list of chapters')
    
    parser.add_argument('--site', '-s', action='store', required=True,
                        help='The website to use.',
                        choices=[i for i in scrapers])
    
    parser.add_argument('--manga', '-m', action='store', default=None,
                        help='A search term to use to look for manga.')
    
    parser.add_argument('--chapter', '-c', action='store', nargs='+',
                        type=float,
                        help='Specifies chapters to download.')
    
    parser.add_argument('--range', '-r', action='store', default=None,
                        help='Specifies chapter range to download. example: 1-50')
    
    parser.add_argument('--all', '-a', action='store_true',
                        help='Download all the chapters.')
    
    parser.add_argument('--index', '-S', action='store', default=0,
                        help='Search index of the manga, defaults to 0 for the first match.')
    
    parser.add_argument('--language', '-l', action='store',
                        help='For multilingual sites, specify the language.')
    
    parser.add_argument('--directory', '-D', action='store', default='.',
                        help='Directory which to download manga. Defaults to current directory.')
    
    parser.add_argument('--cbz', '-z', action='store_true',
                        help='Create a cbz file.')
    
    
    args = parser.parse_args()
    
    scraper = Scraper.getScraper(args.site)
    
    if args.command == 'd':
        if not args.manga:
            print('No manga specified', file=sys.stderr)
            sys.exit(1)
        elif not (args.chapter or args.range or args.all):
            print('No chapters specified', file=sys.stderr)
            sys.exit(1)
        else:
            m, n = -1, -1
            if args.all:
                chapters = []
            elif args.chapter:
                chapters = args.chapter
            else:
                m, n = parse_range(args.range)
            
            scraper.downloadChapters(
                args.manga,
                chapter_list=chapters,
                begin_ch=m,
                end_ch=n,
                directory=args.directory,
                lang=args.language,
                manga_search_index=args.index,
                cbz=args.cbz
                )
    elif args.command == 'l':
        if not args.manga:
            scraper.listMangas()
        else:
            scraper.listMangas(args.manga)
    else:
        if not args.manga:
            print('No manga specified', file=sys.stderr)
            sys.exit(1)
        else:
            scraper.listChapters(args.manga, lang=args.language, manga_search_index=args.index)

if __name__=='__main__':
    main()
