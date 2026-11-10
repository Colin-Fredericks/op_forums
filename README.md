# Onyx Path Forum Backup

This repository is a backup of the Onyx Path discusion boards as of November 8th, 2026, before they were closed. Warning to those who might want to clone it: this repo is LARGE, almost 11GB.

Files are stored in the `forum_backup` folder.

If you'd like to run this yourself:

1. Make sure you have Python 3.14 or later available.
2. Install `uv` from [https://docs.astral.sh/uv/#installation](https://docs.astral.sh/uv/#installation).
3. Run `uv add forumscraper` in this folder. This installs the [Forumscraper command-line utility and library](https://github.com/TUVIMEN/forumscraper).
4. Run `uv run forum_handler.py -h` for more detailed instructions.

The script as-is only scrapes the Onyx Path forums, so it's not going to be very useful after January 1st 2027, but you could theoretically adjust it to scrape someone else's forums I guess. Get permission first. Slamming someone's server is considered rude.

## To Do

- Adjust links so the whole thing can live on GitHub Pages internally, rather than every link going back to the closed forums.
- Store all CSS locally.
