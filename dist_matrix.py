# install pip if you dont have it: https://pypi.python.org/pypi/pip
# intall simplejson: pip install simplejson
## excelent guide here: http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import sys, getopt
import simplejson, urllib
from read_csv_to_dict import read_csv, write_csv

def main(argv):	
	inputfile = ''
	outputfile = ''
	muni = ''
	qrtr = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:m:",["ifile=","ofile=", "mode="])
	except getopt.GetoptError:
		print 'dist_matrix.py -i <inputfile> -o <outputfile> -m <mode>'
		sys.exit(2)
	def distance(origins, destinations, mode, key, **geo_args):
	    geo_args.update({
	        'origins': origins,
	        'destinations': destinations,
	        'mode': mode,
	        'key' : key
	    })
	    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
	    print url
	    result = simplejson.load(urllib.urlopen(url))
	    print result
	    return result['rows'][0]['elements'][0]['distance']['value']
	for opt, arg in opts:
		if opt == '-h':
			print 'dist_matrix.py -i <inputfile> -o <outputfile> -m <mode>' 
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-m", "--mode"):
			mode = arg
		elif opt in ("-k", "--key"):
			key = arg
		# elif opt in ("-u", "--unit"):
		# 	unit = arg
	print 'Input file is ', inputfile
	print 'Output file is ', outputfile
	print 'Mode is ', mode
	GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
	raw_matrix = read_csv(inputfile)
	org_dist = ""
	for each_line in raw_matrix:
		origins = each_line['origin']
		destinations = each_line['destination']
		try:
			distance_m = distance(origins, destinations, mode=mode, key='')
			each_line['distance'] = distance_m
		except:
			each_line['distance'] = 'err_resp'
			pass
		
	
	write_csv(raw_matrix, outputfile)

if __name__ == '__main__':
		main(sys.argv[1:])


