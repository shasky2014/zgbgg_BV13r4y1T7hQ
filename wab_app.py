import json

from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

# app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql/web_database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class idols(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    height = db.Column(db.Integer)
    age = db.Column(db.Integer)
    shows = db.Column(db.String(200))

    def __init__(self, name=None, height=None, age=None, shows=None):
        self.name = name
        self.height = height
        self.age = age
        self.shows = shows

    def __str__(self):
        return json.dumps({'name': self.name,
                           'height': self.height,
                           'age': self.age,
                           'shows': self.shows,
                           })


@app.route('/table/')
def table_demo():
    return render_template('table_demo.html')


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/')
def home():
    all_info = idols.query.all()
    return render_template('home.html', idols=all_info)


@app.route('/home_layui')
def home_layui():
    # all_info = idols.query.all()
    # , idols=all_info
    return render_template('home-layui.html')


@app.route('/bootstrap')
def bootstrap_demo():
    return render_template('bootstrap.html')


@app.route('/modal_demo', methods=['GET', 'POST'])
def modal_demo():
    print('modal_demo fun')
    if request.method == 'POST':
        # print(json.loads(request.data))
        print(request.path)
        print(request.data)
        print(request.form)
        print(request)
    return redirect(url_for('home'))
    pass


@app.route('/select', methods=['GET', 'POST'])
def select():
    print('select', 1, request.method)
    if request.method == 'POST':
        print(request.path)
        print(request.data)
        print(request.form)
        return idols.query.all()
    else:
        print(request.args)
        # 获取pagination对象
        page = int(request.args.get('page'))
        per_page = int(request.args.get('limit'))
        where_id = request.args.get('id', None)
        where_age = request.args.get('age', None)
        print( set(request.args))
        if {'id', 'age'} & set(request.args):
            wheres = {}
            if where_id:
                wheres['id'] = int(where_id)
            if where_age:
                wheres['age'] = int(where_age)
            pagination = idols.query.filter_by(**wheres).paginate(page, per_page=per_page, error_out=False)
            _count = idols.query.filter_by(**wheres).count()
        else:
            pagination = idols.query.paginate(page, per_page=per_page, error_out=False)
            _count = len(idols.query.all())

        posts = [{"id": x.id, "name": x.name, "height": x.height, "age": x.age, "shows": x.shows} for x
                 in pagination.items]
        return {'data': posts, 'count': _count, 'msg': '', 'code': 0}


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    print('insert', 1)
    if request.method == 'POST':
        print(request.form)

        name = request.form['name']
        height = request.form['height']
        age = request.form['age']
        shows = request.form['shows']
        insert_data = idols(name, height, age, shows)
        print(name, height, age, shows)
        db.session.add(insert_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    delete_data = idols.query.get(id)
    print(delete_data)
    db.session.delete(delete_data)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    print('update fun', 1)
    if request.method == 'POST':
        print(request.form)
        update_id = request.form['id']
        update_info = idols.query.get(update_id)

        update_info.name = request.form['name']
        update_info.height = request.form['height']
        update_info.age = request.form['age']
        update_info.shows = request.form['shows']
        print(request.form)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.context_processor
def inject_enumerate():
    """
    # https://stackoverflow.com/questions/27035728/flask-cannot-import-enumerate-undefinederror-enumerate-is-undefined
    # 在html的for循环中用到enumerate，需要先在flask引入这个函数
    """
    return dict(enumerate=enumerate)


if __name__ == '__main__':
    app.run(debug=True)
