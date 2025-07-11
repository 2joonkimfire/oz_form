from flask import Blueprint, jsonify
from app.models import db, Question, Choice, Image
from flask import request

questions_blp = Blueprint("questions", __name__, url_prefix="/questions")

@questions_blp.route("/<int:question_sqe>", methods=["GET"])
def get_question(question_sqe):
    question = Question.query.filter_by(sqe=question_sqe).first()
    if not question:
        return jsonify({"message": "해당 질문이 존재하지 않습니다."}), 404

    image = Image.query.get(question.image_id)

    choices = Choice.query.filter_by(question_id=question.id).all()
    choice_list = [
        {
            "id": c.id,
            "content": c.content,
            "is_active": c.is_active,
            "sqe": c.sqe,
            "question_id": c.question_id
        }
        for c in choices
    ]

    return jsonify({
        "id": question.id,
        "title": question.title,
        "image": image.url if image else None,
        "choices": choice_list
    })

@questions_blp.route("/count", methods=["GET"])
def get_question_count():
    total = Question.query.count()
    return jsonify({"total": total})


@questions_blp.route("", methods=["POST"])
def create_question():
    data = request.get_json()

    title = data.get("title")
    is_active = data.get("is_active")
    sqe = data.get("sqe")
    image_id = data.get("image_id")

    if not title or type(is_active) is not bool or type(sqe) is not int or not image_id:
        return jsonify({"message": "유효한 title, is_active, sqe, image_id 값이 필요합니다."}), 400

    # 해당 image_id 존재 여부 확인
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"message": f"Image ID {image_id}가 존재하지 않습니다."}), 400

    new_question = Question(
        title=title,
        is_active=is_active,
        sqe=sqe,
        image_id=image_id
    )
    db.session.add(new_question)
    db.session.commit()

    return jsonify({"message": f"Title: {title} question Success Create"}), 200