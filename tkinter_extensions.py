import tkinter


class FancyListboxFrame(tkinter.Frame):

    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.listbox = tkinter.Listbox(self)
        self.pack(side="left", fill="y")

        self.popup_menu = tkinter.Menu(self.listbox, tearoff=0)
        self.popup_menu.add_command(label="Delete", command=self.delete_selected)
        self.popup_menu.add_command(label="Select All", command=self.select_all)

        scrollbar = tkinter.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)
        # tkinter.Label(self, text="Bottom label").pack()

        self.listbox.bind("<Button-3>", self.popup)  # Button-2 on Aqua

    def popup(self, event):
        try:
            print(event)
            self.popup_menu.tk_popup(event.x, event.y, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        for i in self.listbox.curselection()[::-1]:
            self.listbox.delete(i)

    def select_all(self):
        self.listbox.selection_set(0, 'end')
