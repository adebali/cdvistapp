#!/usr/bin/env python

import os
import sys
import json
with open(os.path.join('/cdvist', 'app', 'config.json'), 'r') as f:
    config = json.load(f)
import utils
import parsers
from celery import current_task
from time import sleep
# from unassigned import getUnassignedSegments, relativeTransform
from seq import seq
import copy
from iterativeSubSequenceSearch import runSingleProtein

cpu = config['parameters']['cpu']

# def runTmPrediction(filename, toolJob):
#     outFilename = filename + '.tm.txt'
#     code = config['tools'][toolJob['toolName']] + ' -short ' + filename + ' >' + outFilename 
#     os.system(code)
#     finishedToolJson = parsers.tmPrediction(outFilename, toolJob)
#     return finishedToolJson

# def runTmhmm(requestJson, toolIndex, CELERY_MODE=False):
#     totalToolNum = len(requestJson['tools'])
#     if CELERY_MODE:
#         current_task.update_state(state='PROGRESS', meta={'job': 'TMHMM', 'current': 0, 'total': 1, 'toolIndex': toolIndex, 'totalTool': totalToolNum})

#     tmhmmScript = config['tools']['tmhmm']
#     toolJob = requestJson['tools'][toolIndex]
#     jobId = requestJson['id']    
#     outputFile = utils.jobId2filePath(jobId, 'tmhmm.txt')
#     logFile = outputFile + '.log'
#     errorFile = outputFile + '.err'

#     codeList = [
#         tmhmmScript,
#         '-short -noplot',
#         utils.jobId2fasta(jobId),
#         '>',
#         outputFile,
#         '2>', errorFile
#     ]
#     utils.runCode(codeList)
#     requestJson['tools'][toolIndex]['status'] = 'completed'
#     updatedRequest = parsers.tmhmm(requestJson, outputFile, toolIndex)
#     return updatedRequest



def runDeepTMHMM(requestJson, toolIndex, CELERY_MODE=False):
    if CELERY_MODE:
        current_task.update_state(state='PROGRESS', meta={'job': 'TMHMM', 'current': 0, 'total': 1, 'toolIndex': toolIndex})

    import biolib
    application_name = 'DTU/DeepTMHMM:1.0.24'
    app = biolib.load(application_name)
    jobId = requestJson['id']    
    input_file = utils.jobId2fasta(jobId)
    print(f"Running DeepTMHMM on input file: {input_file}")
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file {input_file} does not exist.")
    # result = app.cli(args=f'--fasta {input_file}', machine='local')
    result = app.cli(args=f'--fasta {input_file}')
    output_dir = os.path.join(config['jobRoot'], jobId, 'deepTMHMM_results')
    result.save_files(output_dir)

    outputFile = os.path.join(output_dir, 'TMRs.gff3')
    requestJson['tools'][toolIndex]['status'] = 'completed'
    updatedRequest = parsers.deepTMHMM(requestJson, outputFile, toolIndex)
    return updatedRequest

def rpsblast_execute(inputFile, outputFile, toolJob, **kwargs):
    if kwargs.get('CELERY_MODE', False):
        current_task.update_state(state='PROGRESS', meta=kwargs.get('meta', {}))

    versionToUse = config['databases']['defaultVersion']['rps-cdd']
    dbObject = config['databases']['rps-cdd'][versionToUse]
    bitscoreFile = os.path.join(dbObject['location'], 'bitscore_specific_' + dbObject['name'] + '.txt')
    requestedDb = dbObject[toolJob['db']]
    logFile = outputFile + '.log'
    errorFile = outputFile + '.err'

    codeList = [
        'rpsblast',
        '-num_threads', cpu,
        '-db', requestedDb,
        '-query', inputFile,
        '-outfmt', 7,
        '-out', outputFile,
        '>', logFile,
        '2>', errorFile
    ]
    utils.runCode(codeList)
    return parsers.rpsblast(outputFile, toolJob, bitscoreFile)


