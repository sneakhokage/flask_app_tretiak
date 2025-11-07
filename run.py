import os
from app import create_app, db 
from app.posts.models import Post


app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    """
    Додає db та модель Post у контекст flask shell.
    """
    return {'db': db, 'Post': Post}

if __name__ == '__main__':
    app.run()