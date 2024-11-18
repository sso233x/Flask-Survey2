from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key' 

@app.route('/')
def start_page():
    """Display the survey start page with title, instructions, and start button."""
    return render_template("start.html", survey=satisfaction_survey, title=satisfaction_survey.title)

@app.route('/start', methods=["POST"])
def start_survey():
    """Initialize the responses list in the session and redirect to the first question."""
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/questions/<int:question_id>')
def question_page(question_id):
    """Display the current question."""
    responses = session.get("responses", [])
    
    if len(responses) != question_id:
        flash("You are trying to access an invalid question.")
        return redirect(f"/questions/{len(responses)}")

    if question_id >= len(satisfaction_survey.questions):
        return redirect('/thank-you')

    question = satisfaction_survey.questions[question_id]
    return render_template("questions.html", question=question, question_id=question_id, survey=satisfaction_survey, title="Question")

@app.route('/answer', methods=["POST"])
def handle_answer():
    """Handle the answer submission and redirect to the next question."""
    choice = request.form['answer']
    responses = session.get("responses", [])
    responses.append(choice)
    session["responses"] = responses

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect('/thank-you')

@app.route('/thank-you')
def thank_you_page():
    """Display the thank-you page after the survey is completed."""
    return render_template("thankyou.html", survey=satisfaction_survey, title="Thank You")
