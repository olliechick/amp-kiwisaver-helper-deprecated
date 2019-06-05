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


def process_data(input_filename):
    """Returns:
     - the contents of a CSV file of contributions that count
     - the amount left until you have given MAXIMUM_NECESSARY_PAYMENT"""
    file_contents = read_file(input_filename)
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


def save_csv():
    output_csv, total = process_data('input.txt')
    write_to_file('output.csv', output_csv)


def display_left_to_get():
    output_csv, total = process_data('input.txt')
    messagebox.showinfo("Left to get", '$' + str(total.__round__(2)))


def main():
    root = tkinter.Tk()
    big_frame = ttk.Frame(root)
    big_frame.pack(fill='both', expand=True)

    # label = ttk.Label(big_frame, text="Copy and paste the contents of the report PDF below:")
    label = ttk.Label(big_frame, text="")
    label.pack()
    ttk.Button(root, text="Show left to get", command=display_left_to_get).pack()
    label.pack()
    ttk.Button(root, text="Save CSV", command=save_csv).pack()
    root.mainloop()


if __name__ == '__main__':
    main()
