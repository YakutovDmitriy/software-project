

class SongsDB:
  __slots__ = ['songs']

  def __init__(self, dbfile):
    def toword(s):
      return ''.join(filter(str.isalnum, s))
    self.songs = []
    for line in dbfile:
      line = line.strip()
      words = line.split()
      words = filter(lambda x: len(x) > 0, words)
      words = list(map(toword, words))
      self.songs.append(words)

  def get_songs(self, template):
    for words in self.songs:
      cur = list(map(len, words))
      if cur == template:
        yield ' '.join(words)
