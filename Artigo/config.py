import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/artigo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APISPEC_SPEC = APISpec(
        title='Artigo API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_UI_URL = '/swagger/'
    APISPEC_SWAGGER_URL = '/swagger.json'
