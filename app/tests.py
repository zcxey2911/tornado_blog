import requests

if __name__ == "__main__":

    #添加文章
    data = {'title':'test123','content':'101010'}
    r = requests.post("http://127.0.0.1:8000/article/",data = data)
    print(r.text)

    # # 修改文章
    # data = {'id':1,'content':'修改文章内容'}
    # r = requests.put("http://127.0.0.1:8000/article/",data = data)
    # print(r.text)

    # 删除文章
    # r = requests.delete("http://127.0.0.1:8000/article/?id=2")
    # print(r.text)