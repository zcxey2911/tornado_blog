from peewee import Model, DateTimeField
from datetime import datetime
import peewee_async
import peewee

# 这里mytest和root分别指代数据库名称以及用户和密码
database = peewee_async.PooledMySQLDatabase("blog",host="localhost",port=3306,user="root",password="root")

# 建立基础类

class BaseModel(Model):
    create_time = DateTimeField(default=datetime.now, verbose_name="添加时间", help_text='添加时间')
    update_time = DateTimeField(default=datetime.now, verbose_name='更新时间', help_text='更新时间')

    def save(self, *args, **kwargs):
        if self._pk is None:
            self.create_time = datetime.now()
        self.update_time = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    

    class Meta:
        database = database

# 文章类
class Article(BaseModel):
    
    id = peewee.BigIntegerField(primary_key=True, unique=True,
            constraints=[peewee.SQL('AUTO_INCREMENT')])
    
    title = peewee.CharField(null=False,verbose_name='文章标题', help_text='文章标题')
    
    content = peewee.CharField(null=False,verbose_name='文章内容', help_text='文章内容')
    
    class Meta:
        db_table = "article"


if __name__ == "__main__":

    Article.create_table(True)

    Article.create(title="测试数据1",content="测试数据1")
    Article.create(title="测试数据2",content="测试数据2")