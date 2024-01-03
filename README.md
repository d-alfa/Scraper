# Scraper (refactor_branch)

## Overview

Refactored original scraper using scrapy framework, for better project scaling.

## Changes

- **Created [Black_Tea_Spider]** : Spider crawles through website and extracts data.
- **Created [Black_Tea_Item]** : An Item is a container that is used to store scraped data.
- **Created [Scraper_Pipeline]** : Cleaning, processing, and saving the scraped data.
- **Updated [settings]** : Saving scraped data into .json file.
