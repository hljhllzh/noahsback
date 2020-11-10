# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask import Blueprint

blocklist_bp = Blueprint('blocklist', __name__, url_prefix='/blocklist')

from . import blocklist_api

