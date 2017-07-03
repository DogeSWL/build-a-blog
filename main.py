from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

def get_blogList():
    return Blog.query.all()

@app.route("/newpost")
def newpost_page():
    return render_template('newpost.html')


@app.route('/blog')
def blogPage():

    return render_template('blog.html',blogList=get_blogList())

@app.route("/")
def index():
    return redirect('/blog')


if __name__ == "__main__":
    app.run()
