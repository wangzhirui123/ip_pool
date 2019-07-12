# -*- coding: utf-8 -*-
__author__ = 'Px'

from tornado import web,ioloop
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Index(web.RequestHandler):

    def get(self, *args, **kwargs):
        print self.request.remote_ip
        self.write(self.request.remote_ip)

app = web.Application(
    [
        (r'/',Index),
    ]
)
app.listen(80)
ioloop.IOLoop.instance().start()
