import datetime
import forms
import models
from flask import Flask, g, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'jsbndknjsdsdfnksdnfkjsdn.asasdjanbsdkjasbd'


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    entries = models.JournalEntries.select().order_by(
        models.JournalEntries.date.desc())
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
    """ creates a new entry """
    form = forms.NewEntries()
    if form.validate_on_submit():
        models.JournalEntries.add_entries(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resourses=form.resourses.data
        )
        flash('Entry succesfully saved!', 'succes')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def detail_entries(id):
    """takes an individual entry """
    try:
        entry = models.JournalEntries.select().where(
            models.JournalEntries.id == id).get()
    except models.DoesNotExist:
        return redirect(url_for('index'))
    return render_template('detail.html', entry=entry)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_entries(id):
    """Lets you edit your entries """
    form = forms.NewEntries()
    try:
        entry = models.JournalEntries.select().where(
            models.JournalEntries.id == id).get()
    except models.DoesNotExist:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        models.JournalEntries.update(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resourses=form.resourses.data,
        ).where(models.JournalEntries.id == id).execute()
        flash('Everything went well!', 'succes')
        return redirect(url_for('detail_entries', id=id))
    return render_template('edit.html', entry=entry, form=form)


@app.route('/entries/<int:id>/delete')
def delete_entries(id):
    """Deletes entries """
    try:
        entry = models.JournalEntries.select().where(
            models.JournalEntries.id == id).get()
    except models.DoesNotExist:
        return redirect(url_for('index.html'))
    entry.delete_instance()
    entry.save()
    flash('Your entry was deleted!')
    return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()
    if models.JournalEntries.select().count() == 0:
        models.JournalEntries.add_entries(
            title='My first Flask website.',
            time_spent=15,
            learned='Learned to make my first website!',
            resourses='teamtreehouse',
            date=datetime.datetime.today()
        )
    app.run(debug=True)
