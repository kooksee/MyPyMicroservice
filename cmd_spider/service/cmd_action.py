# -*- coding:utf-8 -*-

from gevent import monkey
from pony.orm import db_session, select

from cmd_spider.db.model import Tag

monkey.patch_all()

import sys

from bs4 import BeautifulSoup
from gevent.pool import Pool

reload(sys)
sys.setdefaultencoding('utf-8')

import requests

import logging

logger = logging.getLogger()


def parse_tags(url=None):
    from cmd_spider.settings import BASE_BLOG_PAGE
    _url = url or BASE_BLOG_PAGE

    res = requests.get(_url)
    bs = BeautifulSoup(res.text, 'lxml')
    tags = bs.select('#file-list .tag-list')
    for tag in tags:
        links = tag.select('.file-item.item a')
        yield dict(
            tag_name=tag.select_one('.tag-item.item .tag-name').text,
            tag_count=tag.select_one('.tag-item.item .tag-count').text,
            tag_links=[dict(
                link_href=link.attrs.get("href"),
                link_name=link.text.strip(' |\n|\b')
            ) for link in links]
        )


def save_tags(url=None):
    from cmd_spider.db.model import Tag

    for tag in parse_tags(url):
        with db_session:
            try:
                t = select(t for t in Tag if t.tag_name == tag['tag_name']).first()
                links = t.tag_links
                for link in tag['tag_links']:
                    if link not in links:
                        links.append(link)
                t.tag_links = links
            except Exception, e:
                logger.debug(e)
                Tag(**tag)


def get_links():
    from cmd_spider.db.model import Tag

    with db_session:
        for links in select(t.tag_links for t in Tag):
            for link in links:
                yield link.get('link_href')


def __parse_header(url=None):
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    blog_metas = bs.select('#reader-full-topInfo code')

    __data = dict(
        blog_url=url,
        author=blog_metas[0].text.strip(' |\n|\b'),
        article_updated_date=blog_metas[1].select_one(".article-updated-date").text.strip(' |\n|\b'),
        article_characters=blog_metas[2].select_one(".article-characters").text.strip(' |\n|\b'),
        article_read=blog_metas[3].select_one(".article-read").text.strip(' |\n|\b')
    )

    header = bs.select('#wmd-preview [data-anchor-id]')
    title = header[0]
    __data.update(dict(
        title=title.text.strip(' |\n|\b') or url
    ))

    tags = header[1]
    if tags.name == 'p':
        __data.update(dict(
            tags=tags.text.strip(' |\n|\b').split(" ")
        ))

    return __data


def save_headers():
    from cmd_spider.db.model import Header
    for header in Pool().imap_unordered(__parse_header, get_links()):
        with db_session:
            try:
                h = select(h for h in Header if h.blog_url == header['blog_url']).first()
                h.set(**header)
            except Exception, e:
                logger.debug(e)
                Header(**header)


if __name__ == '__main__':
    import time

    start_time = time.time()

    # save_tags()
    save_headers()

    with db_session:
        for t in select(t for t in Tag if t.tag_name == u'面试'):
            print t.tag_links

    end_time = time.time()

    print "耗时:{}".format(end_time - start_time)

    pass
