import tornado.ioloop
import tornado.web

import peewee
import peewee_async

import aioredis
import asyncio

from app import article
from app.models import Article
from app.base import BaseHandler
from app.models import database

from playhouse.shortcuts import model_to_dict
import json

def json_model(model):
    return model_to_dict(model)


class MainHandler(BaseHandler):

    async def get(self):

        # 获取分页参数
        page = int(self.get_argument("page",1))
        size = int(self.get_argument("size",2))

        # 异步读取文章
        articles = await self.application.objects.execute(Article.select().paginate(page,size))
        # 序列化操作
        articles = [json_model(x) for x in articles]

        self.render("index.html",articles=articles)
        
        #self.finish({"code":200,"data":articles})

urlpatterns = [
    (r"/", MainHandler)
]

urlpatterns += article.urlpatterns

import os

# 创建Tornado实例
application = tornado.web.Application(urlpatterns,template_path=os.path.join(os.path.dirname(__file__), "templates"),debug=True)

# pewee数据库对象注入Tornado实例
application.objects = peewee_async.Manager(database)


async def redis_pool(loop):
    
    return await aioredis.create_redis_pool('redis://localhost', minsize=1, maxsize=10000, encoding='utf8', loop=loop)

#loop = asyncio.get_event_loop()
#application.redis = loop.run_until_complete(redis_pool(loop))

application.json_model = json_model

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()