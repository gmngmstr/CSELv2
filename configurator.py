#!/usr/bin/env python
import os, sys
import subprocess
from stat import *
from Tkinter import *

class ForenQuest:
    def __init__(self,name,question,answer,points,enabled):
        self.name = name
        self.question = question
        self.answer = answer
        self.points = points
        self.enabled = enabled
		

fq01 = ForenQuest("Question1.txt","Here is my question...","myanswer","0","0")
fq02 = ForenQuest("Question2.txt","Here is my question...","myanswer","0","0")

class AutoScrollbar(Scrollbar):
	# a scrollbar that hides itself if it's not needed. only works if you use th4e grid geometry manager.
	def set(self, lo, hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			# grid_remove is currently missing from Tkinter!
			self.tk.call("grid", "remove", self)
		else:
			self.grid()
		Scrollbar.set(self, lo, hi)
	def pack(self, **kw):
		raise TclError, "cannot use pack with this widget"
	def place(self, **kw):
		raise TclError, "cannot use place with this widget"

class Vuln:
	def __init__(self,name,points,enabled,keywords,keyWordsExtra,hit,miss,layout,tip):
		self.name = name        #What is the vulnerability called?
		self.points = points    #How many points is it worth?
		self.enabled = enabled  #Is the item being scored?
		self.kw = keywords      #Keywords to look for when scoring (Not used on all)
		self.kwe = keyWordsExtra#Extra keywords to look for when scoring (Not used on all)
		self.hm = hit           #Message to display on a hit (Not implemented on all yet)
		self.mm = miss          #Message to display on a miss (Not implemented on all yet)
		self.loc = layout		#What to put in each box
		self.tip = tip          #Explanation of the item
		
class VulnCust:
	def __init__(self,name,points,enabled,location,keywords,completionMessage,hit,miss,tip):
		self.name = name        	#What is the vulnerability called?
		self.points = points    	#How many points is it worth?
		self.enabled = enabled  	#Is the item being scored?
		self.loc = location			#Where is the item
		self.kw = keywords      	#Keywords to look for when scoring
		self.kwe = completionMessage#Message to display when completed
		self.hm = hit           	#Message to display on a hit (Not implemented on all yet)
		self.mm = miss          	#Message to display on a miss (Not implemented on all yet)
		self.tip = tip          	#Explanation of the item
		
v001 = Vuln("silentMiss","0","0","","","","","","Check this box to hide missed items\n(Similar to competition)")
v201 = Vuln("disableGuest","0","0","","","","","","Is the guest disabled in lightdm?")
v202 = Vuln("disableAutoLogin","0","0","","","","","","Is there an auto logged in user in lightdm?")
v203 = Vuln("disableUserGreeter","0","0","","","","","","Disable the user greeter in lightdm")
v204 = Vuln("disableSshRootLogin","0","0","","","","","","'PermitRootLogin no' exists in sshd_config")
v205 = Vuln("checkFirewall","0","0","","","","","","Is ufw enabled?")
v206 = Vuln("checkKernel","0","0","","","","","","Has kernel been updated?")
v207 = Vuln("avUpdated","0","0","","","","","","Has clamav freshclam been run?")
v208 = Vuln("minPassAge","0","0","","","","","","Value of min password age to score is 30 (login.defs)")
v209 = Vuln("maxPassAge","0","0","","","","","","Value of max password age to score is 60 (login.defs)")
v210 = Vuln("maxLoginTries","0","0","","","","","","Value of max login retries to score is 5 (login.defs)")
v211 = Vuln("checkPassLength","0","0","","","","","","Value min pw length is 10 (pam.d/common-password)")
v212 = Vuln("checkPassHist","0","0","","","","","","Value of passwords to remember is 5 (pam.d/common-password)")
v213 = Vuln("checkPassCompx","0","0","","","","","","Has password complexity been implemented? (pam.d/common-password)")
v301 = Vuln("goodUser","0","0","","","","","(Users)","Lose points for removing this user (use negative number) (Can take multiple entries)")
v302 = Vuln("badUser","0","0","","","","","(Users)","Remove these users to score (Can take multiple entries)")
v303 = Vuln("newUser","0","0","","","","","(Users)","This user must be created (Can take multiple entries)")
v304 = Vuln("changePassword","0","0","","","","","(Users)","User who must change password (Can take multiple entries)(Set the desired passwords before submitting)")
v305 = Vuln("removeAdmin","0","0","","","","","(Users)","Remove these users from the sudo group (Can take multiple entries)")
v306 = Vuln("groupExists","0","0","","","","","(Groups)","This group must be created (Can take multiple entries)")
v307 = Vuln("goodProgram","0","0","","","","","(Programs)","Score points by installing these programs (Can take multiple entries)")
v308 = Vuln("badProgram","0","0","","","","","(Programs)","Score points by removing these programs (Can take multiple entries)")
v309 = Vuln("GoodService","0","0","","","","","(Services)","Service that needs to be started (Can take multiple entries)")
v310 = Vuln("badService","0","0","","","","","(Services)","Service that needs to be stopped (Can take multiple entries)")
v311 = Vuln("badFile","0","0","","","","","(Location)","Score points for deleting this file (Can take multiple entries)")
v312 = Vuln("secureSudoers","0","0","","","","","(Keywords)","Words to be removed from /etc/sudoers file (Can take multiple entries)")
v313 = Vuln("checkHosts","0","0","","","","","(Keywords)","Check /etc/hosts for a specific string (Can take multiple entries)")
v314 = Vuln("checkStartup","0","0","","","","","(Keywords)","Check rc.local for a specific string (Can take multiple entries)")
v401 = Vuln("badCron","0","0","","","","","(User)(Keyword)","Check the root crontab for a specific string (Can take multiple entries)(If using multiple users be sure to include a keyword for each)")
v402 = Vuln("userInGroup","0","0","","","","","(users)(Group)","Users that need to be added to a group (Can take multiple entries)(If using multiple users be sure to include a group for each)")
v501 = VulnCust("fileContainsText1","0","0","","","","","","Custom option for requiring a word or phrase to be added to a file.(Spaces will not be counted as separate entries)")
v502 = VulnCust("fileContainsText2","0","0","","","","","","Custom option for requiring a word or phrase to be added to a file.(Spaces will not be counted as separate entries)")
v503 = VulnCust("fileNoLongerContains1","0","0","","","","","","Custom option for requiring a word or phrase to be removed from a file.(Spaces will not be counted as separate entries)")
v504 = VulnCust("fileNoLongerContains2","0","0","","","","","","Custom option for requiring a word or phrase to be removed from a file.(Spaces will not be counted as separate entries)")

vulns = [v001,v201,v202,v203,v204,v205,v206,v207,v208,v209,v210,v211,v212,v213,v301,v302,v303,v304,v305,v306,v307,v308,v309,v310,v312,v313,v314,v401,v402,v501,v502,v503,v504]

def writeToSave(name,points,enabled,locationText,keywords,keywordsExtra):
	f = open('csel.txt','a')
	if enabled == 1:
		f.write(name+'=(y)\n')
		f.write(name+'Value=('+str(points)+')\n')
		if locationText != '':
			f.write(name+'Location=('+str(locationText)+')\n')
		if keywords != '':
			f.write(name+'Keywords=('+str(keywords)+')\n')
		if keywordsExtra != '':
			f.write(name+'ExtraKeywords=('+str(keywordsExtra)+')\n')
	f.close()
		  
def writeToConfig(name,points,enabled,locationText,keywords,keywordsExtra):
	f = open('csel.cfg','a')
	if enabled == 1:
		if name == 'changePassword':
			v = open('passGet.sh','w+')
			v.write("#!/bin/bash\n\nnames=\'"+keywords+"\'\necho '' > name.txt\nIFS=\' \'\nread -ra NAME <<< \"$names\"\nfor i in \"${NAME[@]}\"; do\ngetent shadow | grep \"$i\" >> name.txt\ndone")
			v.close()
			os.chmod('passGet.sh', 0777)
			subprocess.call(['./passGet.sh'])
			with open('name.txt') as t:
				content = t.read().splitlines()
			t.close()
			passwdO = ''
			for cont in content:
				if cont != '':
					passwd = cont.split(':')
					if passwdO != '':
						passwdO = passwdO + ' ' + passwd[1]
					else:
						passwdO = passwd[1]
			keywordsExtra = passwdO.replace('$','\$')
			os.remove('passGet.sh')
			os.remove('name.txt')
		f.write(name+'=(y)\n')
		f.write(name+'Value=('+str(points)+')\n')
		if locationText != '':
			f.write(name+'Location=('+str(locationText)+')\n')
		if keywords != '':
			f.write(name+'Keywords=('+str(keywords)+')\n')
		if keywordsExtra != '':
			f.write(name+'ExtraKeywords=('+str(keywordsExtra)+')\n')
	f.close()

#Create the forensics questions and add answers to csel.cfg
def saveForQ():
	qHeader='This is a forensics question. Answer it below\n------------------------\n'
	qFooter='\n\nANSWER: <TypeAnswerHere>'
	f = open('csel.txt','a')  
	line1a = 'forensicsPath1=('+str(usrDsktp.get())+'Question1.txt)\n'
	line1b = 'forensicsAnswer1=('+fqans01.get()+')\n'
	line1c = 'checkForensicsQuestion1Value=('+str(fqpts01.get())+')\n'
	line1d = 'forensicsQuestion1='+fquest01.get()+'\n'
	line2a = 'forensicsPath2=('+str(usrDsktp.get())+'Question2.txt)\n'
	line2b = 'forensicsAnswer2=('+fqans02.get()+')\n'
	line2c = 'checkForensicsQuestion2Value=('+str(fqpts02.get())+')\n'
	line2d = 'forensicsQuestion2='+fquest02.get()+'\n'
	if fqcb01.get() != 0:
		for line in (line1a,line1b,line1c,line1d):
			f.write(line)
		g = open((str(usrDsktp.get())+'Question1.txt'),'w+')
		g.write(qHeader+fquest01.get()+qFooter)
		g.close()
	if fqcb02.get() != 0:
		for line in (line2a,line2b,line2c,line2d):
			f.write(line)
		h = open((str(usrDsktp.get())+'Question2.txt'),'w+')
		h.write(qHeader+fquest02.get()+qFooter)
		h.close()
	f.close()
	os.chmod((str(usrDsktp.get())+'Question1.txt'), 0777)
	os.chmod((str(usrDsktp.get())+'Question2.txt'), 0777)
	
def createForQ():
    qHeader='This is a forensics question. Answer it below\n------------------------\n'
    qFooter='\n\nANSWER: <TypeAnswerHere>'
    f = open('csel.cfg','a')  
    line1a = 'forensicsPath1=('+str(usrDsktp.get())+'Question1.txt)\n'
    line1b = 'forensicsAnswer1=('+fqans01.get()+')\n'
    line1c = 'checkForensicsQuestion1Value=('+str(fqpts01.get())+')\n'
    line2a = 'forensicsPath2=('+str(usrDsktp.get())+'Question2.txt)\n'
    line2b = 'forensicsAnswer2=('+fqans02.get()+')\n'
    line2c = 'checkForensicsQuestion2Value=('+str(fqpts02.get())+')\n'
    if fqcb01.get() != 0:
        for line in (line1a,line1b,line1c):
            f.write(line)
        g = open((str(usrDsktp.get())+'Question1.txt'),'w+')
        g.write(qHeader+fquest01.get()+qFooter)
        g.close()
    if fqcb02.get() != 0:
        for line in (line2a,line2b,line2c):
            f.write(line)
        h = open((str(usrDsktp.get())+'Question2.txt'),'w+')
        h.write(qHeader+fquest02.get()+qFooter)
        h.close()
    f.close()

#What happens when you click Submit?
def submitCallback():
    #We wanna use those fancy variable lists 
	global checkBoxes
	global vulns
	global pointVal
	global keyWords
	createForQ()
	f = open('csel.cfg','a')
	for vuln,checkEn,score,local,key,keyEx in zip(vulns,checkBoxes,pointVal,locationText,keyWords,keyWordsExtra):
		vuln.enabled = checkEn.get()
		vuln.points = score.get()
		vuln.loc = local.get()
		vuln.kw = key.get()
		vuln.kwe = keyEx.get()
		writeToConfig(vuln.name,vuln.points,vuln.enabled,vuln.loc,vuln.kw,vuln.kwe)
	configFooter="index=("+usrDsktp.get()+"ScoreReport.html)\n#These values will change during install\nimageScore=0\nposPoints=0\nrelease=\"\"\ninitialKernel=(%KERNEL%)\ninstallDate=(%INSTALLDATE%)\n"
	f.write(configFooter)
	f.close()
	root.destroy()
	
def saveConfig():
	#We wanna use those fancy variable lists 
	global checkBoxes
	global vulns
	global pointVal
	global keyWords
	location.config(text=usrDsktp.get())
	f = open('csel.txt','w+')
	f.write('Desktop='+usrDsktp.get()+'\n')
	f.close()
	saveForQ()
	for vuln,checkEn,score,local,key,keyEx in zip(vulns,checkBoxes,pointVal,locationText,keyWords,keyWordsExtra):
		vuln.enabled = checkEn.get()
		vuln.points = score.get()
		vuln.loc = local.get()
		vuln.kw = key.get()
		vuln.kwe = keyEx.get()
		writeToSave(vuln.name,vuln.points,vuln.enabled,vuln.loc,vuln.kw,vuln.kwe)
	tally()
	
def loadSave():
	#We wanna use those fancy variable lists 
	global checkBoxes
	global vulns
	global pointVal
	global keyWords
	with open('csel.txt') as f:
		content = f.read().splitlines()
	f.close()
	for vuln,checkEn,score,local,key,keyEx in zip(vulns,checkBoxes,pointVal,locationText,keyWords,keyWordsExtra):
		for cont in content:
			if 'Desktop=' in cont:
				usrDsktp.set(cont.replace('Desktop=',''))
				location.config(text=usrDsktp.get())
			if 'forensicsAnswer1=(' in cont:
				fqA1 = cont.replace('forensicsAnswer1=(','')
				fqA1 = fqA1.replace(')','')
				fqans01.set(fqA1)
				cont = fqA1
			if 'checkForensicsQuestion1Value=(' in cont:
				fqP1 = cont.replace('checkForensicsQuestion1Value=(','')
				fqP1 = fqP1.replace(')','')
				fqpts01.set(fqP1)
				fqcb01.set(1)
				cont = fqP1
			if 'forensicsQuestion1=' in cont:
				fQ1 = cont.replace('forensicsQuestion1=','')
				fquest01.set(fQ1)
				cont = fQ1
			if 'forensicsAnswer2=(' in cont:
				fqA2 = cont.replace('forensicsAnswer2=(','')
				fqA2 = fqA2.replace(')','')
				fqans02.set(fqA2)
				cont = fqA2
			if 'checkForensicsQuestion2Value=(' in cont:
				fqP2 = cont.replace('checkForensicsQuestion2Value=(','')
				fqP2 = fqP2.replace(')','')
				fqpts01.set(fqP2)
				fqcb02.set(1)
				cont = fqP2
			if 'forensicsQuestion2=' in cont:
				fQ2 = cont.replace('forensicsQuestion2=','')
				fquest02.set(fQ2)
				cont = fQ2
			if vuln.name+'=(y)' in cont:
				checkEn.set(1)
				cont = cont.replace(vuln.name+'=(y)','')
			if vuln.name+'Value=(' in cont:
				points = cont.replace(vuln.name+'Value=(','')
				points = points.replace(')','')
				score.set(points)
				cont = points
			if vuln.name+'=(' in cont:
				checkEn.set(1)
			if vuln.name+'Location=(' in cont:
				loca = cont.replace(vuln.name+'Location=(','')
				loca = loca.replace(')','')
				local.set(loca)
				cont = loca
			if vuln.name+'Keywords=(' in cont:
				keyWd = cont.replace(vuln.name+'Keywords=(','')
				keyWd = keyWd.replace(')','')
				key.set(keyWd)
				cont = keyWd
			if vuln.name+'ExtraKeywords=(' in cont:
				exKeyWd = cont.replace(vuln.name+'ExtraKeywords=(','')
				exKeyWd = exKeyWd.replace(')','')
				keyEx.set(exKeyWd)
				cont = exKeyWd
	tally()

def tally():
	#We wanna use those fancy variable lists 
	global checkBoxes
	global vulns
	global pointVal
	global keyWords
	#Set tally scores
	global tallyScore
	global tallyVuln
	tallyScore = 0
	tallyVuln = 0
	for vuln,checkEn,score,local,key,keyEx in zip(vulns,checkBoxes,pointVal,locationText,keyWords,keyWordsExtra):
	#We do not want the points from the goodUser catagory
		if vuln.name != 'goodUser' and vuln.name != 'silentMiss':
			if checkEn.get() == 1:
				#if vuln.name != 'badCron':
				multivuln = key.get()
				multivuln = multivuln.split(' ')
				for mtv in multivuln:
					tallyVuln = tallyVuln + 1
					tallyScore = tallyScore + score.get()
				#else:
					#tallyVuln = tallyVuln + 1
					#tallyScore = tallyScore + score.get()
	ftTally.config(text="Vulnerablilities: " + str(tallyVuln) + "\nTotal Points: " + str(tallyScore))

f = open('csel.cfg','w+')
configHeader="#!/bin/bash\n#This config file was generated by configurator.py\n\n"

f.write(configHeader)
f.close()
#######Tkinter Time!!!###############

class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master=master
		pad=3
		self._geom='200x200+0+0'
		master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		master.bind('<Escape>',self.toggle_geom)            
	def toggle_geom(self,event):
		geom=self.master.winfo_geometry()
		print(geom,self._geom)
		self.master.geometry(self._geom)
		self._geom=geom

root = Tk()
app=FullScreenApp(root)
#Initialize a crap-ton of TK vars. Can you find a more elegant way?

#Forensic Question stuff
usrDsktp = StringVar()
fqcb01 = IntVar()
fqpts01 = IntVar()
fquest01 = StringVar()
fqans01 = StringVar()
fqcb02 = IntVar()
fqpts02 = IntVar()
fquest02 = StringVar()
fqans02 = StringVar()

#Checkboxes to enable or disable an item 30
cb001 = IntVar()
cb201 = IntVar()
cb202 = IntVar()
cb203 = IntVar()
cb204 = IntVar()
cb205 = IntVar()
cb206 = IntVar()
cb207 = IntVar()
cb208 = IntVar()
cb209 = IntVar()
cb210 = IntVar()
cb211 = IntVar()
cb212 = IntVar()
cb213 = IntVar()
cb301 = IntVar()
cb302 = IntVar()
cb303 = IntVar()
cb304 = IntVar()
cb305 = IntVar()
cb306 = IntVar()
cb307 = IntVar()
cb308 = IntVar()
cb309 = IntVar()
cb310 = IntVar()
cb311 = IntVar()
cb312 = IntVar()
cb313 = IntVar()
cb314 = IntVar()
cb401 = IntVar()
cb402 = IntVar()
cb501 = IntVar()
cb502 = IntVar()
cb503 = IntVar()
cb504 = IntVar()
checkBoxes = [cb001,cb201,cb202,cb203,cb204,cb205,cb206,cb207,cb208,cb209,cb210,cb211,cb212,cb213,cb301,cb302,cb303,cb304,cb305,cb306,cb307,cb308,cb309,cb310,cb312,cb313,cb314,cb401,cb402,cb501,cb502,cb503,cb504]

#Point values for each item 30
pts001 = IntVar()
pts201 = IntVar()
pts202 = IntVar()
pts203 = IntVar()
pts204 = IntVar()
pts205 = IntVar()
pts206 = IntVar()
pts207 = IntVar()
pts208 = IntVar()
pts209 = IntVar()
pts210 = IntVar()
pts211 = IntVar()
pts212 = IntVar()
pts213 = IntVar()
pts301 = IntVar()
pts302 = IntVar()
pts303 = IntVar()
pts304 = IntVar()
pts305 = IntVar()
pts306 = IntVar()
pts307 = IntVar()
pts308 = IntVar()
pts309 = IntVar()
pts310 = IntVar()
pts311 = IntVar()
pts312 = IntVar()
pts313 = IntVar()
pts314 = IntVar()
pts401 = IntVar()
pts402 = IntVar()
pts501 = IntVar()
pts502 = IntVar()
pts503 = IntVar()
pts504 = IntVar()
pointVal = [pts001,pts201,pts202,pts203,pts204,pts205,pts206,pts207,pts208,pts209,pts210,pts211,pts212,pts213,pts301,pts302,pts303,pts304,pts305,pts306,pts307,pts308,pts309,pts310,pts312,pts313,pts314,pts401,pts402,pts501,pts502,pts503,pts504]

#These are for the location that some of the items take 30
lo001 = StringVar()
lo201 = StringVar()
lo202 = StringVar()
lo203 = StringVar()
lo204 = StringVar()
lo205 = StringVar()
lo206 = StringVar()
lo207 = StringVar()
lo208 = StringVar()
lo209 = StringVar()
lo210 = StringVar()
lo211 = StringVar()
lo212 = StringVar()
lo213 = StringVar()
lo301 = StringVar()
lo302 = StringVar()
lo303 = StringVar()
lo304 = StringVar()
lo305 = StringVar()
lo306 = StringVar()
lo307 = StringVar()
lo308 = StringVar()
lo309 = StringVar()
lo310 = StringVar()
lo311 = StringVar()
lo312 = StringVar()
lo313 = StringVar()
lo314 = StringVar()
lo401 = StringVar()
lo402 = StringVar()
lo501 = StringVar()
lo502 = StringVar()
lo503 = StringVar()
lo504 = StringVar()
locationText = [lo001,lo201,lo202,lo203,lo204,lo205,lo206,lo207,lo208,lo209,lo210,lo211,lo212,lo213,lo301,lo302,lo303,lo304,lo305,lo306,lo307,lo308,lo309,lo310,lo312,lo313,lo314,lo401,lo402,lo501,lo502,lo503,lo504]

#These are for the keywords that some of the items take (goodUser, badProgram, etc) 30
kw001 = StringVar()
kw201 = StringVar()
kw202 = StringVar()
kw203 = StringVar()
kw204 = StringVar()
kw205 = StringVar()
kw206 = StringVar()
kw207 = StringVar()
kw208 = StringVar()
kw209 = StringVar()
kw210 = StringVar()
kw211 = StringVar()
kw212 = StringVar()
kw213 = StringVar()
kw301 = StringVar()
kw302 = StringVar()
kw303 = StringVar()
kw304 = StringVar()
kw305 = StringVar()
kw306 = StringVar()
kw307 = StringVar()
kw308 = StringVar()
kw309 = StringVar()
kw310 = StringVar()
kw311 = StringVar()
kw312 = StringVar()
kw313 = StringVar()
kw314 = StringVar()
kw401 = StringVar()
kw402 = StringVar()
kw501 = StringVar()
kw502 = StringVar()
kw503 = StringVar()
kw504 = StringVar()
keyWords = [kw001,kw201,kw202,kw203,kw204,kw205,kw206,kw207,kw208,kw209,kw210,kw211,kw212,kw213,kw301,kw302,kw303,kw304,kw305,kw306,kw307,kw308,kw309,kw310,kw312,kw313,kw314,kw401,kw402,kw501,kw502,kw503,kw504]

#These are for the extra keywords that some of the items take 30
kwe001 = StringVar()
kwe201 = StringVar()
kwe202 = StringVar()
kwe203 = StringVar()
kwe204 = StringVar()
kwe205 = StringVar()
kwe206 = StringVar()
kwe207 = StringVar()
kwe208 = StringVar()
kwe209 = StringVar()
kwe210 = StringVar()
kwe211 = StringVar()
kwe212 = StringVar()
kwe213 = StringVar()
kwe301 = StringVar()
kwe302 = StringVar()
kwe303 = StringVar()
kwe304 = StringVar()
kwe305 = StringVar()
kwe306 = StringVar()
kwe307 = StringVar()
kwe308 = StringVar()
kwe309 = StringVar()
kwe310 = StringVar()
kwe311 = StringVar()
kwe312 = StringVar()
kwe313 = StringVar()
kwe314 = StringVar()
kwe401 = StringVar()
kwe402 = StringVar()
kwe501 = StringVar()
kwe502 = StringVar()
kwe503 = StringVar()
kwe504 = StringVar()
keyWordsExtra = [kwe001,kwe201,kwe202,kwe203,kwe204,kwe205,kwe206,kwe207,kwe208,kwe209,kwe210,kwe211,kwe212,kwe213,kwe301,kwe302,kwe303,kwe304,kwe305,kwe306,kwe307,kwe308,kwe309,kwe310,kwe312,kwe313,kwe314,kwe401,kwe402,kwe501,kwe502,kwe503,kwe504]

#Initialize tally variables
tallyScore = IntVar()
tallyVuln = IntVar()
tallyed = StringVar()

root.title('CSEL Setup Tool')

#Scrollbar set
vscrollbar = AutoScrollbar(root)
vscrollbar.grid(row=0, column=1, sticky=N+S)
hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=E+W)

