#!/usr/bin/env python
#-*- coding:utf-8 -*-
#*******************************************
#APP: EO-RIPPER.py                       ***
#AUTHOR: Jorge Websec                    ***
#TWITTER: @JorgeWebsec                   ***
#Email: jorge@quantika14.com             ***
#License: GNU v3                         ***
#*******************************************

import re, mechanize, json, duckduckgo, urllib2, requests
import requests
from bs4 import BeautifulSoup
from validate_email import validate_email

emails_list = "emails.txt"

class colores:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    alert = '\033[93m'
    fail = '\033[91m'
    normal = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

br = mechanize.Browser()
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

def get_usernameEmail(email):
	email = email.split("@")
	username = email[0]
	return username.replace(".","")

def check_wordpress(email):
	try:
		r = br.open('http://wordpress.com/wp-login.php')
		br.select_form("loginform")
		br.form["log"] = email
		br.form["pwd"] = "123456"
		br.submit()
		respuestaWP = br.response().geturl()
		html =  br.response().read()
		soup = BeautifulSoup(html, "html.parser")
		divError = soup.findAll("div", {"id": "login_error"})
		div = remove_tags(str(divError))
		if "incorrect" in div:
			print "|--[INFO][WordPress][CHECK][>] The account exist..."

		if "Invalid" in div:
			print "|--[INFO][WordPress][CHECK][>] Account doesn't exist..."
	except:
		print colores.alert + "|--[WARNING][LinkedIn][>] Error..." + colores.normal

def check_pastebin(email):
	url = "http://pastebin.com/search?q=" + email.replace(" ", "+")
	print "|--[INFO][PASTEBIN][SEARCH][>] " + url + "..."
	html = br.open(url).read()
	soup = BeautifulSoup(html, "html.parser")
	for div in soup.findAll("div", {"class", "gsc-thumbnail-inside"}):
		print "|--[INFO][PASTEBIN][URL][>]" + str(div)

def check_duckduckgoInfo(email):
	try:
		links = duckduckgo.search(email, max_results=10)
		for link in links:
			if "delsexo.com" in str(link):
				pass
			else:
				print "|--[INFO][DuckDuckGO][SEARCH][>] " + str(link)
	except:
		print colores.alert + "|--[WARNING][DUCKDUCKGO][>] Error..." + colores.normal

def check_duckduckgoSmartInfo(email):
	no_company = ("gmail"," hotmail"," yahoo"," protonmail"," mail")
	split1 = email.split("@")
	name = split1[0].replace("."," ")
	split2 = split1[1].split(".")
	company = split2[0].replace(".", "")
	if company in no_company:
		data = name
	else:
		data = name + " " + company
	links = duckduckgo.search(data, max_results=10)
	for link in links:
		print "|--[INFO][DuckDuckGO][SMART SEARCH][>] " + str(link)
		if "linkedin.com/in/" in str(link):
			print colores.green + "|----[>][POSSIBLE LINKEDIN DETECT] ----" + colores.normal
		if "twitter.com" in str(link):
			print colores.green + "|----[>][POSSIBLE TWITTER DETECT] ----" + colores.normal
		if "facebook.com" in str(link):
			print colores.green + "|----[>][POSSIBLE FACEBOOK DETECT] ----" + colores.normal
		if "soundcloud.com/" in str(link):
			print colores.green + "|----[>][POSSIBLE SOUNDCLOUD DETECT] ----" + colores.normal

def check_AccountTwitter(email):
	username = get_usernameEmail(email)
	url = "https://twitter.com/" + username
	try:
		html = requests.get(url).text
		soup = BeautifulSoup(html, "html.parser")
		for text in soup.findAll("h1"):
			text = remove_tags(str(text))
			if "Sorry" in text or "Lo sentimos," in text:
				print "|--[INFO][Twitter][" + colores.blue+ username + colores.normal + "][>] Account doesn't exist..."
			else:
				print colores.green + "|--[INFO][Twitter][" + colores.blue+ username + colores.green + "][>] The account exist." + colores.normal
	except urllib2.HTTPError:
		print colores.alert + "|--[404 HTTP RESPONSE][Check_AccountTwitter][>] 404 HTTP Twitter error..." + colores.normal

def check_netflix(email):
	try:
		r = br.open('https://www.netflix.com/es/login')
		br.select_form(nr=0)
		br.form["userLoginId"] = email
		br.form["password"] = "123456"
		br.submit()
		respuestaURL = br.response().geturl()
		html =  br.response().read()
		soup = BeautifulSoup(html, "html.parser")
		div = soup.find("div",{"class":"ui-message-contents"})
		if "ninguna" in remove_tags(str(div)):
			print "|--[INFO][NETFLIX][ES][CHECK][>] Account doesn't exist..."
		else:
			print "|--[INFO][NETFLIX][ES][CHECK][>] The account exist..."
	except:
		print colores.alert + "|--[ERROR][Check_Netflix][>] Netflix error..." + colores.normal

