import tkinter
from tkinter import *
from google_images_download import google_images_download
from PIL import ImageTk, Image, ImageDraw, ImageFont
import random
import time
from tkinter.ttk import Progressbar
from tkinter import ttk
from instapy_cli import client
import os

def bar():
    progress = Progressbar(window, orient = HORIZONTAL, length = 300, mode = 'determinate')
    progress.place(relx=0.5, rely=0.07, anchor=CENTER)
    progress['value'] = 20
    window.update_idletasks()
    time.sleep(.1)

    progress['value'] = 40
    window.update_idletasks()
    time.sleep(.1)

    progress['value'] = 50
    window.update_idletasks()
    time.sleep(.1)

    progress['value'] = 60
    window.update_idletasks()
    time.sleep(.1)

    progress['value'] = 80
    window.update_idletasks()
    time.sleep(.1)
    progress['value'] = 100
    progress.place_forget()
def insta():

    username = 'mem.ebot'
    password = 'memebotv3'
    image = 'meme.png'
    text = 'This meme is a auto generated, this insta will now spam memes. Thanks. plz follow for an infinite amount of random memes.' + \
    '\r\n' + '''#meme #edgy #redditmeme #asiandoge #memebot #lol #python #memes
    #hitler'''

    with client(username, password) as cli:
        cli.upload(image, text)
    bar()
def clicked():

    search_keyword = keywordSelector()
    path =fetchImage(search_keyword)

    toptext, bottomtext = captioned(search_keyword)

    meme = makeMeme(path, toptext,bottomtext)
    meme = meme.save("meme.png")
    ph = PhotoImage(file="meme.png")
    bar()
    lbl = Label(window, image=ph)
    lbl.image = ph
    lbl.place(relx=0.5, rely=.35, anchor=CENTER)
    # Delete now unused Google file.
    if os.path.exists(path):
        os.remove(path)

def clicked_args(k_entry, c_entry):

    search_keyword = k_entry.get()
    caption = c_entry.get()
    if search_keyword.strip(" ") == "":
        search_keyword = keywordSelector()
        path = fetchImage(search_keyword)
    else:
        path =fetchImage(search_keyword)

    if caption.strip(" ") == "":
        toptext, bottomtext = captioned(search_keyword)
    else:
        toptext, bottomtext = captioned_args(search_keyword,caption)

    meme = makeMeme(path, toptext,bottomtext)
    meme = meme.save("meme.png")
    ph = PhotoImage(file="meme.png")
    bar()
    lbl = Label(window, image=ph)
    lbl.image = ph
    lbl.place(relx=0.5, rely=.35, anchor=CENTER)
    # Delete now unused Google file.
    if os.path.exists(path):
        os.remove(path)

def fetchImage(keyword, type_str = ""):
    '''Given a search keyword string, return the image path.'''
    if type(keyword)!= str:
        raise Exception('fetchImage should be passed a string.')

    search_keyword = keyword
    response = google_images_download.googleimagesdownload()
    rand = int(random.uniform(1,50))
    offset= rand
    arguments = {"keywords":search_keyword,"limit":offset,\
    "no_directory":True,"print_urls":True,"size":"medium", "offset":offset}   #creating list of arguments
    if type_str:
        arguments["type"] = type_str
        print("Type: "+type_str)

    paths = ()
    paths = response.download(arguments)

    imgpath = paths[0][search_keyword][0]
    #img = Image.open(imgpath)
    #img = img.resize((400,400))

    #photo =img
    #return photo
    return imgpath

#Select the image from a file of words
def keywordSelector():
    with open(r"3esl.txt") as f:
        keywordList = f.read().splitlines()

    nKeyword = len(keywordList)
    a = int(random.uniform(0,nKeyword))
    return keywordList[a]

