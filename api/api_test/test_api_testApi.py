from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from PIL import Image

app = FastAPI()
client = TestClient(app)
"""
TestClient 的作用是模拟客户端，用于测试 FastAPI 应用程序。
TestClient的使用方法：
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
response = client.get("/items/foo")
assert response.status_code == 200
assert response.json() == {"item_id": "foo", "q": None}

pytest.fixture的作用是为测试用例提供一个预设的测试环境，比如测试数据库的连接，测试数据的准备等。
fixture的使用方法：
@pytest.fixture
def client():
    client = TestClient(app)
    return client
def test_read_item(client):
    response = client.get("/items/foo")
    assert response.status_code == 200
    assert response.json() == {"item_id": "foo", "q": None}

"""
@pytest.fixture
def test_image(tmp_path):
    # Create a test image file
    image_path = tmp_path / "test_image.jpg"
    image = Image.new("RGB", (100, 100), color="red")
    image.save(image_path)
    return image_path

def test_get_file_exists(test_image):
    # Test the getFile endpoint when the file exists
    response = client.get(f"/file/{test_image}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.content == open(test_image, "rb").read()

def test_get_file_not_exists():
    # Test the getFile endpoint when the file does not exist
    response = client.get("/file/nonexistent.jpg")
    assert response.status_code == 200
    assert response.json() == {"文件不存在 !"}

def test_get_file_count(test_image):
    # Test the get_file_count endpoint
    response = client.get(f"/img/count/{test_image}")
    assert response.status_code == 200
    assert response.json() == 1

def test_get_all_join_file(test_image):
    # Test the get_all_join_file endpoint
    response = client.get(f"/img/join/{test_image}")
    assert response.status_code == 200
    # Add assertions for the expected response

def test_get_cimg_exists(test_image):
    # Test the getCimg endpoint when the file exists
    response = client.get(f"/img/{test_image}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    # Add assertions for the expected response

def test_get_cimg_not_exists():
    # Test the getCimg endpoint when the file does not exist
    response = client.get("/img/nonexistent.jpg")
    assert response.status_code == 200
    assert response.json() == {"msg": "文件不存在 !", "code": 404}

def test_cimg():
    # Test the cimg endpoint
    response = client.get("/cimg/0/0/0/4096")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    # Add assertions for the expected response

def test_upload_file():
    # Test the upload_file endpoint
    response = client.post("/upload/")
    assert response.status_code == 200
    assert response.json() == {"info": "file 'None' saved at './uploaded_files/None'"}  

def test_download_file():
    # Test the download_file endpoint when the file exists
    response = client.get("/download/test_image.jpg")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.content == open("test_image.jpg", "rb").read()  

def test_download_file_not_exists():
    # Test the download_file endpoint when the file does not exist
    response = client.get("/download/nonexistent.jpg")
    assert response.status_code == 200
    assert response.json() == {"error": "File not found"}

def test_get_steel_info():
    # Test the get_steel_info endpoint
    response = client.get("/steel_info/123456")
    assert response.status_code == 200
    # Add assertions for the expected response 

def test_get_camera_info():
    # Test the get_camera_info endpoint
    response = client.get("/info")
    assert response.status_code == 200
    # Add assertions for the expected response

def test_get_image_count():
    # Test the get_image_count endpoint
    response = client.get("/count/123456/1")
    assert response.status_code == 200
    # Add assertions for the expected response
# 生成全部测试：
# pytest -v -s --html=report.html --self-contained-html test_api.py
# 生成指定测试：
# pytest -v -s --html=report.html --self-contained-html test_api.py::test_get_file_exists
# 生成指定测试类：
# pytest -v -s --html=report.html --self-contained-html test_api.py::TestApi
# 生成指定测试类的指定测试方法：
# pytest -v -s --html=report.html --self-contained-html test_api.py::TestApi::test_get_file_exists
# 生成指定测试类的指定测试方法：
# pytest -v -s --html=report.html --self-contained-html test_api.py::TestApi::test_get_file_exists
# 生成指定测试类的指定测试方法：
# pytest -v -s --html=report.html --self-contained-html test_api.py::TestApi::test_get_file_exists
    