def check_amazon(email):
	r = br.open('https://www.amazon.es/ap/register?showRememberMe=true&openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=esflex&openid.return_to=https%3A%2F%2Fwww.amazon.es%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_youraccount_signout%26signIn%3D1%26useRedirectOnSuccess%3D1&prevRID=8JDMFMXKWNZQKE8EYVTH&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ubid=259-8895990-3455759')
	br.select_form(nr=0)
	br.form["customerName"] = "Gustavo Becquer"
	br.form["email"] = email
	br.form["password"] = "123456//eoripper"
	br.form["passwordCheck"] = "123456//eoripper"
	br.submit()

	html = br.response().read()

	soup = BeautifulSoup(html, "html.parser")
	div = soup.find("div", {"class":"a-alert-content"})

	if "ya existe una cuenta" in remove_tags(str(div)):
		print "|--[INFO][AMAZON][ES][CHECK][>] Account doesn't exist..."
	else:
		print "|--[INFO][AMAZON][ES][CHECK][>] The account exist..."

def check_haveibeenpwned(email):
	url = "https://haveibeenpwned.com/account/" + email
	html = br.open(url)
	soup = BeautifulSoup(html, "html.parser")
	if soup.find("div", {"class": "pwnedSearchResult pwnTypeDefinition pwnedWebsite panel-collapse in"}):
		print "|--[INFO][HAVEIBEENPWNED][>] Your email appear in leaks..."
	else:
		print "|--[INFO][HAVEIBEENPWNED][>] Your email doesn't appear in leaks..."

def check_emailrep(email):
	url = "https://emailrep.io/" + email
	JSON = json.loads(requests.get(url).text)
	
	print "|--[INFO][REPUTATION][>] " + JSON["reputation"]
	print "|--[INFO][SUSPICIUS][>] " + str(JSON["suspicious"])
	print "|--[INFO][BLACK LIST][>] " + str(JSON["details"]["blacklisted"])
	print "|--[INFO][MALICIUS ACTIVITY][>] " + str(JSON["details"]["malicious_activity"])
	print "|--[INFO][SPAM][>] " + str(JSON["details"]["spam"])
	print "|--[INFO][MALICIUS ACTIVITY][>] " + str(JSON["details"]["malicious_activity"])
	print "|--[INFO][SPOOFABLE][>] " + str(JSON["details"]["spoofable"])
	print "|--[INFO][SPF STRICT][>] " + str(JSON["details"]["spf_strict"])
	print "|--[INFO][DMARC ENFORCED][>] " + str(JSON["details"]["dmarc_enforced"])

	DOMAIN = email.split("@")
	print "|--[INFO][DOMAIN][>] Analyzing the domain " + DOMAIN[1]
	print "|----[INFO][CHECK DOMAIN][>] " + str(JSON["details"]["domain_exists"])
	print "|----[INFO][DOMAIN REPUTATION][>] " + str(JSON["details"]["domain_reputation"])
	print "|----[INFO][NEW DOMAIN][>] " + str(JSON["details"]["new_domain"])
	print "|------[INFO][DAYS SINCE DOMAIN CREATION][>] " + str(JSON["details"]["days_since_domain_creation"])
	print "|------[INFO][FREE PROVIDER][>] " + str(JSON["details"]["free_provider"])

	#RRSS Analyzer
	print "|--[INFO][PROFILES IN SOCIAL NETWORKS][>] Analyzing..."
	for profile in JSON["details"]["profiles"]:

		print "|------[INFO][SOCIAL NETWORK][>] " + profile



# Email spoofing generator php
def generate_php(fromm, to, title, messaje):
	php = """<?php
$from      = '""" + fromm + """';
$titulo    = '""" + title + """';
$mensaje   = '""" + messaje + """';
$cabeceras = 'From: """ + to + """' . "\r\n" .
    'Reply-To: nice@eo-ripper.py' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();

mail($from, $titulo, $mensaje, $cabeceras);
echo "Todo OK!";
?>"""
	f = open("evilmail.php", "a");
	f.write(php)
	f.close()
	print "[|--[EO-RIPPER][SAY][>] the evilmail.php has been created!"

