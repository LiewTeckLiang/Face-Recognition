from tkinter import *
from Backend import main
from Util2 import new_register
from tkinter import filedialog
from PIL import ImageTk, Image

WIDTH = 500
HEIGHT = 600

root = Tk()


# To hide the 'Register New User' button after clicked.
def multi():
    RegisterButton['state'] = DISABLED
    new_register()


canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = ImageTk.PhotoImage(file="background.jpg")
background_label = Label(root, image=background_image).place(x=0, y=0, relwidth=1, relheight=1)


StartButton = Button(root, text='Start', command=main)
StartButton.place(relx=0.45, rely=0.1)

RegisterButton = Button(root, text='Register New User', command=multi)
RegisterButton.place(relx=0.35, rely=0.15)


root.wm_title("Register")
root.config(background="#FFFFFF")

root.mainloop()




