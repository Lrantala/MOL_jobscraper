from bs4 import BeautifulSoup
import os
from selenium import webdriver

'''
The idea is to open the from TE-toimisto which contain interesting job advertisements.
The each advertisement is opened in order, and the text that contains the information 
is scraped from the screen and saved to a list/file/whatever.
'''


def get_website_contents(website_address):
    """This function retrieves and returns the contents of the
    website that is passed to it as an argument."""
    browser = webdriver.PhantomJS("/home/eewijet/PhantomJS/bin/phantomjs")
    browser.get(website_address)
    website_contents = browser.page_source
    return website_contents

def get_information_between_tags(contents, divtag, ptag):
    """This function gets the text between certain tags"""
    soup = BeautifulSoup(contents, 'html.parser')
    #info = soup.find(divtag)
    info = soup.find("div", class_=divtag)
    info_text = info.text.strip()
    info_text = info_text.replace('"', '')
    info_text = os.linesep.join([s for s in info_text.splitlines() if s])
    desc = soup.find("p", class_=ptag)
    desc_text = desc.text.strip()
    desc_text = desc_text.replace('"', '')
    desc_text = os.linesep.join([s for s in desc_text.splitlines() if s])
    full_text = info_text + "\n\n" + desc_text
    return full_text


def write_website_to_file(contents, filename):
    """This function writes the website contents to a file
    as bytes."""
    write_contents_bytes = bytearray(contents, "utf-8")
    try:
        with open(filename, "wb") as file:
            file.write(write_contents_bytes)
    except IOError as exception:
        print("Couldn't save the file. Encountered an error: %s" % exception)


def read_arguments(arguments):
    """This reads the arguments passed to the program and returns
    the latter representing the website address. If no address is
    provided, the function returns None."""
    if len(arguments) == 3:
        return arguments[1], arguments[2]
    elif len(arguments) == 2:
        return arguments[1], None
    else:
        return None, None


def print_help():
    """This function prints help text to instruct user how to use
    this scraping program."""
    print("\nThis is a simple program for scraping job advertisements from TE-toimisto's website.")


if __name__ == "__main__":
    address = "https://paikat.te-palvelut.fi/tpt/9534707"
    filename = "tyo.txt"
    if address is None:
        print_help()
    else:
        raw_content = get_website_contents(address)
        if raw_content is None:
            print("Website could not be loaded or does not exist.")
        else:
            content = get_information_between_tags(raw_content, "detailAdName", "detailText")
        if content is None:
            print("There is nothing to be saved.")
        else:
            if filename is not None:
                write_website_to_file(content, filename)
                print("Wrote to file %s" % filename)