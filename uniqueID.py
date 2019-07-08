from Tkinter import *

def retrieve():
	f = open('/usr/local/bin/uniqueId','w+')
	line1 = 'TeamName: ' + str(teamID.get()) + '\n'
	line2 = 'StudentName: ' + str(studentID.get()) + '\n'
	line3 = 'SchoolName: ' + str(schoolID.get()) + '\n'
	line4 = 'TeacherName: ' + str(teacherID.get()) + '\n'
	line5 = 'Grade: ' + str(grade.get())
	for line in (line1, line2, line3, line4, line5):
		f.write(line)
	f.close()
	root.destroy()

def center(master):
		screen_w = master.winfo_screenwidth()
		screen_h = master.winfo_screenheight()
		size = tuple(int(_) for _ in master.geometry().split('+')[0].split('x'))
		x = screen_w/2 - size[0]
		y = screen_h/2 - size[1]
		master.geometry("+%d+%d" % (x, y))

root = Tk()
root.title('Unique ID')
center(root)
teamID = StringVar()
studentID = StringVar()
schoolID = StringVar()
teacherID = StringVar()
grade = StringVar()
frame = Frame(root)
frame.pack()
Label(frame,text='Enter your credentials for the scoreboard',font=('Verdana',10,'bold')).grid(row=0,column=0,columnspan=2)
Label(frame,text='Team Name: ',font=('Verdana',10,'bold'),width=20).grid(row=1,column=0)
Entry(frame,textvariable=teamID,width=20).grid(row=1,column=1)
Label(frame,text='Student Name: ',font=('Verdana',10,'bold'),width=20).grid(row=2,column=0)
Entry(frame,textvariable=studentID,width=20).grid(row=2,column=1)
Label(frame,text='School Name: ',font=('Verdana',10,'bold'),width=20).grid(row=3,column=0)
Entry(frame,textvariable=schoolID,width=20).grid(row=3,column=1)
Label(frame,text='Teacher Name: ',font=('Verdana',10,'bold'),width=20).grid(row=4,column=0)
Entry(frame,textvariable=teacherID,width=20).grid(row=4,column=1)
Label(frame,text='Grade: ',font=('Verdana',10,'bold'),width=20).grid(row=5,column=0)
Entry(frame,textvariable=grade,width=20).grid(row=5,column=1)
Button(frame,text='Submit',command=retrieve).grid(row=6,column=0,columnspan=2)
frame.update_idletasks()

root.mainloop()