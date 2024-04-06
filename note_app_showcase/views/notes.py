from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect  # Import CSRFProtect

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.models import Note, db

bp = Blueprint('notes_bp', __name__)


@bp.route('/')
def notes():
    user_id = session.get('user_id')
    if user_id:
        notes = Note.query.filter_by(user_id=user_id).all()
        return render_template('notes.html', notes=notes)
    else:
        flash('Musisz być zalogowany żeby przeglądać notatki', 'error')
        return redirect(url_for('login_bp.login'))


@bp.route('/add_note', methods=['GET', 'POST'])
def add_note():

    class AddNoteForm(FlaskForm):
        title = StringField('Title', validators=[DataRequired()])
        content = TextAreaField('Content', validators=[DataRequired()])
        submit = SubmitField('Add Note')
    
    form = AddNoteForm()
    
    if form.validate_on_submit():
        user_id = session.get('user_id')
        if user_id:
            title = form.title.data
            content = form.content.data
            
            new_note = Note(title=title, content=content, user_id=user_id)
            db.session.add(new_note)
            db.session.commit()
            flash('Dodano notatkę', 'success')
            return redirect(url_for('notes_bp.notes'))
        else:
            flash('Musisz być zalogowany żeby dodawać notatki', 'error')
            return redirect(url_for('login_bp.login'))
    return render_template('add_note.html', form=form)


@bp.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):

    class EditNoteForm(FlaskForm):
        title = StringField('Title', validators=[DataRequired()])
        content = TextAreaField('Content', validators=[DataRequired()])
        submit = SubmitField('Update Note')
    
    form = EditNoteForm()
    note = Note.query.get_or_404(note_id)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Note updated successfully', 'success')
        return redirect(url_for('notes_bp.notes'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content 

    return render_template('edit_note.html', form=form)

@bp.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    user_id = session.get('user_id')
    if user_id:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
    else:
        flash('Usunięto notatkę', 'error')
        return redirect(url_for('login_bp.login'))
    return redirect(url_for('notes_bp.notes'))
