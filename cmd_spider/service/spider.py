# -*- coding:utf-8 -*-

from gevent import monkey

from cmd_spider.settings import BASE_BLOG_PAGE

monkey.patch_all()

import sys

from bs4 import BeautifulSoup
from gevent.pool import Pool

from cmd_spider.db.models import tdb, TbName

reload(sys)
sys.setdefaultencoding('utf-8')

import requests


def parse_tags():
    res = requests.get(BASE_BLOG_PAGE)
    bs = BeautifulSoup(res.text, 'lxml')
    tags = bs.select('#file-list .tag-list')
    for tag in tags:
        links = tag.select('.file-item.item a')
        yield dict(
            tag_name=tag.select_one('.tag-item.item .tag-name').text,
            tag_count=tag.select_one('.tag-item.item .tag-count').text,
            tag_links=[dict(link_href=link.attrs.get("href"), link_name=link.text.strip(' " "|\n|\b')) for link in
                       links]
        )


def get_links():
    for tag in tdb.table(TbName.Tags).all():
        for link in tag.get("tag_links"):
            yield link.get('link_href')


def __parse_header(url=BASE_BLOG_PAGE):
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    blog_metas = bs.select('#reader-full-topInfo code')

    __data = dict(
        blog_url=url,
        author=blog_metas[0].text.strip(' " "|\n|\b'),
        article_updated_date=blog_metas[1].select_one(".article-updated-date").text.strip(' " "|\n|\b'),
        article_characters=blog_metas[2].select_one(".article-characters").text.strip(' " "|\n|\b'),
        article_read=blog_metas[3].select_one(".article-read").text.strip(' " "|\n|\b')
    )

    header = bs.select('#wmd-preview [data-anchor-id]')
    title = header[0]
    __data.update(dict(
        title=title.text.strip(' " "|\n|\b')
    ))

    tags = header[1]
    if tags.name == 'p':
        __data.update(dict(
            tags=tags.text.strip(' " "|\n|\b').split(" ")
        ))

    return __data


def parse_headers():
    return (a for a in Pool().imap_unordered(__parse_header, get_links()))


def save_tags():
    tdb.purge_table(TbName.Tags)
    tdb.table(TbName.Tags).insert_multiple(parse_tags())


def save_headers():
    tdb.purge_table(TbName.Headers)
    tdb.table(TbName.Headers).insert_multiple(parse_headers())


if __name__ == '__main__':
    import time

    start_time = time.time()

    save_tags()
    save_headers()

    end_time = time.time()

    print "耗时:{}".format(end_time - start_time)

    pass
