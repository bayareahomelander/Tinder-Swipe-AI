from os import listdir, rename
from os.path import isfile, join
from PIL import ImageTk, Image
import tkinter as tk

imageFolder = '/Users/paco/Downloads/unclassified/'
images = [f for f in listdir(imageFolder) if isfile(join(imageFolder, f))]
unclassifiedImages = filter(lambda image: not (image.startswith('0_') or image.startswith('1_')), images)
current = None

def next_img():
    global current, unclassifiedImages
    try:
        current = next(unclassifiedImages)
    except StopIteration:
        root.quit()
    print(current)
    pilImg = Image.open(imageFolder + '/' + current)
    width, height = pilImg.size
    maxHeight = 1000

    if height > maxHeight:
        resizeFactor = maxHeight / height
        pilImg = pilImg.resize((int(width * resizeFactor), int(height * resizeFactor)), resample = Image.LANCZOS)
    
    imgTk = ImageTk.PhotoImage(pilImg)
    img_label.img = imgTk
    img_label.config(image = img_label.img)

def positive(param):
    global current
    rename(imageFolder + '/' + current, imageFolder + '/1_' + current)
    next_img()

def negative(param):
    global current
    rename(imageFolder + '/' + current, imageFolder + '/0_' + current)
    next_img()

if __name__ == "__main__":

    root = tk.Tk()

    img_label = tk.Label(root)
    img_label.pack()
    img_label.bind("<Button-1>", positive)
    img_label.bind("<Button-2>", negative)

    btn = tk.Button(root, text='Next Image', command=next_img)

    next_img()

    root.mainloop()