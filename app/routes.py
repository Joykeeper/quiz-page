from flask import Blueprint, request, render_template, redirect, url_for
from .models import User, QuizQuestion, QuizChoice, db

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, best_score=0)
            db.session.add(user)
            db.session.commit()

        score = 0
        total = 0

        for question in QuizQuestion.query.all():
            total += 1
            answer = ""
            if question.question_type == "choice":
                answer = request.form.get(f"question{question.id}")
            elif question.question_type == "open":
                answer = request.form.get(f"question{question.id}").strip().lower()
            if answer and answer.strip().lower() == question.correct_answer.strip().lower():
                score += 1

        percent_score = int((score / total) * 100) if total > 0 else 0
        if percent_score > user.best_score:
            user.best_score = percent_score
            db.session.commit()
        return render_template("quiz.html", questions=QuizQuestion.query.all(), user=user, score=percent_score)

    return render_template("quiz.html", questions=QuizQuestion.query.all(), user=None)


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    questions = QuizQuestion.query.all()
    return render_template('admin/index.html', questions=questions)

@admin_bp.route('/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        q_type = request.form['question_type']
        q_text = request.form['question_text']
        correct_answer = request.form['correct_answer']

        question = QuizQuestion(question_type=q_type, question_text=q_text, correct_answer=correct_answer)
        db.session.add(question)
        db.session.commit()

        if q_type == 'choice':
            choices = request.form.getlist('choices')
            for choice_text in choices:
                db.session.add(QuizChoice(question_id=question.id, choice_text=choice_text))
            db.session.commit()

        return redirect(url_for('admin.index'))

    return render_template('admin/add_question.html')
