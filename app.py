from flask import Flask, g, render_template_string
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'mydb.sqlite3')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

@app.route('/')
def index():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS visits (count INTEGER)')
    db.execute('INSERT INTO visits (count) VALUES (1)')
    db.commit()
    count = db.execute('SELECT COUNT(*) FROM visits').fetchone()[0]
    return render_template_string('<h1>Visitss: {{ count }}</h1>', count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
