# HyScrape
## Scraping HyTek Web-Based Swim Results
********

## Overview

Almost all swim meets are managed using HyTek's **Meet Manager**, which optionally publishes web-based results during the swim meet. Result files are stored in HTML. The purpose of **HyScrape** is to scrape these results into a tabular format.

********

## Status

This project is in a preliminary phase and has only been tested on collegiate meets. I have a lot of Python code written to scrape the results, but formatting is the primary challenge. Right now the code can scan a specified URL for HyTek results and list all events and their event-specific URL. The formats vary based on a few criteria:

* **Round:** Slight variation between Psych, Prelims, and Finals 
* **Event:** Variation between individual swims, diving, and relays

********

## Project Notes

A large challenge of this project is formatting the result lines. It's fairly easy to *find* the result lines within a HTML page (`re.search(pattern="^\s*\d{1,3}\s.*", string=row)` where `row` is a line in the results/psych page) can consistently find a line representing a swimmer. Great. The hard part is then *formatting* said line into tabular data. There are a few variations these lines can take, such as:

<pre>
`1 FLOR-FL  'A'                        1:34.18    1:34.25   64  `
</pre>

* **1**: Place
* **FLOR-FL**: Team name
* **'A'**: Relay team
* **1:34.18**: Seed time
* **1:34.25**: Time
* **64**: Points

********


