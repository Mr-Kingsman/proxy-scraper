import urllib.request
import threading
import random
import sys
import os
import argparse

useragents=('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')


def checkproxy(txtfile):
	global out_file
	candidate_proxies = open(txtfile).readlines()
	filedl = open(txtfile, "w")
	filedl.close()
	out_file = open(txtfile, "a")
	threads = []
	for i in candidate_proxies:
		print(i)
		t = threading.Thread(target=checker, args=[i])
		t.start()
		threads.append(t)

	for t in threads:
		t.join()

	out_file.close()
	if args.verbose:
		print("\n\nCurrent IPs in proxylist: %s\n" % (len(open(txtfile).readlines())))

def checker(i):
	proxy = 'http://' + i
	proxy_support = urllib.request.ProxyHandler({'http' : proxy})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)
	req = urllib.request.Request(("http://www.google.com"))
	req.add_header("User-Agent", useragents)
	try:
		global chosenTimeout
		urllib.request.urlopen(req, timeout=chosenTimeout)
		out_file.write(i)
		if args.verbose:
			print ("%s works!\n" % proxy)
	except:
		if args.verbose:
			print ("%s does not respond.\n" % proxy)


if __name__ == "__main__":

	global chosenTimeout
	global txtfile

	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--timeout", type=int, help="-t 20")
	parser.add_argument("-l", "--list", help="-l output.txt")
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	chosenTimeout = args.timeout
	txtfile = args.list
	
	threading.Thread(target=checkproxy, args=(txtfile,)).start()
