import os
from core import configApp as app
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
import config

app.mount("/static", StaticFiles(directory=config.get_path("files/static")), name="static")


@app.get("/doc", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Returns the Swagger UI HTML page with customized settings.

    Returns:
        str: The HTML page for Swagger UI.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    """
    Returns the HTML page for Swagger UI OAuth2 redirect.

    Returns:
        str: The HTML page for Swagger UI OAuth2 redirect.
    """
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """
    Returns the ReDoc HTML page with customized settings.

    Returns:
        str: The HTML page for ReDoc.
    """
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )