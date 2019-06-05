#!/usr/bin/env python3
import tkinter
from tkinter import ttk, messagebox

ENCODING = 'utf-8'
MAXIMUM_NECESSARY_PAYMENT = 1042.86


def write_to_file(filename, content, mode='w+'):
    """saves the string content to filename."""
    is_open = False
    while not is_open:
        try:
            f = open(filename, mode)
            is_open = True
        except PermissionError:
            input(
                "Permission error when opening " + filename + ". Let me open it (e.g. by closing it elsewhere) and press enter...")
    f.write(content)
    f.close()


def append_to_file(filename, content):
    write_to_file(filename, content, 'a')


def read_file(filename):
    """Returns content of file"""
    file = open(filename, 'r')
    return file.read()


def process_data(file_contents):
    """Returns:
     - the contents of a CSV file of contributions that count
     - the amount left until you have given MAXIMUM_NECESSARY_PAYMENT"""
    items = ''.join(file_contents.split("Effective date Description Account Amount Units")[1:]).split()
    accounts = read_file('accounts.txt').split('\n')

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

    def save_csv(self):
        write_to_file('output.csv', self.csv_contents)

    def display_left_to_get(self):
        messagebox.showinfo("Left to get", '$' + str(self.left_to_get.__round__(2)))

    def launch_gui(self):
        root = tkinter.Tk()
        root.title("AMP KiwiSaver helper")
        big_frame = ttk.Frame(root)
        big_frame.pack(fill='both', expand=True)

        label = ttk.Label(big_frame, text="Copy and paste the contents of the report PDF below:")
        label.pack()

        # Text box

        def textbox_updated(*args):
            # check the text
            textbox_contents = textbox.get(1.0, tkinter.END)
            self.csv_contents, self.left_to_get = process_data(textbox_contents)

        text_frame = ttk.Frame(big_frame)
        text_frame.pack(fill='both', expand=True)

        report_text = tkinter.StringVar()
        textbox = tkinter.Text(text_frame)
        scrollbar = ttk.Scrollbar(text_frame)

        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        textbox.pack(expand=1, fill=tkinter.BOTH)
        scrollbar.config(command=textbox.yview)
        textbox.config(yscrollcommand=scrollbar.set)
        textbox.bind('<KeyRelease>', textbox_updated)

        # Bottom bar

        left_to_get_label = ttk.Label(big_frame, text="Left to get: $" + str(MAXIMUM_NECESSARY_PAYMENT))
        save_button = ttk.Button(big_frame, text="Save CSV", command=self.save_csv)

        left_to_get_label.pack(in_=big_frame, side=tkinter.LEFT, expand=1, fill=tkinter.X)
        save_button.pack(in_=big_frame, side=tkinter.LEFT, expand=1, fill=tkinter.X)

        # Set up

        root.geometry('300x500')
        root.mainloop()


def main():
    ProcessReport().launch_gui()


if __name__ == '__main__':
    main()
