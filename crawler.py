import requests
from bs4 import BeautifulSoup


class Crawl:
    def __init__(self, url):
        self.base_url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'cdn.tsetmc.com',
            'Cookie': '_ga=GA1.2.553521183.1654344437; _gid=GA1.2.1496477247.1654344437; ASP.NET_SessionId=t2iz14vn5em2dijnfoa3wyh0',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate'}

    def crawl(self, start_url=None):
        contents = []
        url = start_url if start_url else self.base_url

        links = self.get_and_select(url, ['#bodyLeft > div > div.boxMiddle > div > ul > li > a'])
        for link in links:
            try:
                content_url = self.base_url + link.attrs.get('href')
                resp = requests.get(content_url)
                soup = BeautifulSoup(resp.text, 'html.parser')
                p_contents = soup.find_all('p')

                for content in p_contents:
                    if content:
                        contents.append({'url': content_url, 'text': content})
            except Exception as e:
                print(e)
        return contents

    @staticmethod
    def get_and_select(url, selectors: list):
        data = []
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        for selector in selectors:
            data.extend(soup.select(selector))

        return data if data else None


if __name__ == '__main__':
    a = Crawl('https://www.sanjesh.org/')
    a.crawl(start_url='https://www.sanjesh.org/group.aspx?gid=12')
