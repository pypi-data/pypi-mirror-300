

#----
#
from vaccines._physics import retrieve_physics
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#from sanic.response import html
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
#
#----

def sockets_guest (packet):
	physics = retrieve_physics ()

	