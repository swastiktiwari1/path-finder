##################################################################################
# Sudeep Gumaste                                                                 #
# Suvrojyoti Mandal                                                              #
# Swastik Tiwari                                                                 #
# Sweekar Burji                                                                  #
##################################################################################
import cv2
import time
import numpy as np
import threading
import colorsys
from tkinter.filedialog import askopenfilename
from tkinter import *
import tkinter.messagebox

rw=2
p=0
maze=''

class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


start = Point()
end = Point()

dir4=[Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]
def mouse_event(event, pX, pY, flags, param):
    global img, p, start, end

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            start= Point(pX,pY)
            cv2.rectangle(img, (pX-rw,pY-rw), (pX+rw,pY+rw),(0,0,255),-1)
            print("start =", start.x, start.y)
            p+=1
        
        elif p == 1:
            end= Point(pX,pY)
            cv2.rectangle(img, (pX-rw,pY-rw), (pX+rw,pY+rw),(0,250,50),-1)
            print("end =", end.x, end.y)
            p+=1

def disp():
    global img,h,w
    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",mouse_event)
    while True:
        cv2.imshow("Image",img)
        cv2.waitKey(1)

def BFS(s, e):
    global img,h,w
    const=3000
    cell=Point()
    found = False
    q = []
    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    q.append(s)
    v[s.y][s.x] = 1

    while(len(q)>0):
        p=q.pop(0)
        for d in dir4:
            cell = p + d
            if(cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and (img[cell.y][cell.x][0]!= 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] !=0)):
                q.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1

                img[cell.y][cell.x] = list(reversed ([ i*255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x]/const, 1, 1)]))

                parent[cell.y][cell.x] = p

                if cell == e:
                    found = True
                    del q[:]
                    break


    path = []

    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()

        for p in path:
            img[p.y][p.x] = [255,255,255]
        for p in path:
            cv2.rectangle(img, (p.x-rw,p.y-rw), (p.x+rw,p.y+rw),(255,0,0),1)
            img[p.y][p.x] = [0, 0, 255]
            time.sleep(0.01)
            #img[p.y][p.x] = [255, 255, 255]
        tkinter.messagebox.showinfo('Path','Path Found!')
        print("Path found")

    else:
        tkinter.messagebox.showinfo('Path','Path not found')
        print("Path not found")



def main():
    global img,h,w,maze
    if maze=='':
        print("No image chosen")
        tkinter.messagebox.showerror('Error!','Please choose an image file first')
    else:
        try:
            img = cv2.imread(maze, cv2.IMREAD_GRAYSCALE)

            _, img= cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
            

            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            h, w = img.shape[:2]

            print("Select Start point and end point")

            #disp()

            t = threading.Thread(target=disp, args=())
            t.daemon=True
            t.start()

            while p<2:
                pass

            BFS(start,end)
            cv2.waitKey(1)
        except:
            tkinter.messagebox.showerror('Error!','Please select only image files')

def quit():
    ans=tkinter.messagebox.askquestion('confirmation',"Do you want to quit?")
    if(ans=='yes'):
        exit()

def browse():
    global p,maze
    p=0
    window.filename = filedialog.askopenfilename(initialdir = "/",title = "Select Maze image file",filetypes = (("Image files", "*.jpeg;*.jpg;*.png;*.bmp"),("All files", "*")))
    maze=window.filename

#GUI component
window=Tk()
window.configure(backgroun='#2e2323')
#main heder
label1=Label(window,text="      Path Finder",font="Times 28 bold",bg='#2e2323',fg='white')
label1.grid(row=0,sticky=N,columnspan=(4))
label1=Label(window,text=" ",font="Times 28 bold",bg='#2e2323',fg='white')
label1.grid(row=1,sticky=N,columnspan=(3))
#text display 
label2=Label(window,text="\tChoose the maze: ",font="Times 12 bold",bg='#2e2323',fg='white')
label2.grid(row=3)
#select the maze
path=Label(window,text="Plese select a file    ",bg='#2e2323',fg='white')
path.grid(row=3,column=1)
#window name and geometry
window.title("Path finder")
#browse action
butBrowse=Button(window, text="Browse",font="Times 12 bold",command=browse,bg='#462b2b',fg='white')
butBrowse.grid(row=3, column=2)
label2=Label(window,text="\t",font="Times 12 bold",bg='#2e2323',fg='white')
label2.grid(row=3,column=4)
#run button
label1=Label(window,text=" ",font="Times 28 bold",bg='#2e2323',fg='white')
label1.grid(row=4,sticky=N,columnspan=(3))
butRun=Button(window, text="Run",font="Times 12 bold",command=main,bg='#462b2b',fg='white')
butRun.grid(row=5,column=0)
#quit
exitButton=Button(window,text="Exit",font="Times 12 bold",command=quit,bg='#462b2b',fg='white')
exitButton.grid(row=5, column=2)

label1=Label(window,text=" ",font="Times 28 bold",bg='#2e2323',fg='white')
label1.grid(row=6,sticky=N,columnspan=(3))
window.mainloop()
