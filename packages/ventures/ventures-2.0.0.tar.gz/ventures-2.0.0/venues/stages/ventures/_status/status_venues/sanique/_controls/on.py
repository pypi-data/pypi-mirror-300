

'''
	from vaccines.adventures.sanique._controls.on as turn_on_sanique
	turn_on_sanique ()
'''


'''
	sanic /vaccines/venues/stages/vaccines/adventures/sanique/harbor/on.proc.py
'''

#----
#
#
from biotech.topics.show.variable import show_variable
#
#
import atexit
import json
import multiprocessing
import subprocess
import time
import os
import shutil
import sys
import time
import pathlib
from os.path import dirname, join, normpath
import sys
#
#----

	

def floating_process (procedure, CWD, env):
	show_variable ({
		"procedure": procedure
	})
	
	process = subprocess.Popen (
		procedure, 
		
		cwd = CWD,
		env = env,
		shell = True,
		
		close_fds = True
	)
	
	pid = process.pid
	
	show_variable ("sanic pid:", pid)

def turn_on_sanique (packet = {}):
	harbor_port = 10000
	harbor_path = str (normpath (join (
		pathlib.Path (__file__).parent.resolve (), 
		".."
	))) 


	env_vars = os.environ.copy ()
	env_vars ['PYTHONPATH'] = ":".join (sys.path)
	env_vars ['INSPECTOR_PORT'] = "10001"

	'''
		cd /habitat_physical/.venv/lib/python3.12/site-packages/vaccines/adventures/sanique
inspector_port=7457 /habitat_physical/.venv/bin/python /habitat_physical/.venv/bin/sanic harbor:create --port=8000 --host=0.0.0.0 --factory --fast --no-access-logs > /dev/null &
	'''
	'''
		> /dev/null 2>&1 &"
	'''
	the_procedure = " ".join ([
		"sanic",
		f'harbor:create',
		f'--port={ harbor_port }',
		f'--host=0.0.0.0',
		'--factory',
		'--fast',
		"--no-access-logs",
		'>',
		'/dev/null',
		'&'
	])

	process = floating_process (
		procedure = the_procedure,
		CWD = harbor_path,
		env = env_vars
	)
	
