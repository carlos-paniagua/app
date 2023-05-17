from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db' #データベースURI設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Post(db.Model): #データベースのテーブル設定
    __tablename__ = 'food_info'
    id = db.Column(db.Integer,primary_key=True)
    food_name = db.Column(db.String(30),nullable=False)
    cost = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    count = db.Column(db.Integer)
    due = db.Column(db.DateTime,nullable=False)
    category = db.Column(db.String(30))
    save_type = db.Column(db.String(30))
    # image_path = db.Column(db.String(200))

@app.route('/', methods=['GET', 'POST'])
def index():
    
    #データベースにタスクを保存
    if request.method == "GET":
        #データベースからすべての情報を取りだし，トップページに渡す
        posts = Post.query.order_by(Post.due).all() #期限が近い順
        return render_template("index.html",posts=posts,today=date.today())
    
    #保存されているタスクを表示する
    else:
        food_name = request.form.get("food_name")
        cost = request.form.get("cost")
        weight = request.form.get("weight")
        count =  request.form.get("count")
        due = request.form.get("due")
        category = request.form.get("category")
        save_type = request.form.get("save_type")
        # image = request.files('image')
        
        # 画像を保存するパスを作成
        image_path = 'static/images/' + image.filename

        # 画像を指定のパスに保存
        image.save(image_path)
        
        due = datetime.strptime(due,"%Y-%m-%d")
        new_post = Post(food_name=food_name,cost=cost,weight=weight,count=count,due=due,category=category,save_type=save_type)#image_path=image_path
        
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
    app.run(host='0.0.0.0', port=5000) 
    
# from app import app,db
# with app.app_context():
#     db.create_all()