# -*- coding: utf-8 -*-

from flask import Blueprint

film_bp = Blueprint('film', __name__, url_prefix='/film')
GENRE = {"Action","Comedy","Horror","Music","Mystery","Romance","Sci-Fi","Spot","Thriller","War","Western","Crime"}
from . import film_api
