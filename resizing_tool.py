import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import multiprocessing
import img_resizer

if __name__ == '__main__':

    multiprocessing.freeze_support()

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
            
            #button_go.place(relx=0.45, rely=1.2)
            #pb.place(relx=0.22, rely=0.8)
            
            #pb.start()

            sub_arr1, sub_arr2, sub_arr3, sub_arr4 = img_resizer.split(source_dir)
            

            # start processes:
            pipe1_1, pipe1_2 = multiprocessing.Pipe()
            pipe2_1, pipe2_2 = multiprocessing.Pipe()
            pipe3_1, pipe3_2 = multiprocessing.Pipe()
            pipe4_1, pipe4_2 = multiprocessing.Pipe()

            p1 = multiprocessing.Process(target=img_resizer.compress, args=(sub_arr1, source_dir, target_dir, target_size, pipe1_2,))
            p2 = multiprocessing.Process(target=img_resizer.compress, args=(sub_arr2, source_dir, target_dir, target_size, pipe2_2,))
            p3 = multiprocessing.Process(target=img_resizer.compress, args=(sub_arr3, source_dir, target_dir, target_size, pipe3_2,))
            p4 = multiprocessing.Process(target=img_resizer.compress, args=(sub_arr4, source_dir, target_dir, target_size, pipe4_2,))

            p1.start()
            p2.start()
            p3.start()
            p4.start()

            # wait for processes to finish
            pipe1_1.recv()
            pipe2_1.recv()
            pipe3_1.recv()
            pipe4_1.recv()


            #pb.stop()

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
    button_go = tk.Button(window, text='resize', background='greenyellow', command=lambda: Run(size.get()))

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