from tkinter import *
from tkinter import colorchooser
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image

root = Tk()
root.title("Šaranje")
root.geometry("1020x800")

# Convert ICO to GIF
ico_path = 'paintingIcon.ico'
img = Image.open(ico_path)
img.save('icon.gif', 'gif')

# Set the GIF as an icon
root.iconphoto(True, PhotoImage(file='icon.gif'))

# -------------- variables --------------------

# stroke size options 
options = [1,2,3,4,5,10]

stroke_size = IntVar()
stroke_size.set(1)

stroke_color = StringVar()
stroke_color.set("black")

previousColor = StringVar()
previousColor.set("white")

previousColor2 = StringVar()
previousColor2.set("white")

# variables for pencil 
prevPoint = [0,0]
currentPoint = [0,0] 

# variable for text
textValue = StringVar()

# --------------------- functions -------------------------

def usePencil():
    stroke_color.set("black")
    canvas["cursor"] = "pencil"

def useEraser():
    stroke_color.set("white")
    canvas["cursor"] = DOTBOX

def selectColor():
    selectedColor = colorchooser.askcolor("blue" , title="Spektar boja")
    if selectedColor[1] == None :
        stroke_color.set("black")
    else:
        stroke_color.set(selectedColor[1])
        previousColor2.set(previousColor.get())
        previousColor.set(selectedColor[1])

        previousColorButton["bg"] = previousColor.get()
        previousColor2Button["bg"] = previousColor2.get()

def paint(event):
    global prevPoint
    global currentPoint
    x = event.x
    y = event.y
    currentPoint = [x,y]
    # canvas.create_oval(x , y , x +5 , y + 5 , fill="black")

    if prevPoint != [0,0] : 
        canvas.create_polygon(prevPoint[0] , prevPoint[1] , currentPoint[0] , currentPoint[1],fill=stroke_color.get() , outline=stroke_color.get() , width=stroke_size.get())        

    prevPoint = currentPoint

    if event.type == "5" :
        prevPoint = [0,0]

def paintRight(event):
    x = event.x
    y = event.y
    canvas.create_arc(x,y,x+stroke_size.get() , y+stroke_size.get() , fill=stroke_color.get() , outline=stroke_color.get() , width=stroke_size.get())
    

def saveImage():
    
    fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
    x = root.winfo_rootx()
    y = root.winfo_rooty()+100
    img = ImageGrab.grab(bbox=(x,y,x+1020,y+700))
    img.save(fileLocation)
    showImage = messagebox.askyesno("Šaranje" , "Želite li odmah otvoriti sliku?")
    if showImage:
       img.show()
       
def clear():
    if messagebox.askokcancel("Šaranje" , "Želite li očistiti platno?"):
        canvas.delete('all')

def createNew():
    if messagebox.askyesno("Šaranje" , "Želite li spremiti sliku prije nego što očistite platno?"):
        saveImage()
    clear()

def help():
    helpText = "1. Ako držiš desni klik pri crtanju dobit ćeš iscrtkanu crtu \n2.Ako stisneš gumb za listanje na mišu zalijepit ćeš tekst koji si napisao u desnom gornjem kutu"
    messagebox.showinfo("Savjeti" , helpText)

def about():
    messagebox.showinfo("O programu" , "Najjači projekt za oop")

def writeText(event):
    canvas.create_text(event.x , event.y , text=textValue.get())
# ------------------- User Interface -------------------

# Frame - 1 : Tools 

frame1 = Frame(root , height=100 , width=1100 )
frame1.grid(row=0 , column=0, sticky=NW)

# toolsFrame 

toolsFrame = Frame(frame1 , height=100 , width=100, relief=SUNKEN , borderwidth=3)
toolsFrame.grid(row=0 , column=0 )

pencilButton = Button(toolsFrame , text="Olovka" , width=10 , command=usePencil)
pencilButton.grid(row=0 , column=0)
eraserButton = Button(toolsFrame , text="Gumica" , width=10 , command=useEraser)
eraserButton.grid(row=1 , column=0)

# sizeFrame 

sizeFrame = Frame(frame1 , height=100 , width=100, relief=SUNKEN , borderwidth=3 )
sizeFrame.grid(row=0 , column=1 )

sizeLabel = Label(sizeFrame , text="Debljina", width=10)
sizeLabel.grid(row=0 , column=0)
sizeList = OptionMenu(sizeFrame , stroke_size , *options)
sizeList.grid(row=1 , column=0)


