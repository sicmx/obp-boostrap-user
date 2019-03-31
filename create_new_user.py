import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
import time 

def create_new_user():
  # Get geko driver if not present
  if os.path.isfile('./geckodriver') is False:
    subprocess.run("./get-geckodriver.sh")
    

  OBP_HOST = os.getenv('OBP_HOST', False)
  OBP_PASSWORD = os.getenv('OBP_PASSWORD', False)
  OBP_USERNAME = os.getenv('OBP_USERNAME', False)
  OBP_EMAIL = os.getenv('OBP_EMAIL', False)
  OBP_FIRSTNAME = os.getenv('OBP_FIRSTNAME', False)
  OBP_LASENAME = os.getenv('OBP_LASENAME', False)

  options = Options()
  options.headless = False

  fp = webdriver.FirefoxProfile()

  browser = webdriver.Firefox(firefox_profile=fp, options=options, executable_path='./geckodriver')

  browser.get(OBP_HOST + '/user_mgt/sign_up');

  firstnameElm = browser.find_element_by_id('txtFirstName')
  lastnameElm = browser.find_element_by_id('txtLastName')
  emailElm = browser.find_element_by_id('txtEmail')
  usernameElm = browser.find_element_by_id('txtUsername')
  passwordElms = browser.find_elements_by_css_selector('input[type="password"]')
  password1Elm = passwordElms[0]
  password2Elm = passwordElms[1]

  ## Fill form
  firstnameElm.send_keys(OBP_FIRSTNAME)
  lastnameElm.send_keys(OBP_LASENAME)
  emailElm.send_keys(OBP_EMAIL)
  usernameElm.send_keys(OBP_USERNAME)
  password1Elm.clear()
  password1Elm.send_keys(OBP_PASSWORD)
  password2Elm.clear()
  password2Elm.send_keys(OBP_PASSWORD)
  ## Submit form
  password2Elm.send_keys(Keys.RETURN)

if __name__ == '__main__':
  create_new_user()

