# all the imports
import os
from peewee import *
from sprinter.connectdatabase import ConnectDatabase
from sprinter.models import Entries
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='adam',
    PASSWORD='adam'
))
app.config.from_envvar('SPRINTER_SETTINGS', silent=True)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Entries], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
def list_entries():
    entries = Entries.select().order_by(Entries.id.desc())
    return render_template('list.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    new_entry = Entries.create(title=request.form['title'],
                               text=request.form['text'], acc_crit=request.form['acc_crit'],
                               bus_value=request.form['bus_value'], estimation=request.form['estimation'],
                               status=request.form['status'])
    new_entry.save()
    flash('New story was successfully added')
    return redirect(url_for('list_entries'))

@app.route('/update/<story_id>', methods=['POST'])
def update_entry(story_id):
    modif_entry = Entries.update(title=request.form['title'],
                               text=request.form['text'], acc_crit=request.form['acc_crit'],
                               bus_value=request.form['bus_value'], estimation=request.form['estimation'],
                               status=request.form['status']).where(Entries.id == story_id)
    modif_entry.execute()
    flash('Story was successfully modified')
    return redirect(url_for('list_entries'))

@app.route('/story')
def add_story():
    return render_template('form.html')


@app.route('/story/update/<story_id>', methods=['GET', 'POST'])
def update_story(story_id):
    entries = Entries.select().where(Entries.id == story_id)
    return render_template('form.html', entries=entries)


@app.route('/story/delete/<story_id>', methods=['GET'])
def delete_story(story_id):
    Entries.delete().where(Entries.id == story_id).execute()
    flash(story_id + "was deleted")
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(app.config['USERNAME'])
    print(app.config['PASSWORD'])
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('list_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
