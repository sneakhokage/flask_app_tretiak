from app import app, db

from app.posts.models import Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post}

if __name__ == '__main__':
    app.run(debug=True)