from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

env.pelicanconf = 'pelicanconf.py' 

env.github_pages_branch = 'gh-pages'

def clean():
    "Remove rendered site" 
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    "Render site"
    local('pelican -s {pelicanconf}'.format(**env))

def rebuild():
    "Remove site, render it again"
    clean()
    build()

def regenerate():
    "Regenerate site, monitor for changes"
    local('pelican -r -s {pelicanconf}'.format(**env))

def serve():
    "Serve site from localhost"
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    "Serve site from localhost, monitor for changes"
    build()
    serve()

def upload_ghp():
    "Render site and upload to GitHub Pages"
    rebuild()
    local('ghp-import -n -b {github_pages_branch} -p {deploy_path}'.format(**env))
