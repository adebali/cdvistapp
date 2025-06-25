#! /usr/bin/python
import os
import sys
import json
import utils

scriptDir = os.path.dirname(os.path.realpath(__file__))
dbDir = os.path.join(scriptDir, '..', '..', 'db')
fetchDB = os.path.join(scriptDir, 'fetchDB')

with open(os.path.join(scriptDir, '..', 'config.json'), 'r') as f:
    config = json.load(f)



# Databases

def cdd():
    version = config['databases']['versionToInstall']['rps-cdd']
    utils.runCode([
        'bash',
        os.path.join(fetchDB, 'download-cdd-pssm.sh'),
        version,
        os.path.join(dbDir, 'cdd'),
        '/usr/local/bin/'
        ])

def pfam():
    utils.runCode([
        'bash',
        os.path.join(fetchDB, 'download-pfam-hmm.sh'),
        config['databases']['versionToInstall']['hmmer-pfam'],
        os.path.join(dbDir, 'pfam')
        ])

def hhsuite_db(db_name):
    def hhsuite_db_file(dbtype, db_name):
        db_keyword = config['databases']['versionToInstall'][db_name]
        dbObject = config['databases']['hhsuite'][db_keyword]
        return dbObject['name'] + '.' + dbObject['extension']

    db_file = hhsuite_db_file('hhsearch', db_name)
    utils.runCode([
        'bash',
        os.path.join(fetchDB, 'download-hh-suite-hhm.sh'),
        db_file,
        os.path.join(dbDir, 'hh-suite')
        ])

def uniclust_db(db_name):
    def uniclust_db_file(dbtype, db_name):
        db_keyword = config['databases']['versionToInstall'][db_name]
        dbObject = config['databases']['uniclust'][db_keyword]
        return dbObject['name'] + '.' + dbObject['extension']

    db_file = uniclust_db_file('hhsearch', db_name)
    utils.runCode([
        'bash',
        os.path.join(fetchDB, 'download-uniclust-hhm.sh'),
        db_file,
        os.path.join(dbDir, 'uniclust'),
        '&&',
        'cp', 
        os.path.join(dbDir, 'uniclust', '*', '*', '*'), 
        os.path.join(dbDir, 'uniclust'), 
        ])

def all():
    pfam()
    hhsuite_db('hh-pfam')
    hhsuite_db('hh-pdb')
    hhsuite_db('hh-scop')
    uniclust_db('uniclust30')
    # uniclust_db('uniclust20')
    cdd()

if __name__=='__main__':
    print('installing tools and databases')
    all()
