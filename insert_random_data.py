import json
import random

from wab_app import idols


from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql/web_database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

def random_unicode():
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)


class random_idols(idols):

    def random(self):
        self.name = ''.join([random_unicode() for x in range(random.randint(3, 4))])
        self.shows = ''.join([random_unicode() for x in range(random.randint(3, 9))])
        self.age = random.randrange(18, 35)
        self.height = random.randrange(160, 190)
        return self


if __name__ == '__main__':
    for x in range(1000):
        a = random_idols()
        a = a.random()
        db.session.add(a)
        db.session.commit()
        print(json.loads(a.__str__()))
