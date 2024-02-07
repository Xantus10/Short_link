from flask import Flask, render_template, request, send_from_directory, redirect
from os import path
import re

# TODO: add support for other protocols

# Flask app
app = Flask(__name__)


# Convert index to url letters
def indexToLetters(ix: int) -> str:
  ix = str(ix)
  letters = ''
  for n in ix:
    letters += chr(ord(n) + 49)
  letters = 'a' * (5-len(letters)) + letters
  return letters


# Convert url letters to index
def lettersToIndex(letters: str) -> int:
  num = ''
  try:
    for c in letters:
      num += chr(ord(c) - 49)
    return int(num)
  except:
    return -1


# Get the index, that comes now
def getCurrentIndex() -> int:
  with open('./data/urls.txt', 'r') as f:
    currentIx = len(f.read().splitlines())
  return currentIx


# Get the url, associated with index
def getUrlByIndex(ix: int) -> str:
  with open('./data/urls.txt', 'r') as f:
    fileContents = f.read().splitlines()
  if (ix < len(fileContents)):
    return fileContents[ix]
  return ''


# Validate the url (For redirect, the protocol has to be there)
def validateUrl(url: str) -> str:
  # If there is any protocol already specified
  if re.search('^.+://.*$', url):
    return url
  # Now there is no protocol so we assume it is website and check for www
  if not re.search('^www\..*$', url):
    url = 'www.' + url
  return 'https://' + url


# Write the url into a file
def writeUrl(url: str) -> None:
  valurl = validateUrl(url)
  with open('./data/urls.txt', 'a') as f:
    f.write(valurl+'\n')


# Make the url short
def makeShort(toShortUrl: str) -> str:
  short = indexToLetters(getCurrentIndex())
  writeUrl(toShortUrl)
  return short


# Get original url from short one
def getOriginal(shortUrl: str) -> str:
  ix = lettersToIndex(shortUrl)
  if ix < 0:
    return ''
  url = getUrlByIndex(ix)
  return url


# Route for redirections
@app.route('/u/<short>')
def unshortenUrl(short):
  redirectUrl = getOriginal(short)
  if redirectUrl:
    return redirect(redirectUrl)
  return render_template('urlNotExist.html')


# Route for result of shortening
@app.route('/shortened', methods=['POST'])
def shortenUrl():
  toShortUrl = request.form.get('url')
  url = makeShort(toShortUrl)
  return render_template('shortened.html', before=toShortUrl, after=f'localhost/u/{url}')


# Favicon
@app.route('/favicon.ico')
def favicon():
  return send_from_directory(path.join(app.root_path, 'static/icon'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Index
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


def main():
  app.run(port=80)


if __name__ == '__main__':
  main()
