from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# основной файл для работы
app = Flask(__name__)
# наша база данных
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site1.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Article(db.Model):
    # уникальный айди
    id = db.Column(db.Integer, primary_key=True)
    # заголовок
    title = db.Column(db.String(100), nullable=False)
    # вступительный текст
    intro = db.Column(db.String(256), nullable=False)
    # текст статьи
    text = db.Column(db.Text, nullable=False)
    # дата публикации, по дефолту время публикации
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            # Добавляем инфу в базу данных
            # добавляем
            db.session.add(article)
            # сохраняем
            db.session.commit()
            return redirect("/")
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')


if __name__ == "__main__":
    app.run(debug=True)
