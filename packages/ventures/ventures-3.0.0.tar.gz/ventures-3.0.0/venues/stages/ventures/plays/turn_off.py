

''''
	turn_off ({
		
	})
	
"'''


#/
#
from ventures.utilities.map.etch import etch_map
from ventures.utilities.map.scan import scan_map	
from ventures.utilities.ventures.find_venture import find_venture
from ventures.utilities.process.check_is_on import check_is_on
#
from ventures.plays_venture.turn_off import turn_off_venture
#
#
import rich
#
#
import json
import signal
import os
import time
import pprint
#
#\

''''
	turn off tasks everytime
	turn off processes if they are in the ventures_map_bracket
"'''

''''
	if task in ventures_map_bracket
		but not in ventures_map.py
			then: ?
"'''


def turn_off (packet):
	ventures_map_bracket = packet ["ventures_map_bracket"]
	ventures = packet ["ventures"]
	
	
	ventures_to_turn_off = []
	for venture in ventures:
		if (venture ["kind"] == "task"):
			ventures_to_turn_off.append (venture)

	venture_name = ""
	for venture_name in ventures_map_bracket:
		venture = ventures_map_bracket [ venture_name ]
		
		if (venture ["kind"] == "process_identity"):
			ventures_to_turn_off.append (find_venture (ventures, venture_name))
	
	#for venture in ventures_to_turn_off:
	#	print ("turn off:", venture)
	
	
	unfinished = []
	for name in ventures_map_bracket:
		try:
			turn_off_venture ({
				"venture": find_venture (ventures, name),
				"ventures_map_bracket": ventures_map_bracket
			})
		except Exception as E:
			unfinished.append ({
				"name": name
			})
			
	return {
		"unfinished": unfinished
	}
	
	
		
	
	