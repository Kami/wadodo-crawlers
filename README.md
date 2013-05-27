# Wadodo Crawlers

## Available Crawlers

* `vegas.com`

## Usage

```bash
scrapy crawl -o <output file name> -t jsonlines <crawler name> \
--flickr_api_key=<flickr api_key> [--set=DOWNLOAD_DELAY=<seconds>]
```

All of the available options are listed at [http://doc.scrapy.org/en/latest/topics/settings.html](http://doc.scrapy.org/en/latest/topics/settings.html)
