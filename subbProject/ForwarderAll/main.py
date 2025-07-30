from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import requests
import io
import uvicorn
from urllib.parse import urlencode

app = FastAPI()


@app.api_route("/{subpath:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def forward_request(subpath: str, request: Request):
    """
    转发请求到目标服务器
    Args:
        subpath: 目标服务器的路径
        request: 客户端的请求
    Returns:
        目标服务器的响应
    """
    forward_ip = "172.25.3.70"
    port = 899

    # Extract query parameters and encode them
    query_params = request.query_params
    query_string = urlencode({k: v for k, v in query_params.items()})

    # Construct the target URL with query parameters
    url = f"http://{forward_ip}:{port}/{subpath}"
    if query_string:
        url += f"?{query_string}"

    print(url)
    headers = {key: value for key, value in request.headers.items()}  # Use client request headers
    data = await request.body()  # Use client request body
    print(request.method)
    print(headers)
    print(data)

    # Forward the request to the target URL
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
