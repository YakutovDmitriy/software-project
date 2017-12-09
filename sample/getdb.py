from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
import time
import re

def good(s):
  s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii')
  s = re.sub(r'\(.*\)', '', s)
  s = re.sub(r'\,|\!|\.|\'|\/|\?|\*|\"', '', s)
  s = re.sub(r'\&', ' and ', s)
  s = re.sub(r'\-|\:|\;', ' ', s)
  s = ' '.join(s.strip().split())
  return s

def main():
  driver = webdriver.Chrome(in_files('chromedriver.exe'))
  for direc in [-1, 1]:
    for page in range(1, 257):
      driver.get('https://www.thesongclash.com/en/song-list?page=%d&sorting=artist&direction=%d&filter=active' % (page, direc))
      time.sleep(2)
      table = driver.find_elements_by_tag_name("table")[0]
      tbody = table.find_elements_by_tag_name("tbody")[0]
      if tbody != None:
        with open(in_temps('downloads/song_in_%d_%d') % (page, direc), 'w') as f:
          for elem in tbody.find_elements_by_tag_name("tr"):
            tds = elem.find_elements_by_tag_name("td")
            artist = tds[0].find_elements_by_tag_name("a")[0].find_elements_by_tag_name("span")[0].text
            song = tds[1].find_elements_by_tag_name("a")[0].text
            artist = good(artist)
            song = good(song)
            print(artist, song, file=f)
            print("%d: %s - %s" % (page, artist, song))
      else:
        print("Break %d" % page)
        break

if __name__ == '__main__':
  main()
