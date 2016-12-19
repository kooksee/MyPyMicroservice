from pony.orm import Database

db = Database()
db.bind('mysql', host='192.168.200.23', user='admin', passwd='mypass', db='micro')
