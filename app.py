from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db' #データベースURI設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
    
class Post(db.Model): #データベースのテーブル設定
    __tablename__ = 'food_info'
    id = db.Column(db.Integer,primary_key=True)
    food_name = db.Column(db.String(30),nullable=False)
    cost = db.Column(db.Integer)
    # weight = db.Column(db.Integer)
    # count = db.Column(db.Integer)
    due = db.Column(db.DateTime,nullable=False)
    # category = db.Column(db.String(30),nullable=False)
    # save_type = db.Column(db.String(30))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        posts = Post.query.all()    #データベースからすべての情報を取りだし，トップページに渡す
        return render_template("index.html",posts=posts)
    
    else:
        food_name = request.form.get("food_name")
        cost = request.form.get("cost")
        # weight = request.form.get("weight")
        # count =  request.form.get("count")
        due = request.form.get("due")
        # category = request.form.get("category")
        # save_type = request.form.get("save_type")
        
        due = datetime.strptime(due,"%Y-%m-%d")
        new_post = Post(food_name=food_name,cost=cost,due=due)
        
        db.session.add(new_post) #内容を追加
        db.session.commit() #反映
        return redirect("/")

@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)