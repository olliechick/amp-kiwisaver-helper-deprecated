#!/usr/bin/env python3
import tkinter
from tkinter import ttk, messagebox, filedialog
import markdown, tkinterhtml

ENCODING = 'utf-8'
MAXIMUM_NECESSARY_PAYMENT = 1042.86
LEFT_TO_GET_TEMPLATE = "Left to get: $"


def read_file(filename):
    """Returns content of file"""
    file = open(filename, 'r', encoding=ENCODING)
    content = file.read()
    file.close()
    return content


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


def open_about():
    root = tkinter.Tk()
    root.title("Test")
    html = markdown.markdown(read_file('README.md'))
    html_frame = tkinterhtml.HtmlFrame(root)
    html_frame.pack()
    html_frame.set_content(html)

    root.iconbitmap('favicon.ico')
    root.mainloop()


class ProcessReport:
    csv_contents = ''
    left_to_get = MAXIMUM_NECESSARY_PAYMENT

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
                                 "Unable to save output.csv. Maybe you have it open? If so, close it, then try again.")

    def open_valid_accounts_gui(self):
        messagebox.showinfo("Information", "Not yet implemented")

    def launch_gui(self):
        root = tkinter.Tk()
        root.title("AMP KiwiSaver helper")
        big_frame = ttk.Frame(root)
        big_frame.pack(fill='both', expand=True)

        menu = tkinter.Menu(root)
        root.config(menu=menu)
        file_menu = tkinter.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Set valid accounts", command=self.open_valid_accounts_gui)
        file_menu.add_command(label="About", command=open_about)

        label = ttk.Label(big_frame, text="Copy and paste the contents of the report PDF below:")
        label.pack()

        # Text box

        def textbox_updated(*args):
            textbox_contents = textbox.get(1.0, tkinter.END)
            self.csv_contents, self.left_to_get = process_data(textbox_contents)
            left_to_get_label.config(text=LEFT_TO_GET_TEMPLATE + str('{:,.2f}'.format(self.left_to_get)))

        text_frame = ttk.Frame(big_frame)
        text_frame.pack(fill=tkinter.BOTH, expand=True)

        textbox = tkinter.Text(text_frame)
        scrollbar = ttk.Scrollbar(text_frame)

        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        textbox.pack(expand=1, fill=tkinter.BOTH)
        scrollbar.config(command=textbox.yview)
        textbox.config(yscrollcommand=scrollbar.set)
        textbox.bind('<KeyRelease>', textbox_updated)

        # Bottom bar

        left_to_get_label = ttk.Label(big_frame, text=LEFT_TO_GET_TEMPLATE + str(MAXIMUM_NECESSARY_PAYMENT))
        save_button = ttk.Button(big_frame, text="Save CSV", command=self.save_csv)

        left_to_get_label.pack(in_=big_frame, side=tkinter.LEFT, expand=1, fill=tkinter.X)
        save_button.pack(in_=big_frame, side=tkinter.LEFT, expand=1, fill=tkinter.X)

        # Set up

        root.geometry('900x500')
        root.iconbitmap('favicon.ico')
        root.mainloop()


def main():
    ProcessReport().launch_gui()


if __name__ == '__main__':
    main()
