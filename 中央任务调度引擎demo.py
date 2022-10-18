import json
import uuid
import requests
"""
 __    __   __  ____    ____  _______ 
|  |  |  | |  | \   \  /   / |   ____|
|  |__|  | |  |  \   \/   /  |  |__   
|   __   | |  |   \      /   |   __|  
|  |  |  | |  |    \    /    |  |____ 
|__|  |__| |__|     \__/     |_______|

Hive是一个轻量化的分布式爬虫框架，目前还很简陋。

Hive由中央任务调度引擎和下载引擎、解析引擎、存储引擎组成。
中央任务调度引擎：负责组织任务的相关信息并将其发送至三大引擎以实现需求
下载引擎：负责下载网页的源码等信息
解析引擎：负责从源码中解析出需要的数据
存储引擎：负责将相关数据持久化存储

任务包：任务包是Hive系统中存储一个抓取任务的相关信息的json字符串，这个任务包会在中央调度引擎的调度之下在各个引擎中流转。
引擎间通讯方式：各个引擎之间通过http协议传输任务包的json字符串来进行通讯，这也意味着可以使用任何语言编写各个引擎，不同语言编写的引擎可以融合在一个系统中工作
分布式：三大引擎完全独立，可以在一台机器部署多个引擎，也可以在多台机器上部署同一种引擎，然后由任务所属的中央调度引擎依据自己的业务逻辑按需调用
"""


# 可用的各引擎模块连接信息
下载引擎 = ["http://127.0.0.1:3001"]
解析引擎 = ["http://127.0.0.1:4001"]
存储引擎 = ["http://127.0.0.1:5001"]

'''
任务调度引擎初始化在各引擎间以json格式传输的任务包
任务包uuid是使用uuid算法生成的任务包唯一id
下载器名、解析器名、存储器名是各个引擎中的单个处理模块的名称，也是各自监听的http请求url中的参数
链接是该任务需要爬取的链接
'''
任务包 = {
    "任务包uuid": str(uuid.uuid1()),
    "下载器名": "示例",
    "解析器名": "示例",
    "存储器名": "示例",
    "链接": "https://www.baidu.com/",
}

# 在任务正式开始前，将任务包的信息打印出来，供后续比对
print("任务开始前的任务包:", 任务包)
# 任务包发往下载引擎下载数据
响应 = requests.post(url=下载引擎[0]+"/"+任务包['下载器名'],
                   headers={'Content-Type': 'application/json'}, data=json.dumps(任务包))
# 下载引擎完成自己的业务逻辑，将网页源码写入任务包然后将任务包返回，此处把下载引擎返回的任务包再格式化成dict类型
任务包 = json.loads(响应.text)
# 任务包被发往解析引擎，解析引擎从中解析出所需的数据，此处示例解析引擎中解析出的数据是源码中的title
响应 = requests.post(url=解析引擎[0]+"/"+任务包['解析器名'],
                   headers={'Content-Type': 'application/json'}, data=json.dumps(任务包))
# 解析引擎返回的任务包格式化
任务包 = json.loads(响应.text)
# 任务包发往存储引擎，示例存储引擎只将解析引擎解析出的‘标题’数据进行输出，并未持久化存储
响应 = requests.post(url=存储引擎[0]+"/"+任务包['解析器名'],
                   headers={'Content-Type': 'application/json'}, data=json.dumps(任务包))
# 存储引擎返回的任务包格式化
任务包 = json.loads(响应.text)
# 在任务包经过一系列的处理之后，将任务包打印出来供对比
print("任务结束后的任务包:", 任务包)
