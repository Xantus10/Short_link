from flask import Flask, render_template, request, send_from_directory, redirect
from os import path
import re

# TODO: add support for other protocols

app = Flask(__name__)


def indexToLetters(ix: int) -> str:
  ix = str(ix)
  letters = ''
  for n in ix:
    letters += chr(ord(n) + 49)
  letters = 'a' * (5-len(letters)) + letters
  return letters


def lettersToIndex(letters: str) -> int:
  num = ''
  try:
    for c in letters:
      num += chr(ord(c) - 49)
    return int(num)
  except:
    return -1


def getCurrentIndex() -> int:
  with open('./data/urls.txt', 'r') as f:
    currentIx = len(f.read().splitlines())
  return currentIx


def getUrlByIndex(ix: int) -> str:
  with open('./data/urls.txt', 'r') as f:
    fileContents = f.read().splitlines()
  if (ix < len(fileContents)):
    return fileContents[ix]
  return ''


def validateUrl(url: str) -> str:
  if not re.search('^.*www\..*$', url):
    url = 'www.' + url
  if not re.search('^http.*www\..*', url):
    url = 'https://' + url
  return url


def writeUrl(url: str) -> None:
  valurl = validateUrl(url)
  with open('./data/urls.txt', 'a') as f:
    f.write(valurl+'\n')


def makeShort(toShortUrl: str) -> str:
  short = indexToLetters(getCurrentIndex())
  writeUrl(toShortUrl)
  return short


def getOriginal(shortUrl: str) -> str:
  ix = lettersToIndex(shortUrl)
  if ix < 0:
    return ''
  url = getUrlByIndex(ix)
  return url


@app.route('/u/<short>')
def unshortenUrl(short):
  redirectUrl = getOriginal(short)
  if redirectUrl:
    return redirect(redirectUrl)
  return render_template('urlNotExist.html')


@app.route('/shortened', methods=['POST'])
def shortenUrl():
  toShortUrl = request.form.get('url')
  url = makeShort(toShortUrl)
  return render_template('shortened.html', before=toShortUrl, after=f'localhost/u/{url}')


@app.route('/favicon.ico')
def favicon():
  return send_from_directory(path.join(app.root_path, 'static/icon'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


def main():
  app.run(port=80)


if __name__ == '__main__':
  main()