def runRpsblast(requestJson, toolIndex, CELERY_MODE=False):
    totalToolNum = len(requestJson['tools'])
    toolJob = requestJson['tools'][toolIndex]
    jobId = requestJson['id']    
    versionToUse = config['databases']['defaultVersion']['rps-cdd']
    dbObject = config['databases']['rps-cdd'][versionToUse]
    bitscoreFile = os.path.join(dbObject['location'], 'bitscore_specific_' + dbObject['name'] + '.txt')
    totalEntryNum = len(requestJson['entries'])

    metaStatus = {}
    if CELERY_MODE:
        metaStatus = {'job': 'RPS-BLAST', 'current': 0, 'total': totalEntryNum, 'toolIndex': toolIndex, 'totalTool': totalToolNum}
        current_task.update_state(state='PROGRESS', meta=metaStatus)

    currentEntries = copy.deepcopy(requestJson['entries'])
    updatedEntries =[]
    i = 0
    for proteinObject in currentEntries:
        i += 1
        def rpsblast_segment(subSequence, segment, toolJob):
            interval = str(segment['start']) + '-' + str(segment['end'])
            rpsblastFileName = str(i) + '_' + interval + '_rpsblast.txt'
            rpsblast_out = utils.jobId2filePath(jobId, rpsblastFileName)
            fastaInput = utils.createSubseqFasta(jobId, i, interval, subSequence)
            metaStatus = {'job': 'RPS-BLAST', 'current': i, 'total': totalEntryNum, 'toolIndex': toolIndex, 'totalTool': totalToolNum}
            domains = rpsblast_execute(fastaInput, rpsblast_out, toolJob, CELERY_MODE=CELERY_MODE, meta=metaStatus)
            return domains

        protein = copy.deepcopy(proteinObject)
        newProtein = runSingleProtein(protein, toolJob, rpsblast_segment)
        updatedEntries.append(newProtein)

    requestJson['entries'] = updatedEntries
    requestJson['tools'][toolIndex]['status'] = 'completed'
    return requestJson



def moveInsignificantDomainsToUnassigned(protein):
    assignedList = []
    for domain in protein['segments']['assigned']:
        print(domain)
        if domain['assigned'] == False:
            protein['segments']['unassigned'].append(domain)
        else:
            assignedList.append(domain)
    protein['segments']['assigned'] = assignedList
    return protein

def runHmmer(requestJson, toolIndex, CELERY_MODE=False):
    totalToolNum = len(requestJson['tools'])
    if CELERY_MODE:
        current_task.update_state(state='PROGRESS', meta={'job': 'HMMER3', 'current': 0, 'total': 1, 'toolIndex': toolIndex, 'totalTool': totalToolNum})

    toolJob = requestJson['tools'][toolIndex]
    jobId = requestJson['id']    
    outputFile = utils.jobId2filePath(jobId, 'hmmer.txt')
    requestedDb = toolJob['db']
    logFile = outputFile + '.log'
    errorFile = outputFile + '.err'

    codeList = [
        'hmmscan',
        '-o', outputFile,
        '--cpu', cpu,
        config['databases']['hmmer-pfam'][requestedDb]['location'],
        utils.jobId2fasta(jobId),
        '>', logFile,
        '2>', errorFile
    ]
    utils.runCode(codeList)
    requestJson['tools'][toolIndex]['status'] = 'completed'
    updatedRequest = parsers.hmmer(requestJson, outputFile, toolIndex)
    return updatedRequest

def hhblits_execute(inputFile, outputFile, toolJob, **kwargs):
    if kwargs.get('CELERY_MODE', False):
        current_task.update_state(state='PROGRESS', meta=kwargs.get('meta', {}))
    if os.path.isfile(outputFile):
        return True
    hhblits_db_keyword = toolJob['hhblits_db']
    db_location = config['databases']['uniclust'][hhblits_db_keyword]['location']
    hhblits_code = 'hhblits'
    logFile = outputFile + '.log'
    errorFile = outputFile + '.err'
    codeList = [
        hhblits_code,
        '-i', inputFile,
        '-oa3m', outputFile,
        '-n', 1,
        '-cpu', cpu,
        '-d', db_location,
        '>', logFile,
        '2>', errorFile
    ] 
    return utils.runCode(codeList)

def hhsearch_execute(inputFile, outputFile, toolJob, **kwargs):
    if kwargs.get('CELERY_MODE', False):
        current_task.update_state(state='PROGRESS', meta=kwargs.get('meta', {}))
    hhsearch_db_keyword = toolJob['db']
    db_location = config['databases']['hhsuite'][hhsearch_db_keyword]['location']
    hhsearch_code = 'hhsearch'
    logFile = outputFile + '.log'
    errorFile = outputFile + '.err'
    codeList = [
        hhsearch_code,
        '-i', inputFile,
        '-o', outputFile,
        '-cpu', cpu,
        '-d', db_location,
        '>', logFile,
        '2>', errorFile
    ] 
    utils.runCode(codeList)
    return parsers.hhsearch(outputFile, toolJob)

