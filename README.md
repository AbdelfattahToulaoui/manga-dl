# Manga-Dl

A python tool to download manga from popular scanlation sites

### Installing

First, install the dependencies from requirements.txt, to do this make sure you have Python3 and pip installed and in your system path, then open a command prompt in the  and type:

```
pip install bs4 pyexecjs requests
```

or:

```
pip3 install bs4 pyexecjs requests
```

Now, get the code from the repo; to do this, either download and extract the `.zip` file from the github page, or clone the repo using the command:

```
git clone https://github.com/AbdelfattahToulaoui/manga-dl
```

Issue the install command in the code directory:

```
python3 setup.py install
```

If you're using a UNIX, you might have to issue the command as root:

```
sudo python3 setup.py install
```

If this goes without a hitch, you should have the manga-dl module installed on your system, to verify:

```
manga-dl --help
```

You should see the help message of the tool.

## Usage

This tool can download manga from one of the currently supported sites: mangadex,mangafox,mangahub,mangakakalot,manganelo

```
usage: manga-dl [-h] --site
                {mangadex,mangafox,mangahub,mangakakalot,manganelo}
                [--manga MANGA] [--chapter CHAPTER [CHAPTER ...]]
                [--range RANGE] [--all] [--index INDEX] [--language LANGUAGE]
                [--directory DIRECTORY] [--cbz]
                {d,l,c}

Downloads manga from various websites.

positional arguments:
  {d,l,c}               Either d for download, l for list of mangas, or c for
                        list of chapters

optional arguments:
  -h, --help            show this help message and exit
  --site {mangadex,mangafox,mangahub,mangakakalot,manganelo}, -s {mangadex,mangafox,mangahub,mangakakalot,manganelo}
                        The website to use.
  --manga MANGA, -m MANGA
                        A search term to use to look for manga.
  --chapter CHAPTER [CHAPTER ...], -c CHAPTER [CHAPTER ...]
                        Specifies chapters to download.
  --range RANGE, -r RANGE
                        Specifies chapter range to download. example: 1-50
  --all, -a             Download all the chapters.
  --index INDEX, -S INDEX
                        Search index of the manga, defaults to 0 for the first
                        match.
  --language LANGUAGE, -l LANGUAGE
                        For multilingual sites, specify the language.
  --directory DIRECTORY, -D DIRECTORY
                        Directory which to download manga. Defaults to current
                        directory.
  --cbz, -z             Create a cbz file.
```

There are 3 main functionalities: Search manga, list chapters, and download chapters

### Examples

To list all the manga on mangahub:

```
manga-dl l -s mangahub
```

To search for the manga named 'black clover' on mangafox:

```
manga-dl l -s mangafox -m 'black clover'
```

To list all chapters from the manga named 'black clover' available on mangafox:

```
manga-dl c -s mangafox -m 'black clover'
```

To download chapter 3, 4, and 10 of 'Komi-san' from manganelo as `.cbz`:

```
manga-dl d -s manganelo -m 'komi-san' -c 3 4 10 -z
```

To download chapters 1 to 10 of 'Komi-san' from mangadex in french:

```
manga-dl d -s mangadex -m 'komi-san' -l fr -r 1-10
```

To download ALL chapters of 'one piece' from mangahub as `.cbz` files:

```
manga-dl d -s mangadex -m 'one piece' -a
```

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
