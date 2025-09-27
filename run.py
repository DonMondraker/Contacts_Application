#!/usr/bin/python3
import sqlite3
import customtkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from templates.app_configuration import *

tk.set_appearance_mode(app_appearance_mode)
tk.set_default_color_theme(app_color_theme)

conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL,
    phone INTEGER,
    address TEXT NOT NULL
)
""")
conn.commit()

def send_to_database(name, last_name, email, phone, address, box):
    user_name = name.get()
    user_last_name = last_name.get()
    user_email = email.get()
    user_phone = phone.get()
    user_address = address.get()
    if not all([user_name, user_last_name, user_email, user_phone, user_address]):
        messagebox.showerror('Error', 'All fields must be entered')
    else:
        cursor.execute('INSERT INTO users (name, lastname, email, phone, address) VALUES (?, ?, ?, ?, ?)',
                       (user_name, user_last_name, user_email, user_phone, user_address))
        conn.commit()
        name.delete(0, 'end')
        last_name.delete(0, 'end')
        email.delete(0, 'end')
        phone.delete(0, 'end')
        address.delete(0, 'end')
        messagebox.showinfo('Info', 'Contact has been added')
        retrieve_from_database(box)

def retrieve_from_database(box):
    test_list = ['Name:', 'Lastname:', 'Email:', 'Phone number:', 'Address:']
    row_col = 0
    count = 1
    for i in test_list:
        add_to_listbox = tk.CTkLabel(box, text=i)
        add_to_listbox.grid(row=0, column=row_col, padx=25)
        row_col +=1

    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        add_name_box = tk.CTkLabel(box, text=row[0])
        add_name_box.grid(row=count, column=0)
        add_lastname_box = tk.CTkLabel(box, text=row[1])
        add_lastname_box.grid(row=count, column=1)
        add_email_box = tk.CTkLabel(box, text=row[2])
        add_email_box.grid(row=count, column=2)
        add_phone_box = tk.CTkLabel(box, text=row[3])
        add_phone_box.grid(row=count, column=3)
        add_address_box = tk.CTkLabel(box, text=row[4])
        add_address_box.grid(row=count, column=4)
        count += 1

class MyApp(tk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(root_geometry)
        self.title(root_title)
        self.attributes(root_attribute, True)
        self.update()
        self.attributes(root_attribute, False)
        self.resizable(False, False)
        self.display_frame_one = tk.CTkFrame(self)
        self.display_frame_two = tk.CTkFrame(self)
        self.display_frame_three = tk.CTkFrame(self)
        self.display_frame_one.place(x=0, y=0, relwidth=1, relheight=1)
        self.config()

    def config(self):

        # Config Page One
        self.visual_frame = tk.CTkFrame(self.display_frame_one, width=400, height=300)
        self.visual_frame.place(x=105, y=45)

        self.visual_label = tk.CTkLabel(self.visual_frame, text='MyContacts', font=('arial', 50))
        self.visual_label.place(x=70, y=50)

        self.add_button = tk.CTkButton(self.visual_frame, text=button_one_text, command=self.slide_to_frame_two)
        self.add_button.place(x=130, y=160)
        self.display_button = tk.CTkButton(self.visual_frame, text=button_two_text, command=self.slide_to_frame_three)
        self.display_button.place(x=130, y=220)

        # Buttons Page two
        self.visual_frame_two = tk.CTkFrame(self.display_frame_two, width=400, height=345)
        self.visual_frame_two.place(x=105, y=0)
        self.name_entry = tk.CTkEntry(self.display_frame_two, placeholder_text='               Name:')
        self.name_entry.grid(row=0, column=0, pady=20, padx=230)
        self.lastname_entry = tk.CTkEntry(self.display_frame_two, placeholder_text='           Lastname:')
        self.lastname_entry.grid(row=1, column=0)
        self.email_entry = tk.CTkEntry(self.display_frame_two, placeholder_text='              Email:')
        self.email_entry.grid(row=2, column=0, pady=20)
        self.phone_entry = tk.CTkEntry(self.display_frame_two, placeholder_text='       Phone Number:')
        self.phone_entry.grid(row=3, column=0)
        self.address_entry = tk.CTkEntry(self.display_frame_two, placeholder_text='            Address:')
        self.address_entry.grid(row=4, column=0, pady=20)

        self.submit_button = tk.CTkButton(self.display_frame_two, text='Submit', command= lambda: send_to_database(self.name_entry, self.lastname_entry, self.email_entry, self.phone_entry, self.address_entry, self.listbox))
        self.submit_button.grid(row=5, column=0)

        self.return_button = tk.CTkButton(self.display_frame_two, text='Home', command=self.slide_to_frame_one_from_two)
        self.return_button.grid(row=6, column=0, pady=20)

        # Buttons Page Three
        self.listbox = tk.CTkScrollableFrame(self.display_frame_three, width=550, height=310)
        self.listbox.pack(pady=20)

        self.return_button_two = tk.CTkButton(self.display_frame_three, text='Home', command=self.slide_to_frame_one_from_three)
        self.return_button_two.pack(pady=0)


    def slide_to_frame_two(self):
        self.animate_slide(self.display_frame_one, self.display_frame_two, direction='left')

    def slide_to_frame_three(self):
        self.animate_slide(self.display_frame_one, self.display_frame_three, direction='right')
        retrieve_from_database(self.listbox)

    def slide_to_frame_one_from_two(self):
        self.animate_slide(self.display_frame_two, self.display_frame_one, direction='right')

    def slide_to_frame_one_from_three(self):
        self.animate_slide(self.display_frame_three, self.display_frame_one, direction='left')

    def animate_slide(self, current, next_frame, direction="left", step=20):
        width = self.winfo_width()
        if direction == "left":
            start_pos, end_pos = 0, -width
            next_start = width
            delta = -step
        else:  # right
            start_pos, end_pos = 0, width
            next_start = -width
            delta = step

        next_frame.place(x=next_start, y=0, relwidth=1, relheight=1)

        def slide(pos):
            if (direction == "left" and pos > end_pos) or (direction == "right" and pos < end_pos):
                current.place(x=pos, y=0, relwidth=1, relheight=1)
                next_frame.place(x=pos + width if direction == "left" else pos - width, y=0,
                                 relwidth=1, relheight=1)
                self.after(10, lambda: slide(pos + delta))
            else:
                current.place_forget()
                next_frame.place(x=0, y=0, relwidth=1, relheight=1)

        slide(start_pos)

    def run(self):

        self.mainloop()

if __name__ == '__main__':
    MyApp().run()
