from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from core import testApp as app
client = TestClient(app)

def test_home():
    # Test the home endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "本服务主要用于请求图像，api接口可以访问 openapi.json， 文档请访问 /docs  或 /redoc"}

def test_getSteelInfo():
    # Test the getSteelInfo endpoint
    response = client.get("/steel_info?steelNo=123456")
    assert response.status_code == 200
    # Add assertions for the expected response

def test_getCameraInfo():
    # Test the getCameraInfo endpoint
    response = client.get("/info")
    assert response.status_code == 200
    # Add assertions for the expected response

def test_get_image_Count():
    # Test the get_image_Count endpoint without specifying cameraId
    response = client.get("/count?steelNo=123456")
    assert response.status_code == 200
    # Add assertions for the expected response

    # Test the get_image_Count endpoint with specifying cameraId
    response = client.get("/count?steelNo=123456&cameraId=1")
    assert response.status_code == 200
    # Add assertions for the expected response

def test_get_img_by_steelNo():
    # Test the get_img_by_steelNo endpoint
    response = client.get("/search?steelNo=123456&cameraId=1&resize=4096&start=0&end=0")
    assert response.status_code == 200
    # Add assertions for the expected response

# Add more tests as needed