# FOSDEM event scraper

### Running

Here is a typical workflow to get this project running. After cloning the project, change your current directory to the newly cloned project directory. Then run the following:

```shell
# create a local Python virtual environment
python3 -m venv venv

# download and install requirements into the virtual environment
venv/bin/pip install -r requirements.txt
```

Adjust settings as necessary in `fosdem_event_scraper/settings.py`. Scraper specific settings can be found at the bottom of the file. Your file with URLs needs to be where `INPUT_FILE` is pointing at.
`fosdem_event_urls.txt` is in this repository as an example file. Adjust it as you see fit or create your own file.

After setting up, run the following to start the crawler:

```shell
venv/bin/python -m scrapy crawl fosdem-event
```

The output will be written to the file specified by `ICAL_OUTPUT_FILE` in the settings.
