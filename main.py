import html.parser
import urllib.request


def main():
    content_bs = http_get('computer')
    # print(content)
    print(parse_html(content_bs.decode()))


CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'


def http_get(word):
    url = 'https://dictionary.cambridge.org/dictionary/english-japanese/' + word
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': CHROME_USER_AGENT
        })
    with urllib.request.urlopen(req) as f:
        content = f.read()
    return content


class MyParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_trans = False
        self._words = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for (key, val) in attrs:
                if key == 'class' and val == 'def ddef_d db':
                    self._in_trans = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self._in_trans = False

    def handle_data(self, data):
        if self._in_trans:
            word = data.strip()
            if word:
                self._words.append(word)

    def get_trans(self):
        return ' '.join(self._words)


def parse_html(html):
    parser = MyParser()
    parser.feed(html)
    return parser.get_trans()


if __name__ == '__main__':
    main()
