# -*- coding:utf-8 -*-

import json

from pony.orm import db_session, delete, select
from pony.orm.serialization import to_dict

from project.db.model import Template, Project


class ProjectHandle(object):
    def add_projects(self, projects):

        with db_session:
            projects = json.loads(projects)

            for project in projects:
                program = project.get("program")
                process_name = project.get("process_name")
                command = project.get("command")
                numprocess = int(project.get("numprocess"))
                port = int(project.get("port"))

                if Template.exists(program=program):
                    return json.dumps(dict(
                        msg="program:{0}已经存在".format(program),
                        status="fail"
                    ))

                Template(**project)

                for i in range(numprocess):
                    Project(
                        program=program,
                        process_name=process_name.format(port=i),
                        command=command.format(port=i + port),
                        port=i + port
                    )

            return json.dumps(dict(
                status="ok",
                msg=""
            ))

    def remove_projects(self, programs):
        with db_session:
            try:
                programs = json.loads(programs)

                delete(p for p in Template if p.program in programs)
                delete(p for p in Project if p.program in programs)

                return json.dumps(dict(
                    status="ok",
                    msg=""
                ))
            except Exception, e:
                return json.dumps(dict(
                    status="fail",
                    msg=e.message
                ))

    def get_projects(self, data):
        from misc import gen_fields

        print data

        data = json.loads(data)

        programs = data.get("programs", [])
        fields = data.get("fields", [])

        with db_session:
            if programs or fields:
                res = eval("select({0} for p in Project {1})".format(
                    gen_fields('p', fields),
                    "" if not programs else "if p.program in programs"
                ))
            else:
                res = select(p for p in Project)

            _data = res[:] if programs or fields else res.first()
            if __debug__:
                print res.get_sql()
                print to_dict(_data)

            try:
                return json.dumps(dict(
                    status="ok",
                    data=to_dict(_data)
                ))
            except Exception, e:
                return json.dumps(dict(
                    status="fail",
                    msg=e.message
                ))

    def update_project(self, data):
        with db_session:
            try:

                data = json.loads(data)
                program = data.get("program")
                del data["program"]

                Template[program].set(**data)

                delete(p for p in Project if p.program == program)

                process_name = data.get("process_name")
                command = data.get("command")
                numprocess = int(data.get("numprocess"))
                port = int(data.get("port"))
                for i in range(numprocess):
                    Project(
                        program=program,
                        process_name=process_name.format(port=i),
                        command=command.format(port=i + port),
                        port=i + port
                    )

                return json.dumps(dict(
                    status="ok",
                    msg=""
                ))
            except Exception, e:
                return json.dumps(dict(
                    status="fail",
                    msg=e.message
                ))

    def do_actions(self, data):
        data = json.loads(data)
        programs = data.get("programs", [])
        actions = data.get("actions", [])
        if __debug__:
            print data
            print programs, actions

        from project_action import start, stop, restart
        for action in actions:
            print action
            if action == u"start":
                start(programs)
            elif action == u"stop":
                stop(programs)
            elif action == u"restart":
                restart(programs)
            else:
                return json.dumps(dict(
                    status=u'fail',
                    msg=u'命令不正确'
                ))
        return json.dumps(dict(
            status='ok',
            msg=action
        ))

    def ping(self):
        return "ok"


if __name__ == '__main__':
    pass

'''
db.insert("Person", name="Ben", age=33, returning='id')

x = "John"
data = db.select("* from Person where name = $x")

data = db.select("* from Person where name = $x", {"x" : "Susan"})

data = db.select("* from Person where name = $(x.lower()) and age > $(y + 2)")

select(c for c in Customer).order_by(Customer.name).limit(10)

g = Group[101]
g.students.filter(lambda student: student.gpa > 3)[:]

g.students.order_by(Student.name).page(2, pagesize=3)

g.students.order_by(lambda s: s.name).limit(3, offset=3)

Query.random()

select(p for p in Product if p.price > 100).for_update()

@db_session(retry=3)
def your_function():
    ...

update(p.set(price=price * 1.1) for p in Product if p.category.name == "T-Shirt")

delete(p for p in Product if p.category.name == "Floppy disk")
'''