canvas = Canvas(root, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
vscrollbar.config(command=canvas.yview)
hscrollbar.config(command=canvas.xview)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
#Frame creation
frame = Frame(canvas)
frame.rowconfigure(1, weight=1)
frame.columnconfigure(3, weight=1)
frame.columnconfigure(2, weight=1)

frame1 = Frame(canvas)
frame1.rowconfigure(1, weight=1)
frame1.columnconfigure(3, weight=1)
frame1.columnconfigure(2, weight=1)

frame2 = Frame(canvas)
frame2.rowconfigure(1, weight=1)
frame2.columnconfigure(3, weight=1)
frame2.columnconfigure(2, weight=1)

frame3 = Frame(canvas)
frame3.rowconfigure(1, weight=1)
frame3.columnconfigure(3, weight=1)
frame3.columnconfigure(2, weight=1)

frame4 = Frame(canvas)
frame4.rowconfigure(1, weight=1)
frame4.columnconfigure(3, weight=1)
frame4.columnconfigure(2, weight=1)

frame5 = Frame(canvas)
frame5.rowconfigure(1, weight=1)
frame5.columnconfigure(3, weight=1)
frame5.columnconfigure(2, weight=1)

#Making some boxes
#Frame0
scoreLoc = "LOCATION MISSING!"
userDesktop = Entry(frame,textvariable=usrDsktp)
location = Label(frame,text=scoreLoc)
userDesktopLabel = Label(frame,text="Path to Score Report and Forensics\nEx: /home/fred/Desktop/\nDon't forget the trailing '/'")
saveButton = Button(frame,text='Save',command=saveConfig)
loadButton = Button(frame,text='Load',command=loadSave)
checkbox001 = Checkbutton(frame,text=v001.name,variable=cb001)
label001 = Label(frame,text=v001.tip)
submit = Button(frame,text='Write to Config',command=submitCallback)
#Frame1
fqHead1 = Label(frame1,text="Create?",font=('Verdana',10,'bold'))
fqHead2 = Label(frame1,text="Points",font=('Verdana',10,'bold'))
fqHead3 = Label(frame1,text="Question",font=('Verdana',10,'bold'))
fqHead4 = Label(frame1,text="Answer",font=('Verdana',10,'bold'))
ftTally = Label(frame,text="Vulnerablilities: 0\nTotal Points: 0",font=('Verdana',10,'bold'))
fqCheckbox01 = Checkbutton(frame1,text=fq01.name,variable=fqcb01)
fqPoints01 = Entry(frame1,width=5,textvariable=fqpts01)
fqQuest01 = Entry(frame1,textvariable=fquest01)
fqAns01 = Entry(frame1,textvariable=fqans01)
fqCheckbox02 = Checkbutton(frame1,text=fq02.name,variable=fqcb02)
fqPoints02 = Entry(frame1,width=5,textvariable=fqpts02)
fqQuest02 = Entry(frame1,textvariable=fquest02)
fqAns02 = Entry(frame1,textvariable=fqans02)
#Frame2
head1 = Label(frame2,text="Score?",font=('Verdana',10,'bold'))
head2 = Label(frame2,text="Point Value",font=('Verdana',10,'bold'))
head3 = Label(frame2,text="Explanation",font=('Verdana',10,'bold'))
checkbox201 = Checkbutton(frame2,text=v201.name,variable=cb201)
points201 = Entry(frame2,width=5,textvariable=pts201)
label201 = Label(frame2,text=v201.tip)
checkbox202 = Checkbutton(frame2,text=v202.name,variable=cb202)
points202 = Entry(frame2,width=5,textvariable=pts202)
label202 = Label(frame2,text=v202.tip)
checkbox203 = Checkbutton(frame2,text=v203.name,variable=cb203)
points203 = Entry(frame2,width=5,textvariable=pts203)
label203 = Label(frame2,text=v203.tip)
checkbox204 = Checkbutton(frame2,text=v204.name,variable=cb204)
points204 = Entry(frame2,width=5,textvariable=pts204)
label204 = Label(frame2,text=v204.tip)
checkbox205 = Checkbutton(frame2,text=v205.name,variable=cb205)
points205 = Entry(frame2,width=5,textvariable=pts205)
label205 = Label(frame2,text=v205.tip)
checkbox206 = Checkbutton(frame2,text=v206.name,variable=cb206)
points206 = Entry(frame2,width=5,textvariable=pts206)
label206 = Label(frame2,text=v206.tip)
checkbox207 = Checkbutton(frame2,text=v207.name,variable=cb207)
points207 = Entry(frame2,width=5,textvariable=pts207)
label207 = Label(frame2,text=v207.tip)
checkbox208 = Checkbutton(frame2,text=v208.name,variable=cb208)
points208 = Entry(frame2,width=5,textvariable=pts208)
label208 = Label(frame2,text=v208.tip)
checkbox209 = Checkbutton(frame2,text=v209.name,variable=cb209)
points209 = Entry(frame2,width=5,textvariable=pts209)
label209 = Label(frame2,text=v209.tip)
checkbox210 = Checkbutton(frame2,text=v210.name,variable=cb210)
points210 = Entry(frame2,width=5,textvariable=pts210)
label210 = Label(frame2,text=v210.tip)
checkbox211 = Checkbutton(frame2,text=v211.name,variable=cb211)
points211 = Entry(frame2,width=5,textvariable=pts211)
label211 = Label(frame2,text=v211.tip)
checkbox212 = Checkbutton(frame2,text=v212.name,variable=cb212)
points212 = Entry(frame2,width=5,textvariable=pts212)
label212 = Label(frame2,text=v212.tip)
checkbox213 = Checkbutton(frame2,text=v213.name,variable=cb213)
points213 = Entry(frame2,width=5,textvariable=pts213)
label213 = Label(frame2,text=v213.tip)
#Gettting into the fancier vulnerabilities now
#Frame3
head4 = Label(frame3,text="Score?",font=('Verdana',10,'bold'))
head5 = Label(frame3,text="Point Value",font=('Verdana',10,'bold'))
head6 = Label(frame3,text="Keywords/Values",font=('Verdana',10,'bold'))
head7 = Label(frame3,text="Textbox Contents",font=('Verdana',10,'bold'))
head8 = Label(frame3,text="Explanation (Add a space in between entries)",font=('Verdana',10,'bold'))
checkbox301 = Checkbutton(frame3,text=v301.name,variable=cb301)
points301 = Entry(frame3,width=5,textvariable=pts301)
keywords301 = Entry(frame3,textvariable=kw301)
location301 = Label(frame3,text=v301.loc)
label301 = Label(frame3,text=v301.tip)
checkbox302 = Checkbutton(frame3,text=v302.name,variable=cb302)
points302 = Entry(frame3,width=5,textvariable=pts302)
keywords302 = Entry(frame3,textvariable=kw302)
location302 = Label(frame3,text=v302.loc)
label302 = Label(frame3,text=v302.tip)
checkbox303 = Checkbutton(frame3,text=v303.name,variable=cb303)
points303 = Entry(frame3,width=5,textvariable=pts303)
keywords303 = Entry(frame3,textvariable=kw303)
location303 = Label(frame3,text=v303.loc)
label303 = Label(frame3,text=v303.tip)
checkbox304 = Checkbutton(frame3,text=v304.name,variable=cb304)
points304 = Entry(frame3,width=5,textvariable=pts304)
keywords304 = Entry(frame3,textvariable=kw304)
location304 = Label(frame3,text=v304.loc)
label304 = Label(frame3,text=v304.tip)
checkbox305 = Checkbutton(frame3,text=v305.name,variable=cb305)
points305 = Entry(frame3,width=5,textvariable=pts305)
keywords305 = Entry(frame3,textvariable=kw305)
location305 = Label(frame3,text=v305.loc)
label305 = Label(frame3,text=v305.tip)
checkbox306 = Checkbutton(frame3,text=v306.name,variable=cb306)
points306 = Entry(frame3,width=5,textvariable=pts306)
keywords306 = Entry(frame3,textvariable=kw306)
location306 = Label(frame3,text=v306.loc)
label306 = Label(frame3,text=v306.tip)
checkbox307 = Checkbutton(frame3,text=v307.name,variable=cb307)
points307 = Entry(frame3,width=5,textvariable=pts307)
keywords307 = Entry(frame3,textvariable=kw307)
location307 = Label(frame3,text=v307.loc)
label307 = Label(frame3,text=v307.tip)
checkbox308 = Checkbutton(frame3,text=v308.name,variable=cb308)
points308 = Entry(frame3,width=5,textvariable=pts308)
keywords308 = Entry(frame3,textvariable=kw308)
location308 = Label(frame3,text=v308.loc)
label308 = Label(frame3,text=v308.tip)
checkbox309 = Checkbutton(frame3,text=v309.name,variable=cb309)
points309 = Entry(frame3,width=5,textvariable=pts309)
keywords309 = Entry(frame3,textvariable=kw309)
location309 = Label(frame3,text=v309.loc)
label309 = Label(frame3,text=v309.tip)
checkbox310 = Checkbutton(frame3,text=v310.name,variable=cb310)
points310 = Entry(frame3,width=5,textvariable=pts310)
keywords310 = Entry(frame3,textvariable=kw310)
location310 = Label(frame3,text=v310.loc)
label310 = Label(frame3,text=v310.tip)
checkbox311 = Checkbutton(frame3,text=v311.name,variable=cb311)
points311 = Entry(frame3,width=5,textvariable=pts311)
keywords311 = Entry(frame3,textvariable=kw311)
location311 = Label(frame3,text=v311.loc)
label311 = Label(frame3,text=v311.tip)
checkbox312 = Checkbutton(frame3,text=v312.name,variable=cb312)
points312 = Entry(frame3,width=5,textvariable=pts312)
keywords312 = Entry(frame3,textvariable=kw312)
location312 = Label(frame3,text=v312.loc)
label312 = Label(frame3,text=v312.tip)
checkbox313 = Checkbutton(frame3,text=v313.name,variable=cb313)
points313 = Entry(frame3,width=5,textvariable=pts313)
keywords313 = Entry(frame3,textvariable=kw313)
location313 = Label(frame3,text=v313.loc)
label313 = Label(frame3,text=v313.tip)
checkbox314 = Checkbutton(frame3,text=v314.name,variable=cb314)
points314 = Entry(frame3,width=5,textvariable=pts314)
keywords314 = Entry(frame3,textvariable=kw314)
location314 = Label(frame3,text=v314.loc)
label314 = Label(frame3,text=v314.tip)
#Frame4
head9 = Label(frame4,text="Score?",font=('Verdana',10,'bold'))
head10 = Label(frame4,text="Point Value",font=('Verdana',10,'bold'))
head11 = Label(frame4,text="Keywords/Values",font=('Verdana',10,'bold'))
head12 = Label(frame4,text="Extra Keywords/Values",font=('Verdana',10,'bold'))
head13 = Label(frame4,text="Textbox Contents",font=('Verdana',10,'bold'))
head14 = Label(frame4,text="Explanation (Add a space in between entries)",font=('Verdana',10,'bold'))
checkbox401 = Checkbutton(frame4,text=v401.name,variable=cb401)
points401 = Entry(frame4,width=5,textvariable=pts401)
keywords401 = Entry(frame4,textvariable=kw401)
keywordsE401 = Entry(frame4,textvariable=kwe401)
location401 = Label(frame4,text=v401.loc)
label401 = Label(frame4,text=v401.tip)
checkbox402 = Checkbutton(frame4,text=v402.name,variable=cb402)
points402 = Entry(frame4,width=5,textvariable=pts402)
keywords402 = Entry(frame4,textvariable=kw402)
keywordsE402 = Entry(frame4,textvariable=kwe402)
location402 = Label(frame4,text=v402.loc)
label402 = Label(frame4,text=v402.tip)
#Frame5
head15 = Label(frame5,text="Score?",font=('Verdana',10,'bold'))
head16 = Label(frame5,text="Point Value",font=('Verdana',10,'bold'))
head17 = Label(frame5,text="File Location",font=('Verdana',10,'bold'))
head18 = Label(frame5,text="Keywords/Values",font=('Verdana',10,'bold'))
head19 = Label(frame5,text="Completion Message",font=('Verdana',10,'bold'))
head20 = Label(frame5,text="Explanation ",font=('Verdana',10,'bold'))
checkbox501 = Checkbutton(frame5,text=v501.name,variable=cb501)
points501 = Entry(frame5,width=5,textvariable=pts501)
fLocation501 = Entry(frame5,textvariable=lo501)
keywords501 = Entry(frame5,textvariable=kw501)
keywordsE501 = Entry(frame5,textvariable=kwe501)
label501 = Label(frame5,text=v501.tip)
checkbox502 = Checkbutton(frame5,text=v502.name,variable=cb502)
points502 = Entry(frame5,width=5,textvariable=pts502)
fLocation502 = Entry(frame5,textvariable=lo502)
keywords502 = Entry(frame5,textvariable=kw502)
keywordsE502 = Entry(frame5,textvariable=kwe502)
label502 = Label(frame5,text=v502.tip)
checkbox503 = Checkbutton(frame5,text=v503.name,variable=cb503)
points503 = Entry(frame5,width=5,textvariable=pts503)
fLocation503 = Entry(frame5,textvariable=lo503)
keywords503 = Entry(frame5,textvariable=kw503)
keywordsE503 = Entry(frame5,textvariable=kwe503)
label503 = Label(frame5,text=v503.tip)
checkbox504 = Checkbutton(frame5,text=v504.name,variable=cb504)
points504 = Entry(frame5,width=5,textvariable=pts504)
fLocation504 = Entry(frame5,textvariable=lo504)
keywords504 = Entry(frame5,textvariable=kw504)
keywordsE504 = Entry(frame5,textvariable=kwe504)
label504 = Label(frame5,text=v504.tip)

#Pack it up...errr GRID it up!
#Frame0
location.grid(row=0,column=1)
userDesktop.grid(row=0,column=2)
userDesktopLabel.grid(row=0,column=3,sticky=W)
saveButton.grid(row=0,column=4,sticky=W)
loadButton.grid(row=1,column=4,sticky=W)
checkbox001.grid(row=1,column=1,sticky=W)
label001.grid(row=1,column=2,sticky=W)
ftTally.grid(row=2,column=1,sticky=W)
submit.grid(row=2,column=4)
#Frame1
fqHead1.grid(row=0,column=1)
fqHead2.grid(row=0,column=2)
fqHead3.grid(row=0,column=3)
fqHead4.grid(row=0,column=4,sticky=W)
fqCheckbox01.grid(row=5,column=1,sticky=W)
fqPoints01.grid(row=5,column=2)
fqQuest01.grid(row=5,column=3)
fqAns01.grid(row=5,column=4,sticky=W) 
fqCheckbox02.grid(row=6,column=1,sticky=W)
fqPoints02.grid(row=6,column=2)
fqQuest02.grid(row=6,column=3)
fqAns02.grid(row=6,column=4,sticky=W)
#Frame2
head1.grid(row=0,column=1)
head2.grid(row=0,column=2)
head3.grid(row=0,column=3)
checkbox201.grid(row=1,column=1,sticky=W)
points201.grid(row=1,column=2)
label201.grid(row=1,column=3,sticky=W)
checkbox202.grid(row=2,column=1,sticky=W)
points202.grid(row=2,column=2)
label202.grid(row=2,column=3,sticky=W)
checkbox203.grid(row=3,column=1,sticky=W)
points203.grid(row=3,column=2)
label203.grid(row=3,column=3,sticky=W)
checkbox204.grid(row=4,column=1,sticky=W)
points204.grid(row=4,column=2)
label204.grid(row=4,column=3,sticky=W)
checkbox205.grid(row=5,column=1,sticky=W)
points205.grid(row=5,column=2)
label205.grid(row=5,column=3,sticky=W)
checkbox206.grid(row=6,column=1,sticky=W)
points206.grid(row=6,column=2)
label206.grid(row=6,column=3,sticky=W)
checkbox207.grid(row=7,column=1,sticky=W)
points207.grid(row=7,column=2)
label207.grid(row=7,column=3,sticky=W)
checkbox208.grid(row=8,column=1,sticky=W)
points208.grid(row=8,column=2)
label208.grid(row=8,column=3,sticky=W)
checkbox209.grid(row=9,column=1,sticky=W)
points209.grid(row=9,column=2)
label209.grid(row=9,column=3,sticky=W)
checkbox210.grid(row=10,column=1,sticky=W)
points210.grid(row=10,column=2)
label210.grid(row=10,column=3,sticky=W)
checkbox211.grid(row=11,column=1,sticky=W)
points211.grid(row=11,column=2)
label211.grid(row=11,column=3,sticky=W)
checkbox212.grid(row=12,column=1,sticky=W)
points212.grid(row=12,column=2)
label212.grid(row=12,column=3,sticky=W)
checkbox213.grid(row=13,column=1,sticky=W)
points213.grid(row=13,column=2)
label213.grid(row=13,column=3,sticky=W)
#Frame3
head4.grid(row=0,column=1)
head5.grid(row=0,column=2)
head6.grid(row=0,column=3)
head7.grid(row=0,column=4)
head8.grid(row=0,column=5)
checkbox301.grid(row=1,column=1,sticky=W)
points301.grid(row=1,column=2)
keywords301.grid(row=1,column=3)
location301.grid(row=1,column=4,sticky=W)
label301.grid(row=1,column=5,sticky=W)
checkbox302.grid(row=2,column=1,sticky=W)
points302.grid(row=2,column=2)
keywords302.grid(row=2,column=3)
location302.grid(row=2,column=4,sticky=W)
label302.grid(row=2,column=5,sticky=W)
checkbox303.grid(row=3,column=1,sticky=W)
points303.grid(row=3,column=2)
keywords303.grid(row=3,column=3)
location303.grid(row=3,column=4,sticky=W)
label303.grid(row=3,column=5,sticky=W)
checkbox304.grid(row=4,column=1,sticky=W)
points304.grid(row=4,column=2)
keywords304.grid(row=4,column=3)
location304.grid(row=4,column=4,sticky=W)
label304.grid(row=4,column=5,sticky=W)
checkbox305.grid(row=5,column=1,sticky=W)
points305.grid(row=5,column=2)
keywords305.grid(row=5,column=3)
location305.grid(row=5,column=4,sticky=W)
label305.grid(row=5,column=5,sticky=W)
checkbox306.grid(row=6,column=1,sticky=W)
points306.grid(row=6,column=2)
keywords306.grid(row=6,column=3)
location306.grid(row=6,column=4,sticky=W)
label306.grid(row=6,column=5,sticky=W)
checkbox307.grid(row=7,column=1,sticky=W)
points307.grid(row=7,column=2)
keywords307.grid(row=7,column=3)
location307.grid(row=7,column=4,sticky=W)
label307.grid(row=7,column=5,sticky=W)
checkbox308.grid(row=8,column=1,sticky=W)
points308.grid(row=8,column=2)
keywords308.grid(row=8,column=3)
location308.grid(row=8,column=4,sticky=W)
label308.grid(row=8,column=5,sticky=W)
checkbox309.grid(row=9,column=1,sticky=W)
points309.grid(row=9,column=2)
keywords309.grid(row=9,column=3)
location309.grid(row=9,column=4,sticky=W)
label309.grid(row=9,column=5,sticky=W)
checkbox310.grid(row=10,column=1,sticky=W)
points310.grid(row=10,column=2)
keywords310.grid(row=10,column=3)
location310.grid(row=10,column=4,sticky=W)
label310.grid(row=10,column=5,sticky=W)
checkbox311.grid(row=11,column=1,sticky=W)
points311.grid(row=11,column=2)
keywords311.grid(row=11,column=3)
location311.grid(row=11,column=4,sticky=W)
label311.grid(row=11,column=5,sticky=W)
checkbox312.grid(row=12,column=1,sticky=W)
points312.grid(row=12,column=2)
keywords312.grid(row=12,column=3)
location312.grid(row=12,column=4,sticky=W)
label312.grid(row=12,column=5,sticky=W)
checkbox313.grid(row=13,column=1,sticky=W)
points313.grid(row=13,column=2)
keywords313.grid(row=13,column=3)
location313.grid(row=13,column=4,sticky=W)
label313.grid(row=13,column=5,sticky=W)
checkbox314.grid(row=14,column=1,sticky=W)
points314.grid(row=14,column=2)
keywords314.grid(row=14,column=3)
location314.grid(row=14,column=4,sticky=W)
label314.grid(row=14,column=5,sticky=W)
#Frame4
head9.grid(row=0,column=1)
head10.grid(row=0,column=2)
head11.grid(row=0,column=3)
head12.grid(row=0,column=4)
head13.grid(row=0,column=5)
head14.grid(row=0,column=6)
checkbox401.grid(row=1,column=1,sticky=W)
points401.grid(row=1,column=2)
keywords401.grid(row=1,column=3)
keywordsE401.grid(row=1,column=4)
location401.grid(row=1,column=5,sticky=W)
label401.grid(row=1,column=6,sticky=W)
checkbox402.grid(row=2,column=1,sticky=W)
points402.grid(row=2,column=2)
keywords402.grid(row=2,column=3)
keywordsE402.grid(row=2,column=4)
location402.grid(row=2,column=5,sticky=W)
label402.grid(row=2,column=6,sticky=W)
#Frame5
head15.grid(row=0,column=1)
head16.grid(row=0,column=2)
head17.grid(row=0,column=3)
head18.grid(row=0,column=4)
head19.grid(row=0,column=5)
head20.grid(row=0,column=6)
checkbox501.grid(row=1,column=1,sticky=W)
points501.grid(row=1,column=2)
fLocation501.grid(row=1,column=3)
keywords501.grid(row=1,column=4)
keywordsE501.grid(row=1,column=5)
label501.grid(row=1,column=6,sticky=W)
checkbox502.grid(row=2,column=1,sticky=W)
points502.grid(row=2,column=2)
fLocation502.grid(row=2,column=3)
keywords502.grid(row=2,column=4)
keywordsE502.grid(row=2,column=5)
label502.grid(row=2,column=6,sticky=W)
checkbox503.grid(row=3,column=1,sticky=W)
points503.grid(row=3,column=2)
fLocation503.grid(row=3,column=3)
keywords503.grid(row=3,column=4)
keywordsE503.grid(row=3,column=5)
label503.grid(row=3,column=6,sticky=W)
checkbox504.grid(row=4,column=1,sticky=W)
points504.grid(row=4,column=2)
fLocation504.grid(row=4,column=3)
keywords504.grid(row=4,column=4)
keywordsE504.grid(row=4,column=5)
label504.grid(row=4,column=6,sticky=W)

#Frame positioning
#Each item added or removed is worth 20
canvas.create_window(0, 0, anchor=NW, window=frame)
canvas.create_window(0, 120, anchor=NW, window=frame1)
canvas.create_window(0, 200, anchor=NW, window=frame2)
canvas.create_window(0, 500, anchor=NW, window=frame3)
canvas.create_window(0, 820, anchor=NW, window=frame4)
canvas.create_window(0, 900, anchor=NW, window=frame5)

frame.update_idletasks()
frame1.update_idletasks()
frame2.update_idletasks()
frame3.update_idletasks()
frame4.update_idletasks()
frame5.update_idletasks()

canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
