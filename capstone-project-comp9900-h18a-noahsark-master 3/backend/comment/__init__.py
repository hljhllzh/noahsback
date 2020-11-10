# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import Blueprint

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

from . import comment_api

