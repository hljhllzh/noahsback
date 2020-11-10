# -*- coding: utf-8 -*-

from flask import Blueprint

search_bp = Blueprint('search', __name__, url_prefix='/search')

from . import search