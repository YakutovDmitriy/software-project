
def main():
  lines = []
  was = set()
  with open('db.txt') as db:
    for line in db:
      line = ' '.join(line.strip().split())
      if len(line) > 0 and not (line.lower() in was):
        was.add(line.lower())
        lines.append(line)
  lines.sort()
  with open('new_db.txt', 'w') as db:
    for line in lines:
      print(line, file=db)

if __name__ == '__main__':
  main()
