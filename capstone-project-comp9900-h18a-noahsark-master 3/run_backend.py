# -*- coding: utf-8 -*-
from backend import create_app


if __name__ == '__main__': 
    
    app = create_app('config.ProductionConfig') 
    use_debugger = app.debug and not(app.config.get('DEBUG_WITH_APTANA')) 
    app.run(use_debugger=use_debugger, debug=app.debug, use_reloader=use_debugger, host="127.0.0.1")