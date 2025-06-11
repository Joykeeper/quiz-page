from . import db

class Creator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    best_score = db.Column(db.Integer, default=0)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(20))  # "open" or "choice"
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text)

class QuizChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'))
    choice_text = db.Column(db.String(100))
    quiz_question = db.relationship('QuizQuestion', backref='choices')