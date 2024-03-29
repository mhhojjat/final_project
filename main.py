from crawler import Crawl
from database import sqlite
from tokenizer import tokenize


def main():
    a = Crawl('https://www.sanjesh.org/')
    data = a.crawl(start_url='https://www.sanjesh.org/group.aspx?gid=1')

    insert_to_doc = 'insert into documents(link) values (?)'
    insert_to_term = 'insert into terms(term, doc_id, tf) values (?, ?, ?)'
    for d in data:
        url = d.get('url')
        if sqlite.select(f"select id from documents where link = '{url}'"):
            continue
        doc_id = sqlite.execute(insert_to_doc, (url,))
        texts = d.get('text')
        if texts is not None:
            for text in texts:
                terms = tokenize.execute(text.text)
                for term in terms:
                    sqlite.execute(insert_to_term, (term['term'], doc_id, term['tf']))


if __name__ == '__main__':
    main()
