from flask import Blueprint, request, jsonify
from app.models import db, Choice, Question

choices_blp = Blueprint("choices", __name__, url_prefix="/choice")


@choices_blp.route("", methods=["POST"])
def create_choice():
    data = request.get_json()

    content = data.get("content")
    is_active = data.get("is_active")
    sqe = data.get("sqe")
    question_id = data.get("question_id")

    if not content or type(is_active) is not bool or type(sqe) is not int or not question_id:
        return jsonify({"message": "유효한 content, is_active, sqe, question_id 값이 필요합니다."}), 400

    # question_id 유효성 확인
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"message": f"Question ID {question_id}가 존재하지 않습니다."}), 400

    new_choice = Choice(
        content=content,
        is_active=is_active,
        sqe=sqe,
        question_id=question_id
    )
    db.session.add(new_choice)
    db.session.commit()

    return jsonify({"message": f"Content: {content} choice Success Create"}), 200