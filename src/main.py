import requests
import os
import webbrowser
import time
import urllib

import pandas as pd
import numpy as np

import scrapy
import lxml
import lxml.html
# selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium import *

# import selenium stealth
# A python package selenium-stealth to prevent detection. This programme is trying to make python selenium more stealthy.

# import thread ??
# https://docs.python.org/3/library/threading.html
# https://realpython.com/intro-to-python-threading/

# import asyncio
# https://docs.python.org/3/library/asyncio.html

# import simplejson
# https://pypi.org/project/simplejson/

# error handling
from selenium.common.exceptions import NoSuchElementException

# bs4
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.3"
    }

def quitBrowser():
    browser.quit()

def promptToQuit():
    question_to_close = input("Do you want to close the browser. y or n?\n")
    if question_to_close == "y":
        quitBrowser()

def openWebrowserOne():
    global browser
    URL = "https://www.bundesanzeiger.de/pub/de/suche-rechnungslegung?"
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(executable_path="./drivers/geckodriver", options=options)
    browser.implicitly_wait(0.4)
    browser.get(URL)

def openWebrowserOne(web_browser="Chrome"):
    global browser
    URL = "https://www.bundesanzeiger.de/pub/de/suche-rechnungslegung?"
    if (web_browser == "Firefox"):
        options = webdriver.FirefoxOptions()
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver", options=options)
    else:
        options = webdriver.ChromeOptions()
        browser = webdriver.Remote(command_executor='http://www.example.com', options=options)
    options.headless = True
    browser.implicitly_wait(0.4)
    browser.get(URL)


def openWebrowserTwo():
    # update code, because executable path has been depreciated
    # source for update example
    # https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    global browser
    URL = "https://www.bundesanzeiger.de/pub/de/suche-rechnungslegung?"
    browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
    browser.implicitly_wait(0.4)
    browser.get(URL)

# accept cookies
def acceptCookies():
    cookies = browser.find_element(By.ID,'cc_all').click()
    return cookies

def companyLookup():
    searchBar = browser.find_element(By.ID,'id7')
    global company_name
    company_name = input("Please input the company name you are looking for:\n")
    searchBar.send_keys(str(company_name))
    searchBar.submit()


def setCaptchaInput():
    input_field = browser.find_element(By.NAME, "solution")
    captcha = input("Please input the valid captcha characters\n")
    input_field.send_keys(str(captcha))
    input_field.submit()

def selectJahresabschlüsse():
    search_field = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dropdownMenuButton"]')))
    search_field.click()
    jahresabschluesse = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="9135"]/a')))
    jahresabschluesse.click()

def selectIncomeStatement():
    search_field = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dropdownMenuButton"]')))
    search_field.click()
    jahresabschluesse = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="9135"]/a')))
    jahresabschluesse.click()

def createListForCompanyNames():
    wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section[2]/div/div/div/div/div[6]')))
    results = wait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/section[2]/div/div/div/div/div[6]')))
    print(results.text + "\n")
    results_text = results.text
    list2 = results_text.splitlines()
    print(list2)
    r = re.compile(r''+company_name, re.I)
    company_name_list = list(filter(r.match, list2))
    print(company_name_list)
    return company_name_list

def createListForCompanyBalanceSheets():
    return 0

def getLinks():
    elements = browser.find_elements('Jahresabschluss')
    print(elements)

def downloadHTML():
    current_url = getCurrentUrl()
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.find_elment("/html/body/div[1]/section[2]/div/div/div/div/div[6]"))

    return res

def getCurrentUrl():
    return browser.current_url

