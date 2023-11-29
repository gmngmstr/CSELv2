#!/bin/bash
if [ "$EUID" -ne 0 ] ;  then 
	echo "installer must be run as root"
	exit
fi
#Merge the config with the code, output it to csel file
echo 'Merging csel.cfg with payload...'
cat csel.cfg payload > /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH
sed -i "s/%KERNEL%/"`uname -r`"/g" /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH
sed -i "s/%INSTALLDATE%/"`date +%s`"/g" /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH
echo -e 'DONE\nInstalling csel into /usr/local/bin...'
chmod 777 /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH #Make it executable
cp ./uniqueID.py /usr/local/bin/uniqueID.py
if [[ $( grep 'FTPServer' csel.cfg ) ]] ;  then
	cp ./csel_SCORING_REPORT_FTP_DO_NO_TOUCH.sh /usr/local/bin/csel_SCORING_REPORT_FTP_DO_NO_TOUCH
	chmod 777 /usr/local/bin/csel_SCORING_REPORT_FTP_DO_NO_TOUCH #Make it executable
	cp ./FTP.txt /usr/local/bin/FTP.txt
	if [[ $(crontab -l -u root | grep FTP) ]] ; then :; else
		(crontab -l -u root ; echo "* * * * * /usr/local/bin/csel_SCORING_REPORT_FTP_DO_NO_TOUCH") | crontab -
	fi
fi
#Check for crontab entry, add it if it doesn't exist
echo -e 'DONE\nAdding crontab entry...'
if [[ $(crontab -l -u root | grep ENGINE) ]] ; then :; else
	(crontab -l -u root ; echo "1 * * * * /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH") | crontab -
fi

#Check for CYBER folder, create if it doesn't exist
echo -e 'DONE\nCreating /etc/CYBERPATRIOT directory for icons...'
if [ ! -d "/etc/CYBERPATRIOT_DO_NOT_REMOVE" ]
then
	#Add the images for the scoring report to the computer
	mkdir /etc/CYBERPATRIOT_DO_NOT_REMOVE
	cp logo.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/logo.png
	cp iguana.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/iguana.png
	cp CCC_logo.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/CCC_logo.png
	cp SoCalCCCC.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/SoCalCCCC.png
	touch /etc/CYBERPATRIOT_DO_NOT_REMOVE/score
	#Check for python and python-tk, install if not installed
	apt-get install python python-tk -y
	echo 'Python and python-tk is installed.'
	#Launch the configurator
	python configurator.py
	exit 1
fi

#Fire csel to create the initial Score Report
echo -e 'DONE\nFiring csel for the first time...'
/usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH 

#Finish up
scoreReportLoc=$( grep -Po '(?<=indexD=\().*?(?=\))' csel.cfg )
cd $scoreReportLoc
rm ScoreReport.html
ln /usr/local/bin/ScoreReport.html
echo -e 'DONE\n----------------------------------\n\nScore Report is located at:' $scoreReportLoc
