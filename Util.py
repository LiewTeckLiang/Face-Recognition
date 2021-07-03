from __future__ import print_function

import datetime
import os
import threading
import tkinter as tki

import cv2
import imutils
from PIL import Image
from PIL import ImageTk

import pickle


class Util:
    def __init__(self, vs):
       
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
        self.path = None
        self.outputPath = None

        WIDTH = 250
        HEIGHT = 300

        canvas = tki.Canvas(self.root, height=HEIGHT, width=WIDTH)
        canvas.pack()

        e = tki.Entry(self.root)
        e.place(relx=0.25, rely=0.3, relwidth=0.5)

        btn = tki.Button(self.root, text="Snapshot!",
                         command=lambda: self.takeSnapshot(e))
        btn.place(relx=0.25, rely=0.2)

        myButton2 = tki.Button(self.root, text='Change directory.',
                               command=self.change_path)
        myButton2.place(relx=0.25, rely=0.1)

        btn3 = tki.Button(self.root, text="Close", command=canvas.delete('all')).pack()
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        
        self.root.wm_title("New Registration")
       

    def videoLoop(self):
        try:
            
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=500)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                
                # Initialize the panel
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.place(relx=0.05, rely=0.3, relwidth=0.9)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError as e:
            print("Caught a RuntimeError")

    def takeSnapshot(self, e):

        if len(e.get()) == 0:
            self.pop_up()

        else:
           
            ts = datetime.datetime.now()

            filename = e.get() + ".jpg"
            if os.path.getsize("save.p") == 0:
                #If first time put output directory
                self.outputPath = self.outputpath()

            else:
       
                self.path = pickle.load(open("save.p", "rb"))
                self.outputPath = self.path

            p = os.path.sep.join((self.outputPath, filename))

            # save file
            cv2.imwrite(p, self.frame.copy())

            print("Saved as {}".format(filename), "at following directory: " + self.path)

    def onClose(self):
      
        print("Closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

    def outputpath(self):
        if self.path is None:
            self.path = tki.filedialog.askdirectory(title='Select output file.')

        else:
            pickle.dump(self.path, open("save.p", "wb"))

        return self.path

    def pop_up(self):
        pop = tki.Toplevel(self.root)
        pop.title("Error Message")
        pop.geometry("300x100")
        pop.config(bg='blue')

        pop_label = tki.Label(pop, text='Empty Output Directory!')
        pop_label.place(relx=0.1, rely=0.4, relwidth=0.8)

    def change_path(self):
        self.path = tki.filedialog.askdirectory(title='Select output file.')
        pickle.dump(self.path, open("save.p", "wb"))

