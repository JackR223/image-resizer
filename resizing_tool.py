import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import img_resizer


source_dir = ""
target_dir = ""
target_size = 250


window = tk.Tk()
window.geometry("500x250")


def UploadAction(s_t):
    directory = filedialog.askdirectory()
    if s_t == 0:
        global source_dir
        source_dir = directory
        button_source_dir.configure(text=source_dir)
    else:
        global target_dir
        target_dir = directory
        button_target_dir.configure(text=target_dir)


def Run(size):

    if source_dir == "" or target_dir == "":
        messagebox.showerror('Python Error', 'Error: Invalid source or target directory!')
    else:
        global target_size
        target_size = size

        print("Source dir = " + source_dir)
        print("Target dir = " + target_dir)
        print("Target size = " + str(target_size))
        
        button_go.place(relx=0.45, rely=1.2)
        pb.place(relx=0.22, rely=0.8)
        pb.start()

        img_resizer.compress(source_dir, target_dir, target_size)

        pb.stop()

        messagebox.showinfo('Done', 'All files in target directory processed!')

        window.destroy()


l1 = tk.Label(window, text="Source directory: ")
button_source_dir = tk.Button(window, text='Open', width=55, command=lambda: UploadAction(0))

l2 = tk.Label(window, text="Target directory: ")

button_target_dir = tk.Button(window, text='Open', width=55, command=lambda: UploadAction(1))

l3 = tk.Label(window, text="File size (kb): ")

size = tk.Scale(window, from_=1, to=1000, length=390, orient='horizontal')
size.set(250)

global button_go
button_go = tk.Button(window, text='compress', background='greenyellow', command=lambda: Run(size.get()))

global pb
pb = ttk.Progressbar(window, orient='horizontal', mode='indeterminate', length=280)



l1.place(relx=0, rely=0)
#l1.pack()
button_source_dir.place(relx=0.2, rely=0)

l2.place(relx=0, rely=0.2)
button_target_dir.place(relx=0.2, rely=0.2)

l3.place(relx=0, rely=0.4)
size.place(relx=0.2, rely=0.33)

button_go.place(relx=0.45, rely=0.8)

pb.place(relx=0.22, rely=1.2)

window.mainloop()