def banner():
	print """
███████╗ ██████╗       ██████╗ ██╗██████╗ ██████╗ ███████╗██████╗    ██████╗ ██╗   ██╗
██╔════╝██╔═══██╗      ██╔══██╗██║██╔══██╗██╔══██╗██╔════╝██╔══██╗   ██╔══██╗╚██╗ ██╔╝
█████╗  ██║   ██║█████╗██████╔╝██║██████╔╝██████╔╝█████╗  ██████╔╝   ██████╔╝ ╚████╔╝ 
██╔══╝  ██║   ██║╚════╝██╔══██╗██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗   ██╔═══╝   ╚██╔╝  
███████╗╚██████╔╝      ██║  ██║██║██║     ██║     ███████╗██║  ██║██╗██║        ██║   
╚══════╝ ╚═════╝       ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
      Author: Jorge Websec | Twitter: @JorgeWebsec | jorge.coronado@quantika14.com
-------------------------------------------------------------------------------------
[!]What can I know with your email?
    - Only 1 email or emails list
    - Verify emails
    - Verify LinkedIn, WordPress, Amazon[ES], Tumblr, Netflix and DDG Hacking
    - Pastebin
-------------------------------------------------------------------------------------
Date version: 09/01/2017 | Version: 1.0
Date latest version: 21/01/2017 | Version: 1.0.1
Date latest version: 27/07/2018 | Version: 1.0.9
Date latest version: 31/07/2018 | Version: 1.2.1
Date latest version: 30/01/2019 | Version: 1.2.3
Date latest version: 30/08/2019 | Version: 1.3.0
-------------------------------------------------------------------------------------
"""

def menu():
	print ""
	print "------------------------------------------------------------------------"
	print "--- 1. Emails list (default: emails.txt)                             ---"
	print "--- 2. Only one target                                               ---"
	print "--- 3. Email spoofing generate                                       ---"
	print "------------------------------------------------------------------------"
	print ""
	x = int(raw_input("Select 1/2/3: "))
	if type(x) != int:
		print "[Warning][Menu][>] Error..."
		menu()
	else:
		return x

def attack(email):
	email = email.replace("\n", "")

	if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower()):
		print "[INFO][TARGET][>] Hello, " + email + " is correct."
		ok = True
	else:
		print "[INFO][TARGET][>] Hello, " + email + " doesn't a email. Try again!'"
		ok = False
		
	if ok == True:
		url = "http://www.verifyemailaddress.org/es/"
		try:
			is_valid = validate_email(email,verify=True)
			if is_valid:
				print "[INFO][TARGET][>] " + email
				print "|--[INFO][EMAIL][>] Email validated..."
			else:
				print "[INFO][TARGET][>] " + email
				print "|--[INFO][EMAIL][>] It's not created..."
		except:
			print "[INFO][TARGET][>] " + email
			print colores.alert + "|--[INFO][EMAIL] No verification possible... " + colores.normal

	#CALL THE ACTION
	check_emailrep(email)
	check_AccountTwitter(email)
	check_wordpress(email)
	check_netflix(email)
	check_amazon(email)
	check_haveibeenpwned(email)
	check_pastebin(email)
	check_duckduckgoInfo(email)
	check_duckduckgoSmartInfo(email)

def main():
	global emails_list
	banner()
	m = menu()
	if m == 1:
		print "[INFO][Emails list][>] By default 'emails.txt'..."
		print "[INFO][Emails list][>] If you want by default, press ENTER."
		file = open(emails_list, 'r')
		for email in file.readlines():
			attack(email.replace("\n", ""))
	if m == 2:
		email = str(raw_input("Email: "))
		attack(email)
	if m == 3:
		print "-----------------------------------------------------"
		print "--               START EMAIL SPOOFING                "
		print "-----------------------------------------------------"
		print "INSTRUCTIONS: "
		print "1. Generate evilmail.php"
		print "2. Upload to hosting with email server"
		print "3. Run the evilmail.php from the browser"
		print "4. Enjoy!"
		print "-----------------------------------------------------"
		print " "

		fromm = str(raw_input("From:"))
		to = str(raw_input("To: "))
		title = str(raw_input("Title: "))
		messaje = str(raw_input("Messaje: "))
		generate_php(fromm, to, title, messaje)

	if m <0 or m > 3:
		print "|--[EO-RIPPER][SAY][>] Are you stupid?"
		print "|--[EO-RIPPER][SAY][>] 1 or 2 or 3."
	if type(m) == str:
		print "|--[EO-RIPPER][SAY][>] Are you stupid?"
		print "|--[EO-RIPPER][SAY][>] 1 or 2 or 3."

if __name__ == "__main__":
	main()