def main():
    openWebrowserTwo()
    acceptCookies()
    companyLookup()
    # getLinks()
    # selectJahresabschlüsse()
    # createListForCompanyNames()
    # result container global search
    #
    # print(resultContainer)
    link_text = ""
    try:
        link_text = browser.find_element(By.LINK_TEXT, "Jahresabschluss zum Geschäfsjahr vom 01.01.2020 bis zum 31.12.2020")
        print("Full link text found")
    except NoSuchElementException:
        print("No full link text found")
        try:
            link_text = browser.find_element(By.PARTIAL_LINK_TEXT, "Jahresabschluss")
            print("Partial link text found")
        except NoSuchElementException:
            print("No partial link text found")

        # jahresabschluss hyper link class name = "info"
        # name des Unternehmnes html class name = "first"
        # datum html class name = "date"
    # except:
    #     ("Something wrent wrong")
    print(type(link_text))
    link_text.get_attribute("class")
    link_text.screenshot("./screenshots/link_text.png")
    link_text.click()

    # sicherheitsabfrage (captcha)
    try:
        # captcha container
        captcha_container = browser.find_element(By.XPATH, "/html/body/div[1]/section/div/div/div/div/div[3]/div[2]/div[2]")
        print("Captcha container found")
        captcha_container.screenshot("./screenshots/captcha_container.png")
        # captcha wrapper
        captcha_wrapper = browser.find_element(By.XPATH, "/html/body/div[1]/section/div/div/div/div/div[3]/div[2]/div[2]/form/div[2]/div[1]/div")
        print("Captcha wrapper found")
        captcha_wrapper.screenshot("./screenshots/captcha_wrapper.png")
    except NoSuchElementException:
        print("Neither captcha container nor wrapper found")

    # find captcha image and download or screeenshot
    # css selector: .captcha_wrapper > img:nth-child(1)
    # css path: html body div#content.content section.indent_top_small.indent_bottom_small div.container div.row div.col-sm-12 div.content-container.margin_bottom_large div.block-sicherheitsabfrage.mt-30 div.block-content.bg-gray-light div.container.captcha_container form#idbf div.row div.col-md-5 div.captcha_wrapper img
    # only 500 captchas to solve
    # GAN-based approach

    # first approach was using the screenshot method
    # second uses urllib to download the img file
    # donwloading the file yields a higher image quality than screenshotting
    # no always, answer lies here : https://superuser.com/questions/1333187/quality-of-image-file-screenshot-of-the-image-vs-original-image
    try:
    # finding element by css selector
        captcha_elment = browser.find_element(By.CSS_SELECTOR, ".captcha_wrapper > img:nth-child(1)")
        print("first worked")
    except:
        print("captcha element not found")
        try:
            captcha_element_by_xpath_alt = browser.find_element(By.XPATH, "//img[@alt='Captcha']")
            print("second worked")
        except:
            print("captcha element by xpath passing alt as arg not found")
            try:
                captcha_element_by_css_alt = browser.find_element(By.CSS_SELECTOR, '[alt="Captcha"]')
                print("third worked")
            except:
                print("captcha element not found by css selector passing alt as arg ")

    try:
        captcha_form = browser.find_element(By.CLASS_NAME, "form-control")
        print("class name found")
    except NoSuchElementException:
        print("no web element by class name found")
        try:
            captch_input_name = browser.find_element(By.NAME, "sulution")
            print("web element by name found")
        except NoSuchElementException:
            print("no web element by name found")

    # get table
    # table id = "begin_pub"
    try:
        setCaptchaInput()
        source = getCurrentUrl()
        print(source)
        data = pd.read_html(requests.get(source, headers=headers).text)
        print(data)
    except ValueError:
        print("no tables found")
        try:
            # 1 After setting up the driver, we select the table with its ID value
            # 2 Then, from that element, we get the HTML instead of the web driver element object
            # with .get_attribute("outerHTML")
            # 3 We use pandas to parse the html
            # 4 So we index into that list with the only table we have, at index zero
            df = pd.read_html(browser.find_element(By.ID, "begin_pub").get_attribute("outerHTML"))[1]
            print(df)
        except NoSuchElementException:
            print("no table element found")
        finally:
            # beautifulsoup approach
            # https://stackoverflow.com/questions/53398785/pandas-read-html-valueerror-no-tables-found
    finally:
        promptToQuit()

if __name__ == "__main__":
    main()








