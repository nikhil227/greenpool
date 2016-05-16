import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv('HOSTENV') or 'dev'
config_file = basedir+'/config/'+env+'.yml'
with open(config_file, 'r' ) as f:
    CONFIG = yaml.safe_load(f)

APP_NAME = 'pool'
DATABASE_URL = CONFIG['mysql']['connection']
SECRET = 'guty87g7gouigfW$ZE%YRYD'
