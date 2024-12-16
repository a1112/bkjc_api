import io

import requests
from flask import Flask, request, send_file
import config
app = Flask(__name__)


@app.route('/', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/<path:subpath>')
def forward_request(subpath):
    url = config.forward_url + subpath  # 目标服务器的URL
    headers = request.headers  # 使用客户端的请求头
    data = request.data  # 使用客户端发送的数据
    response = requests.request(request.method, url, headers=headers, data=data)
    if "image" in response.headers['content-type']:
        return send_file(
            io.BytesIO(response.content),
            mimetype='image/jpg'
        )
    return response.content, response.status_code, response.headers.items()
