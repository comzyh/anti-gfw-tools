import os,re,sys
import httplib
import getopt
import datetime
from threading import Thread


def test_host(ip, host):
	conn = httplib.HTTPConnection(ip,timeout=1)
	try:
		conn.request('GET', '/',headers={'host':host})
	except Exception, e:
		return "fail"

	try:
		conn.getresponse().read()
	except Exception, e:
		pass
	else:
		return "success"

	conn = httplib.HTTPSConnection(ip,timeout=3)

	try:
		conn.request('GET', '/')
		conn.getresponse().read()
	except Exception, e:
		return "aborted"
	else:
		return "https"
	conn.close()

def main():
	hosts_in_filename = 'hosts'
	hosts_out_filename = 'hosts.new'
	log_filename = 'host_tester.log'
	attempt_times = 2
	try:
		opts, args = getopt.getopt(sys.argv[1:],'f:o:h:l:t:')
		for opt, val in opts:
			if opt == '-f':
				hosts_in_filename = val
			elif opt == '-o':
				hosts_out_filename = val
			elif opt == '-l':
				log_filename = val
			elif opt == '-t':
				attempt_times = int(val)
			elif opt == '-h':
				print "Usage:[-f filename],[-o output_filename]"
				sys.exit()
	except getopt.GetoptError:
		print "Usage:[-f filename],[-o output_filename]"
	print "Logfile: %s" % log_filename
	hosts_in=open(hosts_in_filename,'r')
	hosts_out=open(hosts_out_filename,'w+')
	log_out = open(log_filename,'a')
	log_out.write("Testing hosts file '%s' at %s" % (hosts_in_filename,datetime.datetime.now()))

	def log_write(msg):
		print msg
		log_out.write(msg + '\n')

	available_hosts = []
	for line in hosts_in.readlines():
		if line.strip() == '':
			hosts_out.write(line)
			continue
		arr = line.split()
		if  len(arr) < 2 or arr[0].startswith('#'):
			hosts_out.write(line)
			continue
		ip = arr[0]
		host = arr[1]
		if ip in available_hosts:
			log_write("%s\t%s\t%s" % ('tested',ip,host))
			hosts_out.write(line)
			continue
		for time in range(attempt_times):
			result = test_host(ip,host)
			log_write("%s\t%s\t%s" % (result,ip,host))
			if result == 'success' or result == 'https':
				hosts_out.write(line)
				available_hosts.append(ip)
				break
			else:
				if time + 1 == attempt_times:
					hosts_out.write('#'+line)

if __name__ == '__main__':
	main()
