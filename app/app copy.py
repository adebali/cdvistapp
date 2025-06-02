#!/usr/bin/env python

import os
from flask import Flask, redirect, request, url_for, send_from_directory, flash, render_template, render_template_string, jsonify, send_file
from werkzeug.utils import secure_filename
from worker import celery
from celery.result import AsyncResult
import celery.states as states
from lib import utils
from lib import fasta
from lib import cdvist_pipeline
# from lib import install_tool
import prepareJob
import json
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib', 'config.json'), 'r') as f:
    config = json.load(f)

# install_tool.all()

env=os.environ
app = Flask(__name__, template_folder="static")
app.config['UPLOAD_FOLDER'] = '/flask-app/static/job/fasta'
app.config['ALLOWED_EXTENSIONS'] = set(['.fa', '.fasta', '.txt'])
app.secret_key = "super_secret_key"


@app.route('/add/<int:param1>/<int:param2>')
def add(param1,param2):
    task = celery.send_task('mytasks.add', args=[param1, param2], kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id,
                url=url_for('check_task',id=task.id,_external=True))

@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    print(res)
    return json.dumps({'state': res.state, 'info': str(res.result)})
    # return '{"state": "'+res.state+'"}'
    if res.state==states.PENDING:
        return res.state
    else:
        return str(res.result)

@app.route('/status/<string:id>')
def check_status(id):
    print(id)
    res = celery.AsyncResult(id)
    if res.state!=states.SUCCESS:
        print(res.info)
        if res.state == "PROGRESS" or res.state == "PENDING":
            print(res)
            return json.dumps({"job":res.info['job'], "state":res.state, "current":res.info['current'], "total": res.info["total"], "toolIndex": res.info["toolIndex"], "totalTool": res.info["totalTool"]})
        return json.dumps({"state": res.state})
    else:
        return json.dumps({"job":"", "state":res.state, "current":0, "total": 0, "toolIndex": 0, "totalTool": 0})     


@app.route('/out/<string:jobId>')
def out(jobId):
    task = celery.send_task('mytasks.out', args=[jobId], kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id,
                url=url_for('check_task',id=task.id,_external=True))


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
                'name': 'tmhmm',
                'checked': checkFormInput('tmhmm'),
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
            # getRpsblastField(1),
            # getRpsblastField(2),
            # getRpsblastField(3),
            # getRpsblastField(4),
            # getRpsblastField(5),
            # getHHsearchField(1),
            # getHHsearchField(2),
            # getHHsearchField(3),
            # getHHsearchField(4),
            # getHHsearchField(5)
        ]

        onlyCheckedTools = []
        for tool in tools:
            if tool['checked']:
                onlyCheckedTools.append(tool)
        


        requestJson = prepareJob.makeJson(jobName, inputFasta, onlyCheckedTools)
        task = celery.send_task('tasks.pipeline', task_id=jobName, args=[requestJson], kwargs={})
        # return str(json.dumps(request.form))
        # return str(json.dumps(requestJson))
        return redirect('static/arc.html?id=' + jobName, code=302)
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=env.get('DEBUG',True),
            port=int(env.get('PORT',80)),
            host=env.get('HOST','0.0.0.0')
    )
