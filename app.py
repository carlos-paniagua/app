from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db' #データベースURI設定
db = SQLAlchemy(app)
    
class Post(db.Model): #データベースのテーブル設定
    id = db.Column(db.Integer,primary_key=True)
    food_name = db.Column(db.String(30),nullable=False)
    cost = db.Column(db.Integer)
    weight = db.Column(db.Intenger)
    count = db.Column(db.Intenger)
    due = db.Column(db.DateTime,nullable=False)
    category = db.Column(db.String(30),nullable=False)
    save_type = db.Column(db.String(30))
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def index():
    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)