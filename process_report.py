#!/usr/bin/env python3
import functools
import tkinter
import webbrowser
from tkinter import ttk, messagebox, filedialog

import markdown
import tkinterhtml

from file_io import read_file

MAXIMUM_NECESSARY_PAYMENT = 1042.86
LEFT_TO_GET_TEMPLATE = "Left to contribute: $"
ABOUT_URL = 'https://github.com/olliechick/amp-kiwisaver-helper/blob/master/README.md'


def process_data(file_contents, accounts):
    """Returns:
     - the contents of a CSV file of contributions that count
     - the amount left until you have given MAXIMUM_NECESSARY_PAYMENT"""
    items = ''.join(file_contents.split("Effective date Description Account Amount Units")[1:]).split()

    output_csv = 'Account,Amount\n'
    total = 0

    next_ = next_2 = None
    for i, item in enumerate(items):
        if i < (len(items) - 2):
            next_ = items[i + 1]
            next_2 = items[i + 2]
        if next_2.startswith('$'):
            account = item + " " + next_
            dollars = next_2
            if account in accounts:
                total += float(dollars[1:])
                output_csv += ','.join([account, dollars]) + '\n'

    left_to_give = MAXIMUM_NECESSARY_PAYMENT - total
    if left_to_give < 0:
        left_to_give = 0

    return output_csv, left_to_give


class ProcessReport:
    csv_contents = ''
    left_to_get = MAXIMUM_NECESSARY_PAYMENT
    root = None
    new_account_name = None

    def __init__(self):
        self.html = markdown.markdown(read_file('README.md'))
        accounts = read_file('config/accounts.txt').split('\n')
        self.accounts_list = [account for account in accounts if account.strip() != '']

    def save_csv(self):
        try:
            f = filedialog.asksaveasfile(mode='w', defaultextension=".csv",
                                         filetypes=(("CSV file", "*.csv"), ("All Files", "*.*")))
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            text2save = self.csv_contents
            f.write(text2save)
            f.close()
        except PermissionError:
            messagebox.showerror("Error",
                                 "Unable to save file. Maybe you have it open? If so, close it, then try again.")

    def add_account(self, listbox):
        print(self.new_account_name.get(), "<-")
        self.accounts_list.append(self.new_account_name.get())
        listbox.insert(tkinter.END, self.new_account_name.get())
        self.update_calculation()
        self.new_account_name.set('')

    def delete_account(self, listbox):
        pass


    def open_valid_accounts_gui(self):
        root = tkinter.Toplevel(self.root)
        root.transient(self.root)
        root.grab_set()

        root.title("Accounts whose contributions count")
        frame = ttk.Frame(root)
        frame.pack(fill=tkinter.BOTH, expand=True)

        edit_bar = ttk.Frame(frame)
        edit_bar.pack(fill=tkinter.X, expand=True, side=tkinter.BOTTOM)

        listbox = tkinter.Listbox(frame, selectmode=tkinter.SINGLE)
        listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        scrollbar = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        listbox.pack()

        self.new_account_name = tkinter.StringVar(root)
        new_account_textbox = ttk.Entry(edit_bar, textvariable=self.new_account_name)
        new_account_textbox.pack(in_=edit_bar, side=tkinter.LEFT, expand=True, fill=tkinter.X)

        add_button = ttk.Button(edit_bar, text="Add", command=functools.partial(self.add_account, listbox))
        add_button.pack(in_=edit_bar, side=tkinter.LEFT)

        delete_button = ttk.Button(edit_bar, text="Delete", command=functools.partial(self.delete_account, listbox))
        delete_button.pack(in_=edit_bar, side=tkinter.LEFT)

        for item in self.accounts_list:
            listbox.insert(tkinter.END, item)

        root.mainloop()

    def open_about(self):
        root = tkinter.Toplevel(self.root)
        root.transient(self.root)
        root.grab_set()

        root.title("About")
        big_frame = ttk.Frame(root)
        big_frame.pack(fill='both', expand=True)

        save_button = ttk.Button(big_frame, text="Open in web browser",
                                 command=functools.partial(webbrowser.open, ABOUT_URL))
        save_button.pack(in_=big_frame, side=tkinter.LEFT)

        html_frame = tkinterhtml.HtmlFrame(root)
        html_frame.pack()
        html_frame.set_content(self.html)

        root.iconbitmap('favicon.ico')
        root.mainloop()
        root.grab_set()

    def update_calculation(self, *args):
        textbox_contents = self.textbox.get(1.0, tkinter.END)
        self.csv_contents, self.left_to_get = process_data(textbox_contents, self.accounts_list)
        self.left_to_get_label.config(text=LEFT_TO_GET_TEMPLATE + str('{:,.2f}'.format(self.left_to_get)))

    def launch_gui(self):
        self.root = tkinter.Tk()
        self.root.title("AMP KiwiSaver helper")
        big_frame = ttk.Frame(self.root)
        big_frame.pack(fill='both', expand=True)

        menu = tkinter.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Set valid accounts", command=self.open_valid_accounts_gui)
        file_menu.add_command(label="About", command=functools.partial(self.open_about))

        label = ttk.Label(big_frame, text="Copy and paste the contents of the report PDF below:")
        label.pack()

        # Text box

        text_frame = ttk.Frame(big_frame)
        text_frame.pack(fill=tkinter.BOTH, expand=True)

        self.textbox = tkinter.Text(text_frame)
        scrollbar = ttk.Scrollbar(text_frame)

        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.textbox.pack(expand=1, fill=tkinter.BOTH)
        scrollbar.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=scrollbar.set)
        self.textbox.bind('<KeyRelease>', self.update_calculation)

        # Bottom bar

        self.left_to_get_label = ttk.Label(big_frame, text=LEFT_TO_GET_TEMPLATE + str(MAXIMUM_NECESSARY_PAYMENT))
        save_button = ttk.Button(big_frame, text="Save CSV", command=self.save_csv)

        self.left_to_get_label.pack(in_=big_frame, side=tkinter.LEFT, expand=1, fill=tkinter.X)
        save_button.pack(in_=big_frame, side=tkinter.LEFT, expand=1, fill=tkinter.X)

        # Set up

        self.root.geometry('900x500')
        self.root.iconbitmap('favicon.ico')
        self.root.mainloop()


def main():
    ProcessReport().launch_gui()


if __name__ == '__main__':
    main()
