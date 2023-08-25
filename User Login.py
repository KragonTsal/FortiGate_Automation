from tkinter import *

# Window Creation and Sizing
window = Tk()
window.geometry("350x120")

# User Name Label
user_name_label = Label(window, text = "Username").place(x = 20, y = 20)

# User Name Entry Field
user_name_entry = Entry(window, width = 40).place(x = 90, y = 20)

# User Password Label
user_password_label = Label(window, text = "Password").place(x = 20, y = 50)

# User Password Entry Field
user_password_entry = Entry(window, width = 40).place(x = 90, y = 50)

# Submit Button
submit_button = Button(window, text = "Submit").place(x = 20, y = 80)

window.mainloop()