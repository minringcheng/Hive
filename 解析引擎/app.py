from flask import Flask
from flask import Flask, jsonify, request
import json
from bs4 import BeautifulSoup

监听端口 = 4001
模块类型 = "解析器"

app = Flask(__name__)


@app.route("/")
def hello_hive():
    return "<p>该"+模块类型+"连接正常，监听"+str(监听端口)+"端口。</p><p>轻量化分布式爬虫框架——Hive</p>"


@app.route('/示例', methods=['POST'])
def demo():
    任务包 = json.loads(request.get_data())
    任务包['标题'] = str(BeautifulSoup(任务包['内容'], 'lxml').title.string)
    任务包.pop("内容")  # 后续任务中不需要此处的源码数据,将其清除可以降低传输的无效数据量
    return 任务包


if __name__ == '__main__':
    app.run(debug=True, port=监听端口)
