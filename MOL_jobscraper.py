from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time

'''
The idea is to open the from TE-toimisto which contain interesting job advertisements.
The each advertisement is opened in order, and the text that contains the information 
is scraped from the screen and saved to a list/file/whatever.
'''


def get_website_contents(website_address):
    """This function retrieves and returns the contents of the
    website that is passed to it as an argument."""
    browser.get(website_address)
    time.sleep(1)
    website_contents = browser.page_source
    return website_contents


def get_website_links(website_address):
    """This function retrieves and returns all the links of the
    website that is passed to it as an argument."""
    browser.get(website_address)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    website_links = soup.find_all(class_="list-group-item")
    link_list = []
    for website_link in website_links:
        links = website_link.find_all("a")
        for link in links:
            link_list.append(link["href"])
            # print(link["href"])
    return link_list


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


def write_website_to_file(contents, filename, pathname):
    """This function writes the website contents to a file
    as bytes."""
    write_contents_bytes = bytearray(contents, "utf-8")
    try:
        filepath = os.path.join("./save/" + pathname + "/")
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(os.path.join(filepath, filename), "wb") as file:
            file.write(write_contents_bytes)
            print(filepath + filename + " saved")
    except IOError as exception:
        print("Couldn't save the file. Encountered an error: %s" % exception)


if __name__ == "__main__":

    address_tieto_ja_viestintateknologian_johtajat = ["Tieto_ja_viestintajohtajat", "https://paikat.te-palvelut.fi/tpt/?professions=1330&announced=0&leasing=0&english=false&sort=1"]
    address_informaatio_ja_tietoliikenneteknologian_asiantuntijat = ["Info_ja_tietoliiktekn_asiantunt", "https://paikat.te-palvelut.fi/tpt/?professions=35&announced=0&leasing=0&english=false&sort=1"]
    # This is the main branch, and the three following this one (ICT-alan, shakotekn., and elektroniikan) are individual files under it.
    address_sahkoteknologian_erityisasiantuntijat = ["Sahkoteknologian_erityisasiantunt", "https://paikat.te-palvelut.fi/tpt/?professions=215&announced=0&leasing=0&english=false&sort=1"]
    address_ict_alan_erityisasiantuntijat = ["ICT_alan_asiantunt", "https://paikat.te-palvelut.fi/tpt/?professions=2153&announced=0&leasing=0&english=false&sort=1"]
    address_sahkotekniikan_erityisasiantuntijat = ["Sahkotekniikan_asiantunt", "https://paikat.te-palvelut.fi/tpt/?professions=2151&announced=0&leasing=0&english=false&sort=1"]
    address_elektroniikan_erityisasiantuntijat = ["Elektroniikan_asiantunt", "https://paikat.te-palvelut.fi/tpt/?professions=2152&announced=0&leasing=0&english=false&sort=1"]

    browser = webdriver.PhantomJS("/home/eewijet/PhantomJS/bin/phantomjs")
    address_start = "https://paikat.te-palvelut.fi"
    address = address_tieto_ja_viestintateknologian_johtajat
    pathname = address[0]
    weblinks = get_website_links(address[1])
    link_counter = 0
    for i in weblinks:
        link_counter += 1
    print("Total number of ad links: " + str(link_counter))
    scrape_counter = 0
    for link in weblinks:
        filename = link[5:12] + ".txt"
        link_address = address_start + link
        contents = get_website_contents(link_address)
        information = get_information_between_tags(contents, "detailAdName", "detailText")
        write_website_to_file(information, filename, pathname)
        scrape_counter += 1
    print("Total ads scraped: " + str(scrape_counter) + "/" + str(link_counter))
    browser.close()
    browser.quit()