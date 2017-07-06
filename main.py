from flask import Flask, request, redirect, flash, render_template
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

    def __init__(self, title, body):
        self.title = title
        self.body = body

def get_blogList():
    return Blog.query.all()

@app.route('/addBlog', methods=['POST'])
def add_Blog():
    new_blogTitle = request.form['blog_Title']
    new_blogEntry = request.form['blog_NewEntry']

    title_Error = ''
    entry_Error = ''

    if new_blogTitle == '':
        title_Error = 'Title is empty'
    if new_blogEntry == '':
        entry_Error = 'Entry is empty'

    if (title_Error != '') or (entry_Error != ''):
        return render_template('newpost.html',
                                title_Error = title_Error,
                                entry_Error = entry_Error)
    else:
        blog = Blog(title=new_blogTitle, body=new_blogEntry)
        db.session.add(blog)
        db.session.commit()

        # lastID = db.session.query(Blog.id).order_by(Blog.id.desc()).first()
        #
        # for curID in lastID:
        #     return redirect('/blog?id'+str(curID))
        return redirect('/blog?id='+str(blog.id))

@app.route("/newpost")
def newpost_page():
    return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blogPage():
    some_id = request.args.get('id') # extract the value of id
    if some_id == None: # if value of id returns None render template blog.html
        return render_template('blog.html',blogList=get_blogList())
    else:
        oneBlog = Blog.query.filter_by(id=some_id).all()
        return render_template('singleBlog.html', indBlog=oneBlog)

@app.route("/")
def index():
    return redirect('/blog')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'


if __name__ == "__main__":
    app.run()
