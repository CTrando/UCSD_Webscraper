import requests, bs4, os, pprint
from selenium import webdriver
from pdb import set_trace

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import DEPARTMENT
HTML_STORAGE = 'classes'

os.chdir('C:/Users/ctran/Downloads/chromedriver')

login = 'https://act.ucsd.edu/webreg2/start'
username = input('Enter your username')
password = input('Enter your password')

browser = webdriver.Chrome()
browser.set_page_load_timeout(30)

os.chdir('C:/Users/ctran/PycharmProjects/UCSD_Webscraper')

browser.get(login)
browser.find_element_by_id('ssousername').send_keys(username)
browser.find_element_by_id('ssopassword').send_keys(password)
try:
    browser.find_element_by_class_name('sso-button').submit()
except Exception:
    pass
try:
    submit = WebDriverWait(browser, 200).until(EC.presence_of_element_located(
        (By.ID, 'startpage-button-go')
    ))
    while browser.find_element_by_id('startpage-button-go'):
        submit = browser.find_element_by_id('startpage-button-go')
        submit.click()

except Exception:
    pass

try:
    class_search = WebDriverWait(browser, 200).until(EC.presence_of_element_located
                                                     ((By.ID, 's2id_autogen1')))
    class_search.click()
    class_search.send_keys(DEPARTMENT)
    class_search.send_keys(Keys.RETURN)

except Exception as e:
    print(e)
    pass

# now I should be at the course pages
page_ul = WebDriverWait(browser, 200).until(EC.presence_of_element_located
                                                     ((By.CLASS_NAME, 'jPag-pages')))
pages = page_ul.find_elements_by_tag_name('li')
for page in pages:
    current = browser.find_element_by_class_name('jPag-current').text
    print(current)
    print(page.text)
    if int(page.text) == int(current) + 1:
        page.click()
        print("Have clicked page", page.text)

    try:
        running = True
        while running:
            class_search = WebDriverWait(browser, 10).until(EC.presence_of_element_located
                                                            ((By.CLASS_NAME, 'ui-icon-circlesmall-plus')))
            class_search.click()
    except Exception as e:
        print(e)
        html = browser.page_source
        file = open(os.path.join(os.curdir, HTML_STORAGE, DEPARTMENT, page.text+'.html'), 'w')
        print(pprint.pformat(html))
        file.write(html)
        print(file.name)
        file.close()
        pass

