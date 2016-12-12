from tornado import web


class CmdHandle(object):
    def ping(self):
        return "ok"

    def spider(self, *urls):
        from cmd_spider.service.cmd_action import save_tags, save_headers
        for url in urls:
            save_tags(url)
            save_headers()

    def get_tags(self, tags):
        def __get_tags(*tags):
            from pony.orm import db_session, select
            from cmd_spider.db.model import Tag
            from pony.orm.serialization import to_json
            with db_session:
                for t in select(t for t in Tag if t.tag_name in tags):
                    yield to_json(t)

        return list(__get_tags(*tags))

    def get_headers(self, urls):
        def __get_headers(*urls):
            from pony.orm import db_session, select
            from cmd_spider.db.model import Header
            from pony.orm.serialization import to_json
            with db_session:
                for h in select(h for h in Header if h.blog_url in urls):
                    yield to_json(h)

        return list(__get_headers(*urls))



