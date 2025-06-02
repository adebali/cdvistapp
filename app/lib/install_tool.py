#! /usr/bin/python
import os
import sys
import json
import utils

scriptDir = os.path.dirname(os.path.realpath(__file__))
# vendorDir = os.path.join(scriptDir, '..', 'vendor')
vendorDir = os.path.join('/vendor')
toolDir = os.path.join(vendorDir, 'tools')
dbDir = os.path.join(vendorDir, 'db')

with open(os.path.join(scriptDir, 'config.json'), 'r') as f:
    config = json.load(f)



# The tools

def hmmer3():
    utils.runCode([
        'bash',
        os.path.join(vendorDir, 'install-hmmer3.sh'),
        config['tools']['versionToInstall']['hmmer3'],
        os.path.join(toolDir, 'hmmer3')
        ])

def hhsuite():
    utils.runCode([
        'bash',
        os.path.join(vendorDir, 'install-hh-suite.sh'),
        config['tools']['versionToInstall']['hhsuite'],
        os.path.join(toolDir, 'hhsuite')
        ])

def blast():
    utils.runCode([
        'bash',
        os.path.join(vendorDir, 'download-blast-tarball.sh'),
        config['tools']['versionToInstall']['blast'],
        os.path.join(toolDir, 'blast')
        ])

# Databases

def cdd():
    version = config['databases']['versionToInstall']['rps-cdd']
    utils.runCode([
        'bash',
        os.path.join(vendorDir, 'download-cdd-pssm.sh'),
        version,
        os.path.join(dbDir, 'cdd')
        ])

def pfam():
    utils.runCode([
        'bash',
        os.path.join(vendorDir, 'download-pfam-hmm.sh'),
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
        os.path.join(vendorDir, 'download-hh-suite-hhm.sh'),
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
        os.path.join(vendorDir, 'download-uniclust-hhm.sh'),
        db_file,
        os.path.join(dbDir, 'uniclust'),
        '&&',
        'cp', 
        os.path.join(dbDir, 'uniclust', '*', '*', '*'), 
        os.path.join(dbDir, 'uniclust'), 
        ])

def all():
    hmmer3()
    hhsuite()
    blast()
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
