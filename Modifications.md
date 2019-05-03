#List of modifications to install.sh
Added python and python tk installer
Modified crontab entry
Added CCC and SoCalCCCC logos
Added a line to create a linked file from the /usr/local/bin/ to the desktop for the scoring report
Removed installer for python an python-tk and moved them to an initiate.sh and added a line to launch the configurator.py

#List of modifications to configurator.py
Added a full save function
Added a load function
Added extra info to explanations
Added a hide-able scroll bar
Removed create forensic question button and moved functionality to save button
Added a second section for keywords in the initializer and the corresponding variables
Added a tally for scores and items
Separated the options into section based on info required
Moved v08 to frame
Moved v01-v07 to frame1
Moved forensic questions to frame2
Moved v50-v65 to frame3
Moved v85 to v68 and added to frame4
Moved v66-v67 to frame4
Moved v81-v84 to frame5
Added a text-box to v66-v68
Added another section to Vuln for text-box layout
Added VulnCust class for v81-v84
Added 3 more boxes to v81-v84
Adjusted save and load option to accommodate new info
Adjusted submit option to accommodate new info
Moved password to frame3
Moved password policy to frame2
Adjust file creation for forensic questions
Rearranged program for readability
Renamed many variables for readability
Added option for goodService
Renamed serviceRunning to badService
Added password complexity and password history options
Made window start full-screen
Modified variables to save the scoring report to the same location a the scoring engine to remove ghosting on the desktop
Made 'Write to Config' also run install.sh

#List of modifications to payload
Fixed score totaler
Added multi item scoring to most categories
Added service check option
Modified password checker with testing for current password
Modified options with keywords
Modified options with extrakeywords 2 parameters
Modified userInGroup + points
Modified options with location 3 parameters + points
Rearranged program for readability
Added check for sshrootlogin option
Added option for goodService
Renamed serviceRunning to badService
Modified password history
Added password complexity option
Added CCC and SoCalCCCC logos and my information as a modifier/updater
Added notifications for gaining and loosing points

#TODO
*Add install updates frequency option

*Retest everything

*Make Readme generator and setting setter
*Update all of the explanations