# Social housing motivation

In this repo we process data from the [Mijndak](https://utrecht.mijndak.nl/) page, where social housing is listed. Every city has its own page with listings. We get these pages, and using `beautifulsoup` we fetch all the individual listings and put them in a csv.

This code was created for a data/AI-course and therefore is written quickly and pragmatically. The site is not too well built, which makes scraping a bit of a challenge so bear with me.

## Prerequisites

This code is written in Python and uses no external libraries except `beautifulsoup4` and `playwright` (a headless browsing tool). These can be installed using `pip install -r requirements.txt`. Preferably use a separate python environment with `conda` or `venv` for this. Playwright might also ask you to install some browsers and other tools when first launching.

## Scraping process

- Because Mijndak is a SPA that loads all of its data with javascript, simply going to the city pages (such as [the one from Utrecht](https://utrecht.mijndak.nl/Woningaanbod)) and saving the page as html is the first step. Drag that html file (only the html file is needed) into the `output/listings` folder. This could be automated by using [Playwright](https://playwright.dev/python/docs/library). For now I just did it by hand because of time constraints.
- Next, run the `python fetch-individual-listings.py` command to get the individual listings. This launches a headless browser to fetch the individual listings.
- Finally, run `python listings-to-csv.py` to export the listings to a csv sheet. Here, possible refinements include getting more data from the individual listings. It's pretty basic now.
