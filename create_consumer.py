import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
import time 

def create_consumer():
  # Get geko driver if not present
  if os.path.isfile('./geckodriver') is False:
    subprocess.run("./get-geckodriver.sh")
    

  OBP_API_HOST = os.getenv('OBP_API_HOST', False)
  OBP_PASSWORD = os.getenv('OBP_PASSWORD', False)
  OBP_USERNAME = os.getenv('OBP_USERNAME', False)
  OBP_EMAIL = os.getenv('OBP_EMAIL', False)
  OBP_FIRSTNAME = os.getenv('OBP_FIRSTNAME', False)
  OBP_LASENAME = os.getenv('OBP_LASENAME', False)

  options = Options()
  options.headless = False

  fp = webdriver.FirefoxProfile()

  browser = webdriver.Firefox(firefox_profile=fp, options=options, executable_path='./geckodriver')

  # Login using credentials
  browser.get(OBP_API_HOST + '/user_mgt/login');

  usernameElm = browser.find_element_by_id('username')
  passwordElm = browser.find_element_by_id('password')
  ## Fill in login form
  usernameElm.send_keys(OBP_USERNAME)
  passwordElm.send_keys(OBP_PASSWORD)
  ## Submit form (login)
  passwordElm.send_keys(Keys.RETURN)

  time.sleep(2)
  # Create new consumer
  browser.get(OBP_API_HOST + '/consumer-registration');
  id="appName"
  appNameElm = browser.find_element_by_id('appName')
  redirectUrlElm = browser.find_element_by_id('appRedirectUrl')
  emailElm = browser.find_element_by_id('appDev')
  descElm = browser.find_element_by_id('appDesc')
  # Fill in new consumer form
  appNameElm.send_keys('bootstrap')
  emailElm.send_keys(OBP_EMAIL)
  descElm.send_keys('...')
  time.sleep(2)
  #Submit
  emailElm.send_keys(Keys.RETURN)
  time.sleep(2)

  # Extract auth key and 
  consumerKey = browser.find_element_by_id('auth-key').text
  consumerSecret = browser.find_element_by_id('secret-key').text

  os.environ['OBP_CONSUMER_KEY'] = consumerKey

  with open('consumerKey.txt', 'w') as fp:
    fp.write(consumerKey)
  with open('consumerSecret.txt', 'w') as fp:
    fp.write(consumerSecret)

  browser.quit()

if __name__ == '__main__':
  create_consumer()