#Caption shell chooser
#Symbol to denote caption insert '$'
#Each phrase in the list of phrases must be on its own line-> That's how it uses splitlines
def captionSelector():
    with open(r"PhraseBank.txt") as w:
        captionList = w.read().splitlines()

    nCaption = len(captionList)
    a = int(random.uniform(0,nCaption))
    selectedCaption = str(captionList[a])
    return selectedCaption

def shellAdder(main,insert):
    '''Return the top and bottom text'''
    toptext = ""
    bottomtext = ""

    split_text = main.split("$")

    # Stick insert between entries in split_text
    new = ""

    for i in range(len(split_text) - 1):
        new += split_text[i]
        new += insert
    if len(split_text) > 1: # If we've excluded last string so far:
        new += split_text[-1]
    else: # Length of split_text is only ever 1 if no insert char
        new = main


    fincap = new.split("&")
    if len(fincap) == 2:
        toptext = fincap[0]
        bottomtext = fincap[1]
    else:
        bottomtext = fincap[0]
    return toptext.upper(), bottomtext.upper()

def captioned(keyword):
    ay = captionSelector()
    by = keyword

    return shellAdder(ay,by)

def captioned_args(keyword, caption):
    return shellAdder(caption, keyword)

def makeMeme(path, toptext, bottomtext, overlay = ""):
    '''Given a photo of the Google result, make the meme with the captions.'''
    # Setup new image
    imgsize = (600,460)

    base = Image.open(path).convert('RGBA')
    base = base.resize(imgsize)

    if overlay:
        over = Image.open(overlay).convert('RGBA')
        over = over.resize(imgsize)
        base = Image.alpha_composite(base, over)

    txt = Image.new('RGBA', base.size, (255,255,255,0))
    d = ImageDraw.Draw(txt)
    font = ImageFont.truetype("impact.ttf", 20)

    imgx, imgy = imgsize
    topx, topy = font.getsize(toptext)
    botx, boty = font.getsize(bottomtext)





    if toptext != "":
        # Print toptext outline on Image
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                d.text(( (imgx - topx)/2 + x, 0 + y),toptext,(0,0,0,255),font=font)
        # Print white toptext
        d.text(( (imgx - topx)/2 , 0),toptext,(255,255,255,255),font=font)



    # Print bottomtext outline


    for x in [-1,0,1]:
        for y in [-1,0,1]:
            d.text(( (imgx - botx)/2 + x, int (imgy * 7/8) + y),bottomtext,(0,0,0,255),font=font)
    # Print bottomtext
    d.text(( (imgx - botx)/2 , int(imgy * 7/8) ),bottomtext,(255,255,255,255),font=font)

    final = Image.alpha_composite(base, txt)

    # Return new imagebase
    return final

# Main Code
# Setup

window = tkinter.Tk()

window.title("Welcome to Meme generator")

window.geometry('900x900')
img = Image.open("insta.png")
img = img.resize((900,900))

photo = ImageTk.PhotoImage(img)
bkgrdimg=tkinter.Label(window, image=photo)
bkgrdimg.image = photo
bkgrdimg.place(x=0, y=0, relwidth=1, relheight=1)


# Entry boxes
key_entry = Entry(window)
key_entry.insert(END, 'stalin')
key_entry.place(relx = 0.7, rely = 0.8, anchor = CENTER)
cap_entry = Entry(window)
cap_entry.insert(END, '$&check!')
cap_entry.place(relx = 0.7, rely = 0.85, anchor = CENTER)

# Buttons
rand_btn = Button(window, text="Click Me for Randomized Meme", command=clicked)
rand_btn.place(relx = 0.5, rely = 0.7, anchor = CENTER)

instabtn = Button(window, text="Click Me to upload to insta", background = 'white', foreground = "black", command=insta)

instabtn.place(relx = 0.7, rely = 0.7, anchor = CENTER)

spec_btn = Button(window, text="Click Me for Specified Meme", \
command=(lambda k = key_entry, c = cap_entry:clicked_args(k,c)  ))
spec_btn.place(relx = 0.5, rely = 0.8, anchor = CENTER)



window.mainloop()
