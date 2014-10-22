import os,re,sys
import httplib

from threading import Thread


def main():
	hosts_in=open("hosts","r")
	hosts_out=open("hosts.new","w+")
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
		# print "try",ip,host
		conn = httplib.HTTPConnection(ip,timeout=1)
		try:
			conn.request('get', '/',headers={'host':host})
		except Exception, e:
			print "fail   ",ip,host
			hosts_out.write('#'+line)
		else:
			try:
				conn.getresponse().read()
			except Exception, e:
				print "aborted",ip,host
				hosts_out.write('#'+line)
			else:
				print "success",ip,host
				hosts_out.write(line)
		conn.close()

if __name__ == '__main__':
	main()
