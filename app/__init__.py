from flask import Flask, jsonify
from flask_migrate import Migrate

from app.routes import register_routes
from config import db

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)

		# 400 에러 발생 시, JSON 형태로 응답 반환
    @application.errorhandler(400)
    def handle_bad_request(error):
        response = jsonify({"message": error.description})
        response.status_code = 400
        return response
    
    # 👉 여기가 핵심: 블루프린트 등록
    register_routes(application)
    
    return application