# colorBoxFrame

colorBoxFrame = Frame(frame1 , height=100 , width=100 ,relief=SUNKEN , borderwidth=3 )
colorBoxFrame.grid(row = 0 , column=2)

colorBoxButton = Button(colorBoxFrame , text="Spektar boja" , width=10 , command=selectColor)
colorBoxButton.grid(row=0 , column=0)
previousColorButton = Button(colorBoxFrame , text="Prošla" , width=10 , command=lambda:stroke_color.set(previousColor.get()))
previousColorButton.grid(row=1 , column=0)
previousColor2Button = Button(colorBoxFrame , text="Pretprošla" , width=10 , command=lambda:stroke_color.set(previousColor2.get()))
previousColor2Button.grid(row=2 , column=0)

# colorsFrame

colorsFrame = Frame(frame1, height=100 , width=100, relief=SUNKEN , borderwidth=3)
colorsFrame.grid(row = 0 , column=3)

redButton = Button(colorsFrame , bg="red" , width=10 , command=lambda: stroke_color.set("red"))
redButton.grid(row=0 , column=0)
greenButton = Button(colorsFrame , bg="green" , width=10 , command=lambda: stroke_color.set("green"))
greenButton.grid(row=1 , column=0)
blueButton = Button(colorsFrame , bg="blue" , width=10 , command=lambda: stroke_color.set("blue"))
blueButton.grid(row=2 , column=0)
yellowButton = Button(colorsFrame , bg="yellow" , width=10 , command=lambda: stroke_color.set("yellow"))
yellowButton.grid(row=0 , column=1)
orangeButton = Button(colorsFrame ,  bg="orange" , width=10 , command=lambda: stroke_color.set("orange"))
orangeButton.grid(row=1 , column=1)
purpleButton = Button(colorsFrame , bg="purple" , width=10 , command=lambda: stroke_color.set("purple"))
purpleButton.grid(row=2 , column=1)

# saveImageFrame

saveImageFrame = Frame(frame1, height=100 , width=100, relief=SUNKEN , borderwidth=3)
saveImageFrame.grid(row = 0 , column=4)

saveImageButton = Button(saveImageFrame , text="Spremi" , bg="white" , width=10 , command=saveImage)
saveImageButton.grid(row=0 , column=0)
newImageButton = Button(saveImageFrame , text="New" , bg="white" , width=10 , command=createNew)
newImageButton.grid(row=1 , column=0)
clearImageButton = Button(saveImageFrame , text="Očisti platno" , bg="white" , width=10 , command=clear)
clearImageButton.grid(row=2 , column=0)

# helpSettingFrame

helpSettingFrame = Frame(frame1, height=100 , width=100, relief=SUNKEN , borderwidth=3)
helpSettingFrame.grid(row = 0 , column=5)

helpButton = Button(helpSettingFrame , text="Pomoć" , bg="white" , width=10 , command=help)
helpButton.grid(row=0 , column=0)
aboutButton = Button(helpSettingFrame , text="O programu" , bg="white" , width=10 , command=about)
aboutButton.grid(row=2 , column=0)

# textFrame

textFrame = Frame(frame1, height=100 , width=200, relief=SUNKEN , borderwidth=3)
textFrame.grid(row = 0 , column=6)

textTitleButton = Label(textFrame , text="Kvadratić za tekst:" , bg="white" , width=20 )
textTitleButton.grid(row=0 , column=0)
entryButton = Entry(textFrame, textvariable=textValue, bg="white" , width=20 )
entryButton.grid(row=1 , column=0)
clearButton = Button(textFrame , text="Izbriši tekst" , bg="white" , width=20 , command=lambda:textValue.set(""))
clearButton.grid(row=2 , column=0)

# noteFrame

noteFrame = Frame(frame1, height=100 , width=200, relief=SUNKEN , borderwidth=3)
noteFrame.grid(row = 0 , column=7)

textTitleButton = Text(noteFrame, bg="white" , width=40 , height=4 )
textTitleButton.grid(row=0 , column=0)

# Frame - 2 - Canvas

frame2 = Frame(root , height=640 , width=1020 , bg="yellow")
frame2.grid(row=1 , column=0)

canvas = Canvas(frame2 , height=640 , width=1020 , bg="white" )
canvas.grid(row=0 , column=0)

canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)
canvas.bind("<B3-Motion>" , paintRight)
canvas.bind("<Button-2>", writeText)

root.resizable(False , False)
root.mainloop()
