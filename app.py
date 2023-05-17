from flask import Flask, render_template, request, redirect, url_for
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
    
    #データベースにタスクを保存
    if request.method == "GET":
        #データベースからすべての情報を取りだし，トップページに渡す
        posts = Post.query.order_by(Post.due).all() #期限が近い順
        return render_template("index.html",posts=posts)
    
    #保存されているタスクを表示する
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
        return redirect("/") #トップページへリダイレクト

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
   
    post = Post.query.get(id) # 該当するidの投稿内容を取得
    return render_template("detail.html",post=post) # 、タスクをdetail.htmlに渡す

@app.route("/delete/<int:id>")
def delete(id):
    post = Post.query.get(id) # 該当するidの投稿内容を取得
    db.session.delete(post)   #内容削除
    db.session.commit()     #反映
    return redirect("/")    #トップページへリダイレクト
    
@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    post = Post.query.get(id)
    
    #今まで書かれていた内容を表示
    if request.method == "GET":
        return render_template("update.html",post=post)
    
    #変更内容を更新する
    else:
        post.food_name=request.form.get("food_name")
        post.cost=request.form.get("cost")
        post.due=datetime.strptime(request.form.get("due"),"%Y-%m-%d")
        
        db.session.commit()
        return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)