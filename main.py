import os
import sys
from tkinter import *
import border_remover

PAD_X = 15
PAD_Y = 5


def refresh_lb():
    lb.delete(0, END)
    for x in border_remover.get_all_window_names():
        lb.insert(END, x)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def on_remove_border_click():
    border_remover.remove_window_border(lb.get(lb.curselection()))


def on_restore_border_click():
    border_remover.restore_window_border(lb.get(lb.curselection()))


def add_to_ignored_windows(selection):
    print("setting selection as ignored window: " + selection)
    with open(border_remover.get_ignored_windows_file_path(), 'a') as f:
        f.write(selection + '\n')
        f.flush()
        f.close()
        lb.delete(0, END)
        refresh_lb()


def right_click(event):
    print(event.x, event.y)
    index = lb.index("@%s,%s" % (event.x, event.y))
    selection = lb.get(index)
    lb.select_clear(0, END)
    lb.select_set(index)
    if selection:
        m = Menu(root, tearoff=0)
        m.add_command(label="Remove border", command=on_remove_border_click)
        # m.add_command(label="Resize window", command=on_resize_window_click)
        m.add_command(label="Restore border", command=on_restore_border_click)
        m.add_command(label="Refresh list", command=refresh_lb)
        m.add_command(label="add to ignored windows", command=lambda: add_to_ignored_windows(selection))
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()


root = Tk()
root.title("Border Remover 9000")
root.geometry("400x400")
lb = Listbox(root, selectmode=SINGLE)
refresh_lb()
lb.grid(row=0, column=0, sticky="news", columnspan=2, padx=PAD_X, )

button = Button(root, text="Remove border", command=on_remove_border_click)
button2 = Button(root, text="Restore border", command=on_restore_border_click)
button.grid(row=1, column=0, sticky="news", padx=(PAD_X, 0), pady=(0, PAD_Y))
button2.grid(row=1, column=1, sticky="news", padx=(0, PAD_X), pady=(0, PAD_Y))
lb.bind("<Button-3>", right_click)
Grid.columnconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
root.iconbitmap(resource_path('icon.ico'))



def main():
    root.mainloop()


if __name__ == '__main__':
    main()
