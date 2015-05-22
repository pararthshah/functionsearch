#!/usr/bin/python

import os, sys
import json

import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

import sys
import traceback

import conf
from sourcegraph import SourceGraph

class ImportHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=conf.MAX_WORKERS)    

    @run_on_executor
    def import_graph(self, body):
        sourcegraph = self.settings['sourcegraph']
        print body

        try:
            data = json.loads(body)
            if 'Path' in data:
                sourcegraph.add_node(data['Path'])
            elif 'Src' in data and 'Dst' in data:
                sourcegraph.add_edge(data['Src'], data['Dst'])
                sourcegraph.update_scores()
            else:
                return {'result': 'unknown data format'} 
            return {'result': 'ok'}
        except AssertionError:
            _, _, tb = sys.exc_info()
            tb_info = traceback.extract_tb(tb)
            return {'error': str(tb_info)}

    @tornado.gen.coroutine
    def post(self):
        res = yield self.import_graph(self.request.body)
        self.write(res)

class SearchHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, query):
        sourcegraph = self.settings['sourcegraph']

        paths = sourcegraph.get_ranked_paths(query)
        self.write({'result': paths})

if __name__ == "__main__":
    sourcegraph = SourceGraph()

    application = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': conf.STATIC_PATH}),
        (r"/import", ImportHandler),
        (r"/search/(.*)", SearchHandler)
    ], sourcegraph=sourcegraph)

    application.listen(conf.PORT)
    tornado.ioloop.IOLoop.instance().start()
