#!/bin/bash

#Merge the config with the code, output it to csel file
echo 'Merging csel.cfg with payload...'
cat csel.cfg payload > /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH
sed -i "s/%KERNEL%/"`uname -r`"/g" /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH
sed -i "s/%INSTALLDATE%/"`date +%s`"/g" /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH
echo -e 'DONE\nInstalling csel into /usr/local/bin...'
chmod 777 /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH #Make it executable

#Check for crontab entry, add it if it doesn't exist
echo -e 'DONE\nAdding crontab entry...'
if [[ $(crontab -l -u root | grep csel) ]] ; then :; else
	(crontab -l -u root ; echo "* * * * * /usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH")| crontab -
fi

#Check for CYBER folder, create if it doesn't exist
echo -e 'DONE\nCreating /etc/CYBERPATRIOT directory for icons...'
if [ ! -d "/etc/CYBERPATRIOT_DO_NOT_REMOVE" ]
then
	mkdir /etc/CYBERPATRIOT_DO_NOT_REMOVE
	cp logo.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/logo.png
	cp iguana.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/iguana.png
	cp CCC_logo.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/CCC_logo.png
	cp SoCalCCCC.png /etc/CYBERPATRIOT_DO_NOT_REMOVE/SoCalCCCC.png
	touch /etc/CYBERPATRIOT_DO_NOT_REMOVE/score
fi

#Check for Pyhton, install if not insalled
apt-get install python python-tk -y
echo 'Python and python-tk is installed.'

#Fire csel to create the initial Score Report
echo -e 'DONE\nFiring csel for the first time...'
/usr/local/bin/csel_SCORING_ENGINE_DO_NOT_TOUCH

#Finish up
scoreReportLoc=$( grep -Po '(?<=indexD=\().*?(?=\))' csel.cfg )
cd $scoreReportLoc
ln  /usr/local/bin/ScoreReport.html
echo -e 'DONE\n----------------------------------\n\nScore Report is located at:' $scoreReportLoc
