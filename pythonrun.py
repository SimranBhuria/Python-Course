#Including the tkinter module in the file to build a GUI
import tkinter 
from tkinter.constants import *
# Including the messagebox to produce pop up windows for errors, warnings or info.
import tkinter.messagebox
import subprocess
from subprocess import CalledProcessError
import sys
import re

import py_compile
from py_compile import PyCompileError



# create the root GUI window
tk = tkinter.Tk()

# Creating a new GUIwindow
GUIwindow = tkinter.Frame(tk, relief=RIDGE, borderwidth=10, bg="dark orchid",width=1024, height=600)
# Placing the GUI window with the help of the grid layout manager.
GUIwindow.grid(column=0, row=0)    
##  register the window with the geometry manager, so that is displayed
## in the GUI, else it will not be displayed:
GUIwindow.grid(padx=1, pady=1)
# to fix the window's size, the following is also needed:
GUIwindow.grid_propagate(0) 


#Creating spaces for entering text.
inputTextArea = tkinter.Text(GUIwindow, borderwidth=5, width=60,height=33)
#Placing it appropriately
inputTextArea.grid(row=2, column=1, rowspan=3)

#Creating spaces for entering text.
inputTextArea1 = tkinter.Text(GUIwindow, borderwidth=5, width=60,height=10)
#Placing it appropriately
inputTextArea1.grid(row=4, column=4)


outputContents = tkinter.StringVar()
#Creating an area to display text 
displayTextArea = tkinter.Frame(GUIwindow, relief=RIDGE, borderwidth=5, width=500, height=300)
displayTextArea.grid(column=4,row=2)
displayTextArea.grid_propagate(0)


# Creating a label for the text area that we created above. 
displayLabel = tkinter.Label(displayTextArea, borderwidth=5)
# Setting the text for the label  
displayLabel['textvariable'] = outputContents
# Placing the label on the window. 
displayLabel.pack(fill=X, expand=1, side=TOP)
 
displayLabel.grid(column=0, row=0)

def process(f):
   with open('test.py') as fin, open('Code.py','w+') as fout:
      for line in fin:
        if 'input' in line:
            
            k=f.strip()
            if k.isalpha():
               g='"'+k+'"'
            rest = line.split('input', 1)[0]
            
            if '=' not in line:
                a = line[line.find('(')+len('('):line.rfind(')')]   
                         
                g=line.replace(a,g,1)
                fout.write(g)         
                             
            else:
              fout.write(rest.strip()+g+"\n")
        else:
            fout.write(line)
   
   
   with open("output.txt", "w") as f:
           try:  
             subprocess.check_call(["python", "Code.py"], stdout=f, stderr=f)
           except CalledProcessError as e:
             output = e.output
   display_output()
   
def get_input(event):
  if event.keysym == 'Return':   
    process(inputTextArea1.get(0.0,END))



def finput():
    fout=open("test.py", 'r')
    d=open("output.txt",'w')
    for line in fout:
        
        if 'input' in line:
            e=re.findall('"([^"]*)"',line)
            
            
            break
    try:
       d.write(e[0]+"  " +'(Input Required)')
       display_output() 
       d.close()
       fout.close()       
    except IndexError as e:
       with open("output.txt", "w") as f:
                     try:  
                            subprocess.check_call(["python", "test.py"], stdout=f, stderr=f)
                     except CalledProcessError as e:
                            output = e.output
       
       display_output() 
    
    
         
    

def get_code(event):
   if event.keysym == 'Return':   
    Code=inputTextArea.get(0.0, END)
   
    fout=open("test.py", 'w')
    
    fout.write(Code)
    
    
    fout.close()
    if 'input' in Code:
      with open("output.txt", "w") as f:
        try:
                    
               py_compile.compile("test.py", '', '', True)
        except OSError as e:
                finput()
          except py_compile.PyCompileError as e:
                with open("output.txt", "w") as f:
                     try:  
                            subprocess.check_call(["python", "test.py"], stdout=f, stderr=f)
                     except CalledProcessError as e:
                            output = e.output
       
                display_output()            
               
                   
      
          
           
      
    else:   
       
       with open("output.txt", "w") as f:
           try:  
             subprocess.check_call(["python", "test.py"], stdout=f, stderr=f)
           except CalledProcessError as e:
             output = e.output
       
       display_output()        

def display_output():
   
    fin=open("output.txt")
    e=fin.readlines()
    
    j="".join(e)
    
    outputContents.set("")
    outputContents.set(j)    
    print(outputContents.get())    
 


inputTextArea.bind('<Return>',get_code) 
inputTextArea1.bind('<Return>',get_input) 
        
 #Creating a button
displayButton1 = tkinter.Button(GUIwindow, text="Write your code here!", bg="snow4", fg="Black") 
# #Placing the button appropriately
displayButton1.grid(column=1, row=1)      
# #Creating a button
displayButton2 = tkinter.Button(GUIwindow, text="See the output here!", bg="snow4", fg="Black") 
# #Placing the button appropriately
displayButton2.grid(column=4, row=1)      

displayButton3 = tkinter.Button(GUIwindow, text="Insert the input here!", bg="snow4", fg="Black") 
# #Placing the button appropriately
displayButton3.grid(column=4, row=3)     







tk.mainloop()

