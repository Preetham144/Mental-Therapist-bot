from flask import Flask, render_template, request, redirect, url_for, session
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from datetime import datetime

app = Flask(__name__)

chatbot = ChatBot('TherapistBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('your_custom_mental_health_corpus.yml')

LOGS_DIRECTORY = 'logs'
if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY)

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    conversation_history = get_conversation_history(session['username'])
    return render_template("index_mental_health_extended.html", 
                           username=session['username'],
                           conversation_history=conversation_history)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/get")
def get_bot_response():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_message = request.args.get('msg')
    log_user_message(session['username'], user_message)
    response = str(chatbot.get_response(user_message))
    log_chatbot_response(session['username'], response)
    update_conversation_history(session['username'], user_message, response)
    return response

def log_user_message(username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {username}: {message}\n"
    with open(os.path.join(LOGS_DIRECTORY, f"{username}_user_logs.txt"), 'a') as log_file:
        log_file.write(log_entry)

def log_chatbot_response(username, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - TherapistBot: {response}\n"
    with open(os.path.join(LOGS_DIRECTORY, f"{username}_chatbot_logs.txt"), 'a') as log_file:
        log_file.write(log_entry)

def get_conversation_history(username):
    history_file_path = os.path.join(LOGS_DIRECTORY, f"{username}_conversation_history.txt")
    if os.path.exists(history_file_path):
        with open(history_file_path, 'r') as history_file:
            return history_file.read()
    return ''

def update_conversation_history(username, user_message, chatbot_response):
    history_file_path = os.path.join(LOGS_DIRECTORY, f"{username}_conversation_history.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {username}: {user_message}\nTherapistBot: {chatbot_response}\n\n"
    with open(history_file_path, 'a') as history_file:
        history_file.write(entry)

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
