

from .utilities.hike_passive import hike_passive


'''
	ventures_map.JSON {
		"adventure_1": {
			"process_identity": ""
		},
		"adventure_2": {
			"process_identity": ""
		}				
	}
'''

'''
	check_is_on ({
		"name": "",
		
		"is_on": 
		"wait_for": 
	})
'''




#/
#
#
#	every venture
#
from .plays.turn_on import turn_on
from .plays.turn_off import turn_off
from .plays.is_on import is_on
#
#
#	1 venture
#
from ventures.plays_venture.turn_on import turn_on_venture
from ventures.plays_venture.turn_off import turn_off_venture
#
from ventures.utilities.map.etch import etch_map
from ventures.utilities.map.scan import scan_map
#
#
#	utilities
#
from ventures.utilities.ventures.find_venture import find_venture
#
#
import os
#
#
import rich
#
#\

def ventures_map (packet):
	ventures = packet ["ventures"]
	the_map_path = packet ["map"]

	ventures_map_bracket = {}
	if os.path.exists (the_map_path):
		ventures_map_bracket = scan_map ({
			"path": the_map_path
		})

	def turn_on_move (packet = {}):
		print ('turn on move', packet)
	
		rich.print_json (data = {
			'turn on move': packet
		})
	
		''''
			This is for turning on one at a time.
		"'''
		if (type (packet) == dict and "name" in packet):
			name = packet ["name"]
		
			venture = find_venture (ventures, name)
		
			the_venture_packet = turn_on_venture ({
				"venture": venture,
				"ventures_map_bracket": ventures_map_bracket
			})
			
			etch_map ({
				"path": the_map_path,
				"bracket": ventures_map_bracket
			})
			status = is_on ({
				"ventures": ventures,
				"ventures_map_bracket": ventures_map_bracket
			});
			
			return;
	
		ventures_packet = turn_on ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		})
		etch_map ({
			"path": the_map_path,
			"bracket": ventures_map_bracket
		})
		status = is_on ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		});

	def is_on_move (packet = {}):	
		status = is_on ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		});
	
		return;
		
	def turn_off_move (packet = {}):
		rich.print_json (data = {
			'turn off move': packet
		})
	
		''''
			This is for turning off one at a time.
		"'''
		if (type (packet) == dict and "name" in packet):
			name = packet ["name"]
			turn_off_venture ({
				"venture": find_venture (ventures, name),
				"ventures_map_bracket": ventures_map_bracket
			})
			etch_map ({
				"path": the_map_path,
				"bracket": ventures_map_bracket
			})
			status = is_on ({
				"ventures": ventures,
				"ventures_map_bracket": ventures_map_bracket
			});
			return;
	
		turn_off ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		});
		etch_map ({
			"path": the_map_path,
			"bracket": ventures_map_bracket
		});
		status = is_on ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		});
	
		return;
		
	def refresh ():
		turn_off ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		});
		ventures_packet = turn_on ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		})
		etch_map ({
			"path": the_map_path,
			"bracket": ventures_map_bracket
		})
		status = is_on ({
			"ventures": ventures,
			"ventures_map_bracket": ventures_map_bracket
		});

	return {
		"turn on": turn_on_move,
		"turn off": turn_off_move,
		"is on": is_on_move,
		"refresh": refresh
	}