
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import jsonify

common_bp = Blueprint('common', __name__)


@common_bp.route("/")
def index():
    return jsonify({"hello": "world"})
