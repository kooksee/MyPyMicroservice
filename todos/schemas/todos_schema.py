# -*- coding:utf-8 -*-
from cerberus import Validator


class TodosForm(object):
    v = Validator({
        'name': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
        'group': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
        'message': {'type': 'string', 'required': False},
        'is_done': {'type': 'integer', "allowed": [1, 0], 'nullable': False,'required': False},
    })

    def validate(self, datas):
        for data in datas:
            status, error = self.v.validate(data), self.v.errors
            if not status:
                return status, error

        return True, None


if __name__ == '__main__':
    t = TodosForm()
    print t.validate({
        'name': 'john',
        'group': 'john',
    })
    pass
