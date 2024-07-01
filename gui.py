from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from main import *


def view_passwords_gui():
    passwords = view_passwords()
    if not hasattr(view_passwords_gui, 'password_text'):
        view_passwords_gui.password_text = Text(root, wrap=WORD, height=10, width=50)
        view_passwords_gui.password_text.place(relx=0.5, rely=0.4, anchor=CENTER)

    view_passwords_gui.password_text.delete('1.0', END)
    if passwords:
        view_passwords_gui.password_text.insert(END, passwords)
    else:
        view_passwords_gui.password_text.insert(END, "No passwords found.")
    view_passwords_gui.password_text.config(state=NORMAL)


def show_add_password_fields():
    if not hasattr(show_add_password_fields, 'add_frame'):
        show_add_password_fields.add_frame = Frame(root)
        show_add_password_fields.add_frame.place(relx=0.5, rely=0.55, anchor=CENTER)

        site_label = ttk.Label(show_add_password_fields.add_frame, text="Site")
        site_label.grid(row=0, column=0, padx=5, pady=5)
        show_add_password_fields.site_entry = ttk.Entry(show_add_password_fields.add_frame)
        show_add_password_fields.site_entry.grid(row=0, column=1, padx=5, pady=5)

        password_label = ttk.Label(show_add_password_fields.add_frame, text="Password")
        password_label.grid(row=1, column=0, padx=5, pady=5)
        show_add_password_fields.password_entry = ttk.Entry(show_add_password_fields.add_frame, show="*")
        show_add_password_fields.password_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(show_add_password_fields.add_frame, text="Add", command=add_password_gui)
        add_button.grid(row=2, columnspan=2, pady=10)


def add_password_gui():
    site = show_add_password_fields.site_entry.get().strip()
    password = show_add_password_fields.password_entry.get().strip()
    if site and password:
        add_password(site, password)
        messagebox.showinfo("Success", "Password added successfully!")
        show_add_password_fields.site_entry.delete(0, END)
        show_add_password_fields.password_entry.delete(0, END)
    else:
        messagebox.showwarning("Input Error", "Please enter both site and password.")


def show_delete_password_fields():
    if not hasattr(show_delete_password_fields, 'delete_frame'):
        show_delete_password_fields.delete_frame = Frame(root)
        show_delete_password_fields.delete_frame.place(relx=0.5, rely=0.75, anchor=CENTER)

        delete_site_label = ttk.Label(show_delete_password_fields.delete_frame, text="Site to delete")
        delete_site_label.grid(row=0, column=0, padx=5, pady=5)
        show_delete_password_fields.delete_site_entry = ttk.Entry(show_delete_password_fields.delete_frame)
        show_delete_password_fields.delete_site_entry.grid(row=0, column=1, padx=5, pady=5)

        delete_button = ttk.Button(show_delete_password_fields.delete_frame, text="Delete", command=delete_password_gui)
        delete_button.grid(row=1, columnspan=2, pady=10)


def delete_password_gui():
    site = show_delete_password_fields.delete_site_entry.get().strip()
    if site:
        success = delete_password(site)
        if success:
            messagebox.showinfo("Success", "Password deleted successfully!")
            show_delete_password_fields.delete_site_entry.delete(0, END)
        else:
            messagebox.showwarning("Not Found", "No password found for the given site.")
    else:
        messagebox.showwarning("Input Error", "Please enter a site to delete.")







initialize_password_file()
# Создание основного окна Tkinter
root = Tk()
root.title('Password Manager')
root.geometry("600x450")

# Кнопка для просмотра паролей
view_button = ttk.Button(root, text="View Passwords", command=view_passwords_gui)
view_button.place(relx=0.5, rely=0.2, anchor=CENTER, height=40, width=200)

# Кнопка для добавления пароля
add_button = ttk.Button(root, text="Add Password", command=show_add_password_fields)
add_button.place(relx=0.5, rely=0.3, anchor=CENTER, height=40, width=200)

# Кнопка для удаления пароля
delete_button = ttk.Button(root, text="Delete Password", command=show_delete_password_fields)
delete_button.place(relx=0.5, rely=0.4, anchor=CENTER, height=40, width=200)






root.mainloop()