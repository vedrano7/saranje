import tkinter as tk
from tkinter import *
from tkinter import colorchooser
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

#glavni prozor, varijable i inicijalizacija vrijednosti

root = Tk()
root.title("Šaranje")
root.geometry("751x600")

root.iconphoto(True, PhotoImage(file='icon.gif'))

stroke_size = IntVar()
stroke_size.set(1)

stroke_color = StringVar()
stroke_color.set("black")

prevColor = StringVar()
prevColor.set("white")

prev2Color = StringVar()
prev2Color.set("white")

prevPoint = [0,0]
currentPoint = [0,0] 

textValue = StringVar()

options = [1,2,3,4,5,10]

#funkcije

def usePencil():
    stroke_color.set("black")
    canvas["cursor"] = "pencil"

def useEraser():
    stroke_color.set("white")
    canvas["cursor"] = DOTBOX

def selectColor():
    selectedColor = colorchooser.askcolor("blue" , title="Spektar boja")
    if selectedColor[1] != None :
        prev2Color.set(prevColor.get())
        prevColor.set(stroke_color.get())
        
        prevColorButton["bg"] = prevColor.get()
        prev2ColorButton["bg"] = prev2Color.get()
        
        stroke_color.set(selectedColor[1])
        
def changeColors(new_color):
    if new_color!=stroke_color.get():
        if new_color!=prevColor.get():
            prev2Color.set(prevColor.get())
            prevColor.set(stroke_color.get())
            
            prevColorButton["bg"] = prevColor.get()
            prev2ColorButton["bg"] = prev2Color.get()
                
        elif new_color==prevColor.get():
            prev2Color.set(prev2Color.get())
            prevColor.set(stroke_color.get())


            prevColorButton["bg"] = prevColor.get()
            prev2ColorButton["bg"] = prev2Color.get()
            
        stroke_color.set(new_color)
        
def paint(event):
    global prevPoint
    global currentPoint
    x = event.x
    y = event.y
    currentPoint = [x,y]

    if prevPoint != [0,0] : 
        canvas.create_polygon(prevPoint[0] , prevPoint[1] , currentPoint[0] , currentPoint[1],fill=stroke_color.get() , outline=stroke_color.get() , width=stroke_size.get())        

    prevPoint = currentPoint

    if event.type == "5" :
        prevPoint = [0,0]

def paintRightClick(event):
    x = event.x
    y = event.y
    canvas.create_arc(x,y,x+stroke_size.get() , y+stroke_size.get() , fill=stroke_color.get() , outline=stroke_color.get() , width=stroke_size.get())
    
def saveImage():
    try:
        fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
        x = lowerFrame.winfo_rootx()
        y = lowerFrame.winfo_rooty()
        img = ImageGrab.grab(bbox=(x+81,y+94,x+1150,y+819))
        img.save(fileLocation)
        showImage = messagebox.askyesno("Šaranje" , "Želite li odmah otvoriti sliku?")
        if showImage:
           img.show()

    except Exception as e:
        messagebox.showinfo("Greška" , "Neuspjelo spremanje slike")
       
def clearCanvas():
    if messagebox.askokcancel("Šaranje" , "Želite li očistiti platno?"):
        canvas.delete('all')

def loadImage():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.gif;*.bmp")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((1100, 500), Image.ANTIALIAS) if hasattr(Image, 'ANTIALIAS') else img
            canvas.delete('all')
            canvas.image = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)
            
    except Exception as e:
        messagebox.showinfo("Greška" , "Neuspjelo učitavanje slike")

def help():
    helpText = "1. Ako držiš desni klik pri crtanju dobit ćeš iscrtkanu crtu \n2.Ako stisneš gumb za listanje na mišu zalijepit ćeš tekst koji si napisao u kvadratiću za tekst"
    messagebox.showinfo("Savjeti: " , helpText)

def about():
    messagebox.showinfo("O programu" , "najjači oop projekt")

def pasteText(event):
    canvas.create_text(event.x , event.y , text=textValue.get())
    
#GUI

    #gornji okvir

upperFrame = Frame(root , height=100 , width=1100 )
upperFrame.grid(row=0 , column=0, sticky=NW)

        #okvir za pribor

toolsFrame = Frame(upperFrame , height=100 , width=100, relief=SUNKEN , borderwidth=3)
toolsFrame.grid(row=0 , column=0 )

pencilButton = Button(toolsFrame , text="Olovka" , width=10 , command=usePencil)
pencilButton.grid(row=0 , column=0)
eraserButton = Button(toolsFrame , text="Gumica" , width=10 , command=useEraser)
eraserButton.grid(row=1 , column=0)

        #okvir za debljinu pribora

