from flask import Blueprint, request, jsonify
from app.models import db, Image

images_blp = Blueprint("images", __name__, url_prefix="/image")


@images_blp.route("", methods=["POST"])
def create_image():
    data = request.get_json()

    url = data.get("url")
    image_type = data.get("type")

    if not url or not image_type or image_type not in ["main", "sub"]:
        return jsonify({"message": "유효한 'url'과 'type' 값이 필요합니다."}), 400

    new_image = Image(url=url, type=image_type)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": f"ID: {new_image.id} Image Success Create"}), 200