import os
import json
import datetime
import random

current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, '../', 'config.json'), 'r') as f:
    config = json.load(f)
    
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, str):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data

def jsonFile2dict(filePath):
    return json.loads(open(filePath).read())

def extension_fa(filename):
    return '.'.join(filename.split('.')[:-1]) + '.fa'

def makeId(prefix = ''):
    consonants = "qwrtypsdfghjklzxcvbnm"
    vowels = "aeiou"
    today = datetime.datetime.today()
    return prefix + str("{:02d}".format(today.year))[2:] + str("{:02d}".format(today.month)) + str("{:02d}".format(today.day)) + '_' + \
        random.choice(consonants) + random.choice(vowels) + random.choice(consonants) + random.choice(vowels) + \
        random.choice(consonants) + random.choice(vowels) + random.choice(consonants)

def writeTextToFile(text, filePath):
    out = open(filePath, 'w')
    out.write(text)
    out.close()

def jobId2filePath(jobId, fileName):
    return os.path.join(config['jobRoot'], jobId, fileName)

def createSubseqFasta(jobId, proteinIndex, interval, subSequence):
    description = str(proteinIndex) + '.' + interval
    fastaFile = os.path.join(config['jobRoot'], jobId, description + '.fa' )
    out = open(fastaFile, 'w')
    out.write('>' + description + '\n' + subSequence)
    out.close()
    return fastaFile

def jobId2fasta(jobId):
    return jobId2filePath(jobId, 'input.fa')

def jobId2request(jobId):
    return jobId2filePath(jobId, 'request.json')

def runCode(code):
    newCode = []
    for e in code:
        newCode.append(str(e))
    codeString = ' '.join(newCode)
    print(codeString)
    failureFlag = os.system(codeString)
    if failureFlag:
        raise ValueError(failureFlag)
    return True

def writeRequest(requestJson):
    with open(jobId2filePath(requestJson['id'], 'request.json'), 'w') as fp:
        json.dump(requestJson, fp, indent=1, sort_keys=True)
