# 필요한 패키지 불러오기
from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

# SQUAlchemy 인스턴스화
db = SQLAlchemy()
# CSRF 인스턴스화
csrf = CSRFProtect()

# create_app 함수 생성
def create_app(config_key):
    # 플라스크 인스턴스(객체) 생성
    app = Flask(__name__)
    # config_key에 매치되는 환경의 config 클래스 읽어들임
    app.config.from_object(config[config_key])

    # # 앱의 config 설정
    # app.config.from_mapping(
    #     SECRET_KEY='GoogleCloudPlatform',
    #     SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # SQL을 콘솔 로그에 출력하는 설정
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY='qwer1234%'
    # )
    # SQLAlchemy와 앱 연계
    db.init_app(app)
    # CSRF와 앱 연계
    csrf.init_app(app)
    # Migrate와 앱 연계
    Migrate(app, db)
    # curd 패키지로부터 views를 import
    from apps.crud import views as crud_views
    # register_blueprint를 사용해 views의 crud를 앱에 등록
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    return app