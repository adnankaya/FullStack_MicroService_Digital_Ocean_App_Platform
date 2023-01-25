from flask import Flask, jsonify
from celery import Celery
# internals
import settings

app = Flask(__name__)
celery = Celery(__name__, **settings.PARAMS_CELERY)



@app.route("/")
def index():
    return jsonify(message="App1 works!")

# define celery task
@celery.task
def check_celery_task():
    return "celery works!"

@app.route('/celery-check/', methods=['GET'])
def celery_check():
    task = check_celery_task.delay()
    response = {
        'celery-check': task.id,
        'celery-state': task.state
    }
    return jsonify(response)