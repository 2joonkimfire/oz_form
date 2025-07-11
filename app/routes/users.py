from flask import Blueprint, request, jsonify
from app.models import User
from config import db

user_blp = Blueprint("users", __name__)

@user_blp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    gender = data.get("gender")

    new_user = User(name=name, email=email, age=age, gender=gender)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": f"{name}님 회원가입을 축하합니다",
        "user_id": new_user.id
    }), 200