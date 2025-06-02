import argparse
from cdvist_pipeline import runPipeline
import json

parser = argparse.ArgumentParser()
parser.add_argument('-i', required= False, help='input json file')
parser.add_argument('-id', required= False, help='job id')
args = parser.parse_args()

if args.i:
    fileInput = args.i
elif args.id:
    jobId = args.id
    fileInput = '/flask-app/static/job/fasta/' + jobId + '/request.json'
else:
    jobId = '000000_test'
    fileInput = '/flask-app/static/job/fasta/' + jobId + '/request_initial.json'    

with open(fileInput) as data_file:
    requestJson = json.load(data_file)
runPipeline(requestJson, False)