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

@bp.route('/add_note', methods=['POST'])
def add_note():
    user_id = session.get('user_id')
    if user_id:
        title = request.form['title']
        content = request.form['content']
        
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        flash('Notatka usunięta', 'success')
        return redirect(url_for('notes_bp.notes'))
    else:
        flash('Musisz być zalogowany żeby usuwać notatki', 'error')
        return redirect(url_for('login_bp.login'))

@bp.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    user_id = session.get('user_id')
    if user_id:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
    else:
        flash('You must be logged in to delete notes', 'error')
        return redirect(url_for('login_bp.login'))
    return redirect(url_for('notes_bp.notes'))

