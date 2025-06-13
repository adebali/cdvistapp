import os
import sys
sys.path.append(os.path.dirname(__file__))
import json
from flask import Flask, jsonify, request, render_template, redirect
from werkzeug.utils import secure_filename
from lib import utils, fasta
import prepareJob
from celery import Celery
from celery.result import AsyncResult
import celery.states as states
from .tasks import add_together  # import tasks here
from .tasks import long_task  # import tasks here



def make_celery(app):
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_url = f'redis://{redis_host}:6379/0'
    celery = Celery(
        app.import_name,
        backend=redis_url,
        broker=redis_url
    )
    celery.conf.update(app.config)
    celery.conf.update({
        'broker_connection_retry_on_startup': True  # Retain retry behavior during startup
    })
    celery.autodiscover_tasks(['app'])
    return celery

app = Flask(__name__, template_folder="static")
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'job', 'fasta')
app.secret_key = "super_secret_key"

celery = make_celery(app)

# @app.route('/')
# def index():
#     return '<a href="/start-task">Start Task</a>'

@app.route('/start-task')
def start_task():
    task = long_task.apply_async(args=[10])
    status_url = f'/task-status/{task.id}'
    return f'Task started! <a href="{status_url}">Check status here</a>', 202

@app.route('/task-status/<task_id>')
def task_status(task_id):
    task = celery.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Waiting in queue...'}
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'percent': int((task.info.get('current', 0) / task.info.get('total', 1)) * 100)
        }
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}

    return jsonify(response)

@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    return json.dumps({'state': res.state, 'info': str(res.result)})

@app.route('/status/<string:id>')
def check_status(id):
    res = celery.AsyncResult(id)
    if res.state!=states.SUCCESS:
        if res.state == "PROGRESS" or res.state == "PENDING":
            print(res)
            # return json.dumps({"job":res.info['job'], "state":res.state, "current":res.info['current'], "total": res.info["total"], "toolIndex": res.info["toolIndex"], "totalTool": res.info["totalTool"]})
            return json.dumps({"job":res.info['job'], "state":res.state, "current":res.info['current'], "total": res.info["total"], "toolIndex": res.info["toolIndex"]})
        return json.dumps({"state": res.state})
    else:
        return json.dumps({"job":"", "state":res.state, "current":0, "total": 0, "toolIndex": 0, "totalTool": 0})     



@app.route('/', methods=['GET', 'POST'])
def root():
    
    def checkFormInput(key):
        if key in request.form.keys():
            return request.form[key]
        else:
            print(key + 'is not in the form')
            return False

    def mainPageError(message):
        return redirect('/?msg=' + message)

    def getHHsearchField(num):
        num = str(num)
        return {
            'name': 'hhsearch',
            'checked': checkFormInput('hhsearch' + num),
            'db': checkFormInput('hhsearch_db' + num),
            'gap_length': int(checkFormInput('hhsearch_gap' + num)),
            'status': 'not processed',
            'probability': float(checkFormInput('hhsearch_prob' + num)),
            'hhblits_db': checkFormInput('hhblits_db' + num)
        }

    
    def getRpsblastField(num):
        num = str(num)
        return {
            'name': 'rpsblast',
            'checked': checkFormInput('rpsblast' + num),
            'db': checkFormInput('rps_db' + num),
            'gap_length': int(checkFormInput('rps_gap' + num)),
            'status': 'not processed',
        }

    error = None

    if request.method == 'POST':
        jobName= utils.makeId('')
        inputFasta = os.path.join(app.config['UPLOAD_FOLDER'], jobName, 'input.fa')
        file = request.files.get('file', '')
        text = checkFormInput('text')
        if not file or file.filename == '':
            error = 'No selected file'

        if file:
            filename = secure_filename(file.filename)
            error = filename
            os.system('mkdir ' + os.path.join(app.config['UPLOAD_FOLDER'], jobName))
            file.save(inputFasta)
            fastaObject = fasta.fasta(inputFasta)
            sequenceCount = fastaObject.getSequenceCount()
            if sequenceCount == 0:
                return mainPageError('Not a valid fasta formatted input is provided')                
            if sequenceCount > 500:
                return mainPageError('Maximum allowed sequence number, 500 is exceeded: ' + str(sequenceCount))
            maxLength = fastaObject.getMaxSeqLength()
            if maxLength > 3000:
                return mainPageError('Allowed maximum length of a protein is exceeded: ' + str(maxLength))

 
            # currentJson = compileJson()
            # currentJson['jobName'] = jobName
            # jsonString = json.dumps(currentJson)
            # return redirect('/customInput/' + jsonString)
            # return redirect('static/job/fasta/' + jobName + '/' + 'input.fa')
        elif text:
            os.system('mkdir ' + os.path.join(app.config['UPLOAD_FOLDER'], jobName))        
            utils.writeTextToFile(text, inputFasta)
        else:
            return "No input specified."
        tools = [
            {
                'name': 'DeepTMHMM',
                'checked': checkFormInput('deeptmhmm'),
                'status': 'not processed'
            },
            {
                'name': 'hmmer3',
                'checked': checkFormInput('hmmer3'),
                # 'db': 'pfam31.0',
                'db': checkFormInput('hmmer3_db'),
                'status': 'not processed'
            },
            # {
            #     'name': 'rpsblast',
            #     'checked': checkFormInput('rpsblast1'),
            #     'db': checkFormInput('rps_db1'),
            #     'gap_length': int(checkFormInput('rps_gap1')),
            #     'status': 'not processed'
            # },
            getRpsblastField(1),
            getRpsblastField(2),
            getRpsblastField(3),
            getRpsblastField(4),
            getRpsblastField(5),
            getHHsearchField(1),
            getHHsearchField(2),
            getHHsearchField(3),
            getHHsearchField(4),
            getHHsearchField(5)
        ]

        onlyCheckedTools = []
        for tool in tools:
            if tool['checked']:
                onlyCheckedTools.append(tool)
        
        requestJson = prepareJob.makeJson(jobName, inputFasta, onlyCheckedTools)
        task = celery.send_task('tasks.pipeline', task_id=jobName, args=[requestJson], kwargs={})
        return redirect('static/arc.html?id=' + jobName, code=302)
    return render_template('index.html', error=error)


@app.route('/run-task')
def run_task():
    result = add_together.delay(10, 20)
    return f'Task launched! Task ID: {result.id}'

@app.route('/task-result/<task_id>')
def task_result(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        return f"Result: {result.result}"
    else:
        return "Task is still running. Please check back later."
    
if __name__ == '__main__':
    env=os.environ
    app.run(debug=env.get('DEBUG',True),
            port=int(env.get('PORT',80)),
            host=env.get('HOST','0.0.0.0')
    )