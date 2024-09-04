from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import requests
import io

from core import app, default_forwarder_server_dict, ForwarderServer

import forwarder_api


@app.api_route("/{forward_ip}/{port}/{subpath:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS",
                                                               "HEAD"])
async def forward_request(forward_ip: str, port: str, subpath: str, request: Request):
    """
    转发请求到目标服务器
    Args:
        forward_ip: 目标服务器的 IP
        port: 目标服务器的端口
        subpath: 目标服务器的路径
        request: 客户端的请求
    Returns:
        目标服务器的响应
    """
    url = "http://" + forward_ip + f":{port}/" + subpath  # 目标服务器的 URL
    print(url)
    headers = {key: value for key, value in request.headers.items()}  # 使用客户端的请求头
    data = await request.body()  # 使用客户端发送的数据
    print(request.method)
    print(headers)
    print(data)
    # 将请求转发到目标 URL
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=data
    )

    print(response.content)
    if "image" in response.headers.get('content-type', ''):
        return StreamingResponse(
            io.BytesIO(response.content),
            media_type='image/jpg'
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )


@app.get("/set_forward_config")
async def set_forward_config(forward_ip: str, port: str, request: Request):
    """
    设置默认的转发目标
    Args:
        request:
        forward_ip: 目标服务器的 IP
        port: 目标服务器的端口

    Returns:
        设置成功的消息
    """
    from_path = request.client.host
    default_forwarder_server_dict[from_path] = ForwarderServer(forward_ip, port)
    return {"message": "forwarder set successfully to " + forward_ip + " : " + port}


@app.get("/get_forward_config")
async def get_forward_config(request: Request):
    """
    获取默认的转发目标
    Returns:
        默认的转发目标
    """
    return default_forwarder_server_dict[request.client.host].__dict__


@app.get("/get_forward_table")
def get_forward_table(request: Request):
    """
    获取转发表
    Returns:
        转发表
    """
    return default_forwarder_server_dict


@app.api_route("/forward/{subpart:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def forward(subpath: str, request: Request):
    """
    转发请求到默认的目标服务器
    Args:
        subpath:  目标服务器的路径
        request:  客户端的请求

    Returns:
        目标服务器的响应
    """
    forward_ip = default_forwarder_server_dict[request.client.host].ip
    forward_port = default_forwarder_server_dict[request.client.host].port
    if forward_ip is None:
        return {"message": "forwarder not set"}
    return await forward_request(forward_ip, forward_port, subpath, request)