def hhblits_hhsearch_iterate(requestJson, toolIndex, CELERY_MODE=False):

    totalToolNum = len(requestJson['tools'])
    totalEntryNum = len(requestJson['entries'])
    metaStatus = {}
    if CELERY_MODE:
        metaStatus = {'job': 'HHsearch', 'current': 0, 'total': totalEntryNum, 'toolIndex': toolIndex, 'totalTool': totalToolNum}
        current_task.update_state(state='PROGRESS', meta=metaStatus)

    toolJob = requestJson['tools'][toolIndex]
    jobId = requestJson['id']
    currentEntries = copy.deepcopy(requestJson['entries'])
    updatedEntries =[]
    i = 0
    for proteinObject in currentEntries:
        i += 1
        def hhblits_hhsearch(subSequence, segment, toolJob):
            interval = str(segment['start']) + '-' + str(segment['end'])
            hhblitsFileName = str(i) + '_' + interval + '_hhblits_' + toolJob['hhblits_db'] + '.a3m'
            hhsearchFileName = str(i) + '_' + interval + '_hhsearch_' + toolJob['db'] + '.hhr'
            hhblits_out = utils.jobId2filePath(jobId, hhblitsFileName)
            hhsearch_out = utils.jobId2filePath(jobId, hhsearchFileName)
            fastaInput = utils.createSubseqFasta(jobId, i, interval, subSequence)
            metaStatus = {'job': 'HHblits', 'current': i, 'total': totalEntryNum, 'toolIndex': toolIndex, 'totalTool': totalToolNum}
            if hhblits_execute(fastaInput, hhblits_out, toolJob, CELERY_MODE=CELERY_MODE, meta=metaStatus):
                metaStatus = {'job': 'HHsearch', 'current': i, 'total': totalEntryNum, 'toolIndex': toolIndex, 'totalTool': totalToolNum}                
                domains = hhsearch_execute(hhblits_out, hhsearch_out, toolJob, CELERY_MODE=CELERY_MODE, meta=metaStatus)
                if len(domains) > 0:
                    if domains[0]['prob'] > float(toolJob['probability']):
                        domains[0]['assigned'] = True
                    else:
                        domains[0]['assigned'] = False
                if len(domains) > 1:
                    for j in range(1, len(domains)):
                        domains[j]['assigned'] = False
                return domains
            return []

        # if CELERY_MODE:
        #     current_task.update_state(state='PROGRESS', meta={'job': 'HHsearch', 'current': i, 'total': totalEntryNum})
        protein = copy.deepcopy(proteinObject)
        newProtein = moveInsignificantDomainsToUnassigned(runSingleProtein(protein, toolJob, hhblits_hhsearch))
        updatedEntries.append(newProtein)
    
    requestJson['entries'] = updatedEntries
    return requestJson


def zipAccessories(jobId, extensions = []):
    '''compresses the accessory files and leaves the request.json'''
    wildcard_string = ''
    jobDir = os.path.join(config['jobRoot'], jobId)
    if extensions != []:
        for extension in extensions:
            wildcard_string += ' ' + os.path.join(jobDir, '*.' + extension)
        codeList = [
            'tar czvf',
            os.path.join(jobDir, 'acc.tgz'),
            '$(ls ' + wildcard_string + ' )'
        ]
        utils.runCode(codeList)
        rmCode = [
            'rm -f ',
            wildcard_string
        ]
        utils.runCode(rmCode)


def runTool(requestJson, toolIndex, CELERY_MODE=False):
    toolJob = requestJson['tools'][toolIndex]
    totalToolNum = len(requestJson['tools'])
    if CELERY_MODE:
        current_task.update_state(state='PROGRESS', meta={'job': 'counting', 'current': 0, 'total': totalToolNum, 'toolIndex': 0, 'totalTool': totalToolNum})

    # if toolJob['name'] == 'tmPrediction':
    #     toolJob = runTmPrediction(filename, toolJob)
    if toolJob['name'] == 'DeepTMHMM':
        if toolJob['checked']:
            return runDeepTMHMM(requestJson, toolIndex, CELERY_MODE)
        return requestJson
    
    if toolJob['name'] == 'hmmer3':
        if toolJob['checked']:
            return runHmmer(requestJson, toolIndex, CELERY_MODE)
        return requestJson

    if toolJob['name'] == 'rpsblast':
        if toolJob['checked']:        
            return runRpsblast(requestJson, toolIndex, CELERY_MODE)
        return requestJson

    if toolJob['name'] == 'hhsearch':
        if toolJob['checked']:        
            return hhblits_hhsearch_iterate(requestJson, toolIndex, CELERY_MODE)
        return requestJson
    
    return requestJson



def runPipeline(requestJson, CELERY_MODE=False):
    toolIndex = 0
    tools = requestJson['tools']
    print(tools)
    for tool in tools:
        if tool['status'] == 'not processed':
            requestJson = runTool(requestJson, toolIndex, CELERY_MODE)
            utils.writeRequest(requestJson)
        toolIndex += 1
    if CELERY_MODE:
        zipAccessories(requestJson['id'], ['txt', 'a3m', 'hhr', 'log', 'err', 'fa'])
        current_task.update_state(state='SUCCESS')
    return requestJson

# with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'static', 'job', 'fasta', '171005_magodam', 'request.json'), 'r') as f:
#     requestJson = json.load(f)
#     runPipeline(requestJson)

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        requestJson = json.load(f)
        runPipeline(requestJson)