sizeFrame = Frame(upperFrame , height=100 , width=100, relief=SUNKEN , borderwidth=3 )
sizeFrame.grid(row=0 , column=1 )

sizeLabel = Label(sizeFrame , text="Debljina", width=10)
sizeLabel.grid(row=0 , column=0)
sizeList = OptionMenu(sizeFrame , stroke_size , *options)
sizeList.grid(row=1 , column=0)

        #okvir za spektar boja i proslu i pretproslu boju

colorSpectrumFrame = Frame(upperFrame , height=100 , width=100 ,relief=SUNKEN , borderwidth=3 )
colorSpectrumFrame.grid(row = 0 , column=2)

colorSpectrumButton = Button(colorSpectrumFrame , text="Spektar boja" , width=10 , command=selectColor)
colorSpectrumButton.grid(row=0 , column=0)

prevColorButton = Button(colorSpectrumFrame , text="Prošla" , width=10 , command=lambda:changeColors(prevColor.get()))
prevColorButton.grid(row=1 , column=0)
prev2ColorButton = Button(colorSpectrumFrame , text="Pretprošla" , width=10 , command=lambda:changeColors(prev2Color.get()))
prev2ColorButton.grid(row=2 , column=0)

        #okvir za brz odabir boja

colorsFrame = Frame(upperFrame, height=100 , width=100, relief=SUNKEN , borderwidth=3)
colorsFrame.grid(row = 0 , column=3)

redButton = Button(colorsFrame, bg="red", width=10, command=lambda: changeColors("red"))
redButton.grid(row=0, column=0)
greenButton = Button(colorsFrame, bg="green", width=10, command=lambda: changeColors("green"))
greenButton.grid(row=1, column=0)
blueButton = Button(colorsFrame, bg="blue", width=10, command=lambda: changeColors("blue"))
blueButton.grid(row=2, column=0)
yellowButton = Button(colorsFrame, bg="yellow", width=10, command=lambda: changeColors("yellow"))
yellowButton.grid(row=0, column=1)
orangeButton = Button(colorsFrame, bg="orange", width=10, command=lambda: changeColors("orange"))
orangeButton.grid(row=1, column=1)
blackButton = Button(colorsFrame, bg="black", width=10, command=lambda: changeColors("black"))
blackButton.grid(row=2, column=1)

        #okvir za opcije upravljanja slikama/platnom

imageAndCanvasOptionsFrame = Frame(upperFrame, height=100 , width=100, relief=SUNKEN , borderwidth=3)
imageAndCanvasOptionsFrame.grid(row = 0 , column=4)

saveImageButton = Button(imageAndCanvasOptionsFrame , text="Spremi" , bg="white" , width=10 , command=saveImage)
saveImageButton.grid(row=0 , column=0)

loadImageButton = Button(imageAndCanvasOptionsFrame , text="Učitaj" , bg="white" , width=10 , command=loadImage)
loadImageButton.grid(row=1 , column=0)

clearCanvasButton = Button(imageAndCanvasOptionsFrame , text="Očisti platno" , bg="white" , width=10 , command=clearCanvas)
clearCanvasButton.grid(row=2 , column=0)

        #okvir za tekst

textFrame = Frame(upperFrame, height=100 , width=200, relief=SUNKEN , borderwidth=3)
textFrame.grid(row = 0 , column=5)

textTitleButton = Label(textFrame , text="Kvadratić za tekst:" , bg="white" , width=20 )
textTitleButton.grid(row=0 , column=0)
entryButton = Entry(textFrame, textvariable=textValue, bg="white" , width=20 )
entryButton.grid(row=1 , column=0)
clearButton = Button(textFrame , text="Izbriši tekst" , bg="white" , width=20 , command=lambda:textValue.set(""))
clearButton.grid(row=2 , column=0)

        #okvir za dodatne opcije

additionalOptionsFrame = Frame(upperFrame, height=100 , width=100, relief=SUNKEN , borderwidth=3)
additionalOptionsFrame.grid(row = 0 , column=6)

helpButton = Button(additionalOptionsFrame , text="Pomoć" , bg="white" , width=10 , command=help)
helpButton.grid(row=0 , column=0)
aboutButton = Button(additionalOptionsFrame , text="O programu" , bg="white" , width=10 , command=about)
aboutButton.grid(row=2 , column=0)

    #donji okvir

lowerFrame = Frame(root , height=500 , width=1100)
lowerFrame.grid(row=1 , column=0)

canvas = Canvas(lowerFrame , height=500 , width=1100 , bg="white" )
canvas.grid(row=0 , column=0)

canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)
canvas.bind("<B3-Motion>" , paintRightClick)
canvas.bind("<Button-2>", pasteText)

root.resizable(False , False)
root.mainloop()
