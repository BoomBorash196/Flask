from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# основной файл для работы
app = Flask(__name__)
# наша база данных
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site1.db'
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
            return redirect("/posts")
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        # Заменяем значения в базе данных
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            # сохраняем
            db.session.commit()
            return redirect("/posts")
        except:
            return "При редактировании статьи произошла ошибка"
    else:

        return render_template('post_update.html', article=article)


@app.route('/posts/')
def posts():
    # обращаемся через определенную модель к базе данных
    # сортровкаа по дате / .all() # .all() чтобы получить все из базы данных
    articles = Article.query.order_by(Article.date.desc()).all()
    # articles это список
    # создаем ключевое имя articles и роботаем с ним
    return render_template('posts.html', articles=articles)


# обработка url адреса
@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('posts_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении статьи произошла ошибка"


if __name__ == "__main__":
    # Устанавливаем контекст приложения
    with app.app_context():
        # Создаем все таблицы в базе данных
        db.create_all()
    app.run(debug=True)
