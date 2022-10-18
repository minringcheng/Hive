from flask import Flask
from flask import Flask, jsonify, request
import json
import requests

监听端口 = 3001
模块类型 = "下载器"

app = Flask(__name__)


@app.route("/")
def hello_hive():
    return "<p>该"+模块类型+"连接正常，监听"+str(监听端口)+"端口。</p><p>轻量化分布式爬虫框架——Hive</p>"


@app.route('/示例', methods=['POST'])
def demo():
    任务包 = json.loads(request.get_data())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(任务包['链接'], headers=headers, timeout=5)
        response.encoding = response.apparent_encoding if response.encoding == 'ISO-8859-1' else response.encoding
        print("状态码:", response.status_code)
        任务包['内容'] = response.text
    except Exception as e:
        print("下载链接源码失败")
        任务包['内容'] = ""
    return 任务包


if __name__ == '__main__':
    app.run(debug=True, port=监听端口)
