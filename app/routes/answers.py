from flask import Blueprint, request, jsonify
from app.models import db, Answer
from datetime import datetime

answers_blp = Blueprint("answers", __name__, url_prefix="/submit")

@answers_blp.route("", methods=["POST"])
def submit_answers():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"message": "요청 형식이 올바르지 않습니다. 리스트로 보내주세요."}), 400

    created_user_id = None

    for item in data:
        user_id = item.get("user_id")
        choice_id = item.get("choice_id")

        if user_id is None or choice_id is None:
            return jsonify({"message": "user_id 또는 choice_id가 없습니다."}), 400

        answer = Answer(user_id=user_id, choice_id=choice_id, created_at=datetime.utcnow())
        db.session.add(answer)

        created_user_id = user_id

    db.session.commit()

    return jsonify({"message": f"User: {created_user_id}'s answers Success Create"})