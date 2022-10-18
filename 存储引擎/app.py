from flask import Flask
from flask import Flask, jsonify, request
import json

监听端口 = 5001
模块类型 = "存储器"

app = Flask(__name__)


@app.route("/")
def hello_hive():
    return "<p>该"+模块类型+"连接正常，监听"+str(监听端口)+"端口。</p><p>轻量化分布式爬虫框架——Hive</p>"


@app.route('/示例', methods=['POST'])
def demo():
    任务包 = json.loads(request.get_data())
    print(任务包['标题'])
    return 任务包


if __name__ == '__main__':
    app.run(debug=True, port=监听端口)
