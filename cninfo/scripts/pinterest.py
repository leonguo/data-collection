# -*- coding: UTF-8 -*-

from selenium import webdriver
import time


def main():
    # You most certainly want to change this
    url = "https://www.pinterest.com/login/?referrer=home_page"
    print  url
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 selenium.py")
    browser = webdriver.Firefox(profile, executable_path='E:\js\geckodriver.exe')
    browser.get(url)
    time.sleep(1)

    # The element names will likely be different for your application,
    # therefore change accordingly
    user = browser.find_element_by_name("id")
    password = browser.find_element_by_name("password")
    # Clear the input fields
    user.clear()
    password.clear()
    user.send_keys("hotman8168@gmail.com")
    password.send_keys("hotman8168com")
    time.sleep(1)
    browser.find_element_by_css_selector('button.red.SignupButton.active').click()

    # Keep the page loaded for 8 seconds
    time.sleep(5)

    print(browser.current_url)
    browser.get(browser.current_url)
    content = browser.page_source
    print content
    browser.close()

if __name__ == '__main__':
    main()
