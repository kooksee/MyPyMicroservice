# -*- coding:utf-8 -*-

import logging

from pony.orm import db_session, select, delete
from tornado import web

from todos.db.model import Todo
from todos.schemas.todos_schema import TodosForm

logger = logging.getLogger()

import json


class TodosHandler(web.RequestHandler):
    def post(self):

        if __debug__:
            print self.request.body

        import json

        _data = json.loads(self.request.body)

        status, error = TodosForm().validate(_data)
        if not status:
            self.write({
                "status": "failed",
                "msg": error
            })
            self.finish()

        with db_session:
            for _d in _data:
                Todo(**_d)

        self.write({
            "status": "ok",
            "msg": u"创建成功"
        })

    def get(self):
        ids = self.get_argument("ids", "")
        if ids:
            ids = ids.split(",")
        if __debug__:
            print ids
        fields = self.get_argument("fields", [])

        with db_session:
            if not ids:
                _data = [{"id": t.id, "name": t.name, "group": t.group, "message": t.message, "is_done": t.is_done} for
                         t in select(t for t in Todo)[:]]
            else:
                _data = [{"id": t.id, "name": t.name, "group": t.group, "message": t.message, "is_done": t.is_done} for
                         t in select(t for t in Todo if t.id in ids)[:]]

            if __debug__:
                print _data
            self.write({
                "status": "ok",
                "data": _data,
                "msg": ""
            })
            self.finish()

    def delete(self):
        ids = json.loads(self.request.body).get("ids",[])

        if __debug__:
            print ids

        with db_session:
            if not ids:
                delete(t for t in Todo)
            else:
                delete(t for t in Todo if t.id in ids)
            self.write({
                "status": "ok",
                "msg": u"删除成功"
            })


class TodoHandler(web.RequestHandler):
    def put(self, id=None):
        with db_session:
            if Todo.exists(id=id):
                __d = self.request.body
                __d = json.loads(__d)
                t = Todo[id]
                t.set(**__d)
                self.write({
                    "status": "ok",
                    "msg": u"修改成功"
                })
            else:
                self.write({
                    "status": "failed",
                    "msg": u"{}不存在".format(id)
                })
            self.finish()

    def get(self, id=None):

        if __debug__:
            print id

        with db_session:
            t = select(t for t in Todo if t.id == id).first()
            if not t:
                self.write({
                    "status": "failed",
                    "msg": u"{}不存在".format(id)
                })
                self.finish()

            self.write({
                "status": "ok",
                "data": {
                    "id": t.id, "name": t.name, "group": t.group, "message": t.message, "is_done": t.is_done
                },
                "msg": ""
            })
            self.finish()
