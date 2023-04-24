from flask import Flask, render_template, redirect, request, url_for, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.questions import QuestionsForm
from forms.user import RegisterForm, LoginForm
from data.questions import Questions
from data.users import User
from data import db_session
import sqlite3
from PIL import Image
from io import BytesIO

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run(port = 5000, host = '127.0.0.1')


@app.route('/map')
@login_required
def map():
    con = sqlite3.connect("db/blogs.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM questions""").fetchall()
    result = result[0][1:-1]
    result = [result]
    print(result)
    con.close()
    if result[0][0] == 'да' and result[0][1] == 'да' and result[0][2] == 'да':
        return render_template('map1.html', coord_theatre_1 = [55.760278, 37.618611], coord_nature_1 = [55.73133, 37.60328],
                               coord_dost_1 = [55.75167, 37.61778])
    if result[0][0] == 'нет' and result[0][1] == 'нет' and result[0][2] == 'нет':
        return render_template('map11.html', coord_theatre_1=[], coord_nature_1=[],
                               coord_dost_1=[])
    if result[0][0] == 'да' and result[0][1] == 'да' and result[0][2] == 'нет':
        return render_template('map2.html', coord_theatre_1 = [55.760278, 37.618611], coord_dost_1 = [55.75167, 37.61778],
                               coord_thatre_2 = [55.756741, 37.6016])
    if result[0][0] == 'да' and result[0][1] == 'нет' and result[0][2] == 'да':
        return render_template('map3.html', coord_dost_1=[55.75167, 37.61778], coord_nature_1=[55.73133, 37.60328],
                               coord_dost_2=[55.7435, 37.618778])
    if result[0][0] == 'нет' and result[0][1] == 'да' and result[0][2] == 'да':
        return render_template('map5.html', coord_nature_2 = [55.79901400, 37.67481600], coord_thatre_1 = [55.760278, 37.618611],
                               coord_nature_1 = [55.73133, 37.60328])
    if result[0][0] == 'да' and result[0][1] == 'нет' and result[0][2] == 'нет':
        return render_template('map10.html', coord_dost_1 = [55.75167, 37.61778], coord_dost_2 = [55.7435, 37.618778],
                               coord_dost_3 = [55.725972, 37.556583])
    if result[0][0] == 'нет' and result[0][1] == 'да' and result[0][2] == 'нет':
        return render_template('map4.html', coord_theatre_1 = [55.760278, 37.618611], coord_thatre_2 = [55.756741, 37.6016],
                               coord_theatre_3 = [55.74361, 37.65389])
    if result[0][0] == 'нет' and result[0][1] == 'нет' and result[0][2] == 'да':
        return render_template('map7.html', coord_nature_1 = [55.73133, 37.60328], coord_nature_2 = [55.79901400, 37.67481600],
                               coord_nature_3 = [55.831388, 37.629277])
    return




@app.route('/ques', methods=['GET', 'POST'])
@login_required
def add_ques():
    db_sess = db_session.create_session()
    ques = db_sess.query(Questions).filter(Questions.id == 1).first()
    if ques:
        db_sess.delete(ques)
        db_sess.commit()
    form = QuestionsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ques = Questions()
        ques.que1 = form.que1.data
        ques.que2 = form.que2.data
        ques.que3 = form.que3.data
        current_user.ques.append(ques)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('ques.html', form=form)


@app.route('/ques_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def ques_delete(id):
    db_sess = db_session.create_session()
    ques = db_sess.query(Questions).filter(Questions.id == id, Questions.user == current_user).first()
    if ques:
        db_sess.delete(ques)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/ques/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ques(id):
    form = QuestionsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        ques = db_sess.query(Questions).filter(Questions.id == id, Questions.user == current_user).first()
        if ques:
            form.que1.data = ques.que1
            form.que2.data = ques.que2
            form.que3.data = ques.que3

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ques = db_sess.query(Questions).filter(Questions.id == id, Questions.user == current_user).first()
        if ques:
            ques.que1 = form.que1.data
            ques.que2 = form.que2.data
            ques.que3 = form.que3.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('ques.html', title='Редактирование новости', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        ques = db_sess.query(Questions).filter(Questions.user == current_user)
    else:
        ques = db_sess.query(Questions)
    return render_template("index.html", ques=ques)


@app.route('/register', methods=['GET', 'POST'])
def reqister():

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/file_upload', methods=['POST', 'GET'])
def file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Загрузка своей картинки</title>
                          </head>
                          <body>
                            <h1>Загрузим картинку</h1>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        data = f.read()
        im = Image.open(BytesIO(data))
        im.save('static/img/result.{im_format}'.format(im_format=im.format))
        img = Image.open('static/img/result.{im_format}'.format(im_format=im.format))
        img.save('static/img/result.png')
        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
