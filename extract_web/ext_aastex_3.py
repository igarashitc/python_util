import os
import signal
import time
import traceback
import re

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def main():

  print("read http links from input bib file")
  links = ext_http("MWC297_2023.bib")
  #for link in links:
  # print(link)
  
  print("write http links to text file")
  with open("bib_http.txt", "w") as file:
    for line in links:
      file.write(line+"\n")

  print("extract aastex")
  ext_aastex(links)

def ext_http(bib_file):

  http_links = []
  
  with open(bib_file, "r", encoding='utf-8') as file:

    for line in file:
      match = re.search(r"url\s*=\s*{(http[^}]+)}", line)
      if match:
        http_links.append(match.group(1)+"/exportcitation")

  return http_links

def ext_aastex(links): 
  
  driver = webdriver.Chrome()
 
  for link in links:
    print(link)
    driver.get(link)

    time.sleep(5)
    for _ in range(20):
      try:
        dropdown = driver.find_element(By.ID, "ex-dropdown")
      except NoSuchElementException:
        print("An exception occur.")
        print(traceback.format_exc())
        print("wait for loading.")
        time.sleep(5)
      else:
        print("Complete")
        break
    else:
      print("Page loading time out")
      break 
    select   = Select(dropdown)

    # select AASTEX drop down menu.
    select.select_by_index(13)

    # extraxt text
    time.sleep(1)
    for _ in range(30):
      try:
        txt = driver.find_element(By.CLASS_NAME, "export-textarea")
      except NoSuchElementException:
        print("An exception occur.")
        print(traceback.format_exc())
        print("wait for loading.")
        time.sleep(2)
      else:
        print("Load aastex complete:", txt.text)
        break
    else:
      print("AASTEX loading time out")
      break

    #with open("bib_aastex.tex", "a") as file:
    #  file.write(txt.text+"\n")


if __name__ == '__main__':
  main()


