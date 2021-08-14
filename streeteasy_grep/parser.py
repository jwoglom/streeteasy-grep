#!/usr/bin/env python3

import sys
import json
import time
from selenium import webdriver

from streeteasy_grep import config as cfg


def construct_url(args=None):
    """ Construct street easy url given args """

    # TODO: Use args make it dynamic
    lower_bound = 0
    upper_bound = 3000
    # TODO: Support multiple locations (have to manually find each keyword)
    location = "ues"
    beds = 1
    no_fee = True

    url = f"{cfg.STREETEASY_SITE}/for-rent/{location}/price:{lower_bound}-{upper_bound}|beds:{beds}"

    if no_fee:
        url += f"|no_fee"

    return url


def sanitize_link(link):
    """ Santiize link from any non-standard features. """

    if not link:
        return ""
    # Remove query paramaters
    link = link.split("?")[0]

    return link


def main():
    """ Setup and parse results"""
    # Requires gecko driver to be installed.
    # https://github.com/mozilla/geckodriver/releases
    opts = webdriver.FirefoxOptions()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    url = construct_url()
    print(f"Parsing url: [{url}]")
    driver.get(url)

    # Start parsing out the result content
    # This is extremely fragile and required looking through the HTML for the div ids
    search_results = driver.find_element_by_class_name("searchCardList")
    result_list = search_results.find_elements_by_tag_name("li")
    results_dictionary = {}
    for result in result_list:
        # Get the listing link
        a_el = result.find_elements_by_class_name("listingCard-globalLink")
        link = sanitize_link(a_el[0].get_attribute("href"))
        # Get text info
        # Have to use xpath to get span elements
        text_el = result.find_elements_by_xpath('.//span[@class = "u-displayNone"]')
        print(text_el)
        text = text_el[0].text
        # Get price
        price_el = result.find_elements_by_class_name("price")
        price = price_el[0].text

        results_dictionary[link] = {"Description": text, "Price": price}

    print(results_dictionary)

    driver.close()


if __name__ == "__main__":
    sys.exit(main())
