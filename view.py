import tkinter as tk
import glob
from PIL import Image
import os
from tkinter import messagebox, font

info = '''
welcome to your sleeping children automatic overseer .
where you can see which children woke up in the night,
in what times and images of them - in three frames.
this in order to identify and solve sleeping disorder 
from young age.
'''


help = '''
choose image to see it .
images order by bed number,
wake up order by abc and three frames
to each wake up time.
'''


def update_list():
    lst.delete(0, tk.END)
    search_term = search_var.get()
    path = 'images'
    files = os.listdir(path)
    for filename in files:
        if 'png' in filename and filename != 'Image-processing.png':
            if search_term.lower() in filename.lower():
                lst.insert(tk.END, filename.split(".")[0])


def showimg(event):
    n = lst.curselection()
    filename = 'images\\' + lst.get(n) + ".png"
    img = tk.PhotoImage(file=filename)
    w, h = img.width(), img.height()
    canvas.image = img
    canvas.config(width=w, height=h)
    canvas.delete("all")
    canvas.create_image(0, 50, image=img, anchor=tk.NW)
    lines = open("results.txt").readlines()
    for index, line in enumerate(lines):
        num = filename.index("-") - 1
        if "bedNumber: " + filename[num] in line:
            time = lines[index - 1].replace('t', 'T', 1).strip()
            number = lines[index].replace('b', 'B', 1).strip()

    canvas.create_text(300, 30, text=number + " " + time, fill=
    "black", font=('Helvetica 15 bold'))


def make_images_png():
    path = 'images'
    files = os.listdir(path)
    for filename in files:
        im1 = Image.open('images\\' + filename)
        path_no_ext = filename.split('.')
        path_no_ext[-1] = ".png"
        new_path = ''.join(path_no_ext)
        im1.save('images\\' + new_path)


def resize_images(width, height):
    path = 'images'
    files = os.listdir(path)
    for filename in files:
        image = Image.open('images\\' + filename)
        image = image.resize((width, height), Image.ANTIALIAS)
        image.save(fp='images\\' + filename)


def next_selection():
    selection_indices = lst.curselection()

    # default next selection is the beginning
    next_selection = 0

    # make sure at least one item is selected
    if len(selection_indices) > 0:
        # Get the last selection, remember they are strings for some reason
        # so convert to int
        last_selection = int(selection_indices[-1])

        # clear current selections
        lst.selection_clear(selection_indices)

        # Make sure we're not at the last item
        if last_selection < lst.size() - 1:
            next_selection = last_selection + 1

    lst.activate(next_selection)
    lst.selection_set(next_selection)
    showimg(root)


def prev_selection():
    selection_indices = lst.curselection()

    # default next selection is the beginning
    next_selection = lst.size() - 1

    # make sure at least one item is selected
    if len(selection_indices) > 0:
        # Get the last selection, remember they are strings for some reason
        # so convert to int
        last_selection = int(selection_indices[-1])

        # clear current selections
        lst.selection_clear(selection_indices)

        # Make sure we're not at the last item
        if last_selection > 0:
            next_selection = last_selection - 1

    lst.activate(next_selection)
    lst.selection_set(next_selection)
    showimg(root)


def help_msg():
    tk.messagebox.showinfo("help message", help)


###############  main  ############

# set window
root = tk.Tk()
root.geometry("800x600+300+50")
root.title("see wake up images")

# change images to fit
make_images_png()
resize_images(600, 600)

# make filter for list box
search_var = tk.StringVar(root)
search_var.trace("w", lambda name, index, mode: update_list())
entry = tk.Entry(root, textvariable=search_var, width=13)
entry.pack()

# make label for search
lb = tk.Label(text="search for images here:", font='Aerial 13 bold')
lb.place(in_=entry, relx=-2.5, anchor="nw", bordermode="outside", y=-2)

# make list box
lst = tk.Listbox(root, width=20)
lst.pack(side="left", fill=tk.BOTH, expand=0)
lst.bind("<<ListboxSelect>>", showimg)
lst.configure(background="skyblue4", foreground="white", font='Aerial 13')
update_list()

# make next button
btn_next = tk.Button(root, text='next', bd='5',
                     command=next_selection, width=15, background='red', font='bold')
btn_next.place(x=0, y=400)

# make prev button
btn_prev = tk.Button(root, text='prev', bd='5',
                     command=prev_selection, width=15, background='red', font='bold')
btn_prev.place(x=0, y=450)

# make help button
btn_help = tk.Button(root, text='help', bd='5',
                     command=help_msg, width=15, background='red', font='bold')
btn_help.place(x=0, y=500)

# make canvas and add image
canvas = tk.Canvas(root)
img = tk.PhotoImage(file='images\\' + "Image-processing.png")
w, h = img.width(), img.height()
canvas.image = img
canvas.config(width=w, height=h)
canvas.create_image(0, 0, image=img, anchor=tk.NW)

# add welcome message with details
canvas.create_text(280, 70, text=info, fill=
"black", font=('Helvetica 16 bold'))
canvas.pack()

root.mainloop()
