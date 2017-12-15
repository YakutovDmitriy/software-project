from .tools import in_files
import re
from selenium import webdriver
import sys
import time
import unicodedata


def simplify_string(s):
  s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii')
  s = re.sub(r'\(.*\)', '', s)
  s = re.sub(r'\,|\!|\.|\'|\/|\?|\*|\"', '', s)
  s = re.sub(r'\&', ' and ', s)
  s = re.sub(r'\-|\:|\;', ' ', s)
  s = ' '.join(s.strip().split())
  return s


class DBUpdater:

  __slots__ = ['pages', 'directions', 'songs', 'time_to_sleep']

  def __init__(self, pages, directions, time_to_sleep):
    self.pages = pages
    self.directions = directions
    self.time_to_sleep = time_to_sleep

  def get_songs(self):
    self.songs = []
    driver = webdriver.Chrome(in_files('chromedriver.exe'))
    for direc in self.directions:
      for page in self.pages:
        driver.get('https://www.thesongclash.com/en/song-list?page=%d&sorting=artist&direction=%d&filter=active' % (page, direc))
        time.sleep(self.time_to_sleep)
        table = driver.find_elements_by_tag_name("table")[0]
        tbody = table.find_elements_by_tag_name("tbody")[0]
        if tbody != None:
          for elem in tbody.find_elements_by_tag_name("tr"):
            tds = elem.find_elements_by_tag_name("td")
            artist = tds[0].find_elements_by_tag_name("a")[0].find_elements_by_tag_name("span")[0].text
            song = tds[1].find_elements_by_tag_name("a")[0].text
            artist = simplify_string(artist)
            song = simplify_string(song)
            print("%d: %s - %s" % (page, artist, song), file=sys.stderr)
            self.songs.append((artist, song))
        else:
          print("Break %d" % page, file=sys.stderr)
          break

  def safe_songs(file):
    for (artist, song) in self.songs:
      print(artist, song, file=file)


def main():
  updater = DBUpdater(pages=range(1, 257), directions=[-1, 1], time_to_sleep=2)
  updater.get_songs()
  with open(in_temps('downloads/new_db.txt'), 'w') as new_db:
    updater.safe_songs(new_db)


if __name__ == '__main__':
  main()
