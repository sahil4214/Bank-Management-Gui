#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import scrolledtext,messagebox
from difflib import SequenceMatcher


# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers
                      (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, phone TEXT, email TEXT, address TEXT, password TEXT, balance REAL)''')
    conn.commit()
    conn.close()

# Function to insert a new customer record during registration
def insert_customer(name, gender, age, phone, email, address, password, balance):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, gender, age, phone, email, address, password, balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (name, gender, age, phone, email, address, password, balance))
    conn.commit()
    conn.close()
# Function to create the chatbot table if it doesn't exist
def create_chatbot_table():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chatbot
                      (id INTEGER PRIMARY KEY, query TEXT, response TEXT)''')
    conn.commit()
    conn.close()    




# Function to handle registration button click


def register():
    global entry_name, entry_gender, entry_age, entry_phone, entry_email, entry_address, entry_password, entry_balance
    name = entry_name.get()
    gender = entry_gender.get()
    age = entry_age.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    password = entry_password.get()
    balance = entry_balance.get()

  

    if name == "" or gender == "" or age=="" or phone=="" or email=="" or address=="" or password == "" or balance == "":
        messagebox.showerror("Error", "Please fill in all the fields.")
        return

    try:
        age = int(age)
        balance = float(balance)
    except ValueError:
        messagebox.showerror("Error", "Invalid balance. Please enter a valid number.")
        return

    if len(phone) != 10:
        messagebox.showerror("Error", "Phone number must be exactly 10 digits.")
        return
def validate_phone_input(char):
    return char.isdigit() and len(entry_phone.get()) < 10

    insert_customer(name, gender, age, phone, email, address, password, balance)
    success_message = "Registration successful!"
    success_label = tk.Label(register_screen, text=success_message, fg="green")
    success_label.grid(row=2, column=0, columnspan=2, pady=10)  
    messagebox.showinfo("Success", success_message)
    register_screen.destroy()
# Function to handle login button click
def login():
    global entry_username, entry_login_password
    name = entry_username.get()
    password = entry_login_password.get()

    if name == "" or password == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    if name == "admin" and password == "admin123":
        login_screen.destroy()
        success_message = "Admin login successful!"
        success_label = tk.Label(root, text=success_message, fg="green")
        success_label.grid(row=2, column=0, columnspan=2, pady=10)# Use grid manager here
        messagebox.showinfo("Success", success_message)
        view_all_customers()
    else:
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM customers WHERE name = ?", (name,))
        result = cursor.fetchone()
        conn.close()

        if result is None:
            messagebox.showerror("Error", "User not found.")
        else:
            stored_password = result[0]
            if password == stored_password:
                login_screen.destroy()
                success_message = "Login successful!"
                success_label = tk.Label(root, text=success_message, fg="green")
                success_label.grid(row=2, column=0, columnspan=2, pady=10)  # Use grid manager here
                messagebox.showinfo("Success", success_message)
                open_account_dashboard(name)
            else:
                messagebox.showerror("Error", "Invalid username or password.")



# Function to open the account dashboard
def open_account_dashboard(name):
    # Create the main dashboard screen
    dashboard_screen = tk.Toplevel(root)
    dashboard_screen.title("Account Dashboard")

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE name = ?", (name,))
    customer_info = cursor.fetchone()
    conn.close()

    label_welcome = tk.Label(dashboard_screen, text=f"Welcome, {name}!", font=("Helvetica", 14, "bold"))
    label_welcome.grid(row=0, column=0, columnspan=2, pady=10)

    label_info = tk.Label(dashboard_screen, text= f"Name: {customer_info[1]}\nGender: {customer_info[2]}\nAge: {customer_info[3]}\nPhone no: {customer_info[4]}\nEmail: {customer_info[5]}\nAddress: {customer_info[6]}\nPassword: {customer_info[7]}\nBalance: {customer_info[8]}",
                          font=("Helvetica", 12))
    label_info.grid(row=1, column=0, columnspan=2, pady=10)
    

    # Function to show personal information
    def show_personal_info():
        messagebox.showinfo("Personal Information", f"Name: {customer_info[1]}\nGender: {customer_info[2]}\nAge: {customer_info[3]}\nPhone no: {customer_info[4]}\nEmail: {customer_info[5]}\nAddress: {customer_info[6]}\nPassword: {customer_info[7]}\nBalance: {customer_info[8]}")
   
 # Function to handle deposit button click
    def deposit():
        deposit_screen = tk.Toplevel(dashboard_screen)
        deposit_screen.title("Deposit")

        def deposit_amount():
            try:
                amount = float(entry_deposit.get())

                if amount <= 0:
                    messagebox.showerror("Error", "Invalid deposit amount. Please enter a positive value.")
                    return

                new_balance = customer_info[8] + amount

                conn = sqlite3.connect("bank.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE customers SET balance = ? WHERE name = ?", (new_balance, name))
                conn.commit()
                conn.close()

                messagebox.showinfo("Deposit", f"Deposit successful. Your new balance is: {new_balance}")
                deposit_screen.destroy()
                open_account_dashboard(name)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")


        label_deposit = tk.Label(deposit_screen, text="Enter deposit amount:")
        label_deposit.grid(row=0, column=0, pady=5)
        entry_deposit = tk.Entry(deposit_screen)
        entry_deposit.grid(row=0, column=1, pady=5)
        btn_deposit = tk.Button(deposit_screen, text="Deposit", command=deposit_amount)
        btn_deposit.grid(row=1, column=0, columnspan=2, pady=5)
 # Function to handle withdraw button click
    def withdraw():
        withdraw_screen = tk.Toplevel(dashboard_screen)
        withdraw_screen.title("Withdraw")

        def withdraw_amount():
            try:
                amount = float(entry_withdraw.get())

                if amount <= 0:
                    messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a positive value.")
                    return

                current_balance = customer_info[8]

                if amount > current_balance:
                    messagebox.showerror("Error", "Insufficient balance.")
                else:
                    new_balance = current_balance - amount

                    conn = sqlite3.connect("bank.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE customers SET balance = ? WHERE name = ?", (new_balance, name))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Withdraw", f"Withdrawal successful. Your new balance is: {new_balance}")
                    withdraw_screen.destroy()
                    open_account_dashboard(name)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")


        label_withdraw = tk.Label(withdraw_screen, text="Enter withdrawal amount:")
        label_withdraw.grid(row=0, column=0, pady=5)
        entry_withdraw = tk.Entry(withdraw_screen)
        entry_withdraw.grid(row=0, column=1, pady=5)
        btn_withdraw = tk.Button(withdraw_screen, text="Withdraw", command=withdraw_amount)
        btn_withdraw.grid(row=1, column=0, columnspan=2, pady=5)

    # Add buttons for personal info, deposit, and withdraw
    btn_personal_info = tk.Button(dashboard_screen, text="Personal Information", command=lambda: show_personal_info())
    btn_personal_info.grid(row=2, column=0, columnspan=2, pady=5)

    btn_deposit = tk.Button(dashboard_screen, text="Deposit", command=deposit)
    btn_deposit.grid(row=3, column=0, pady=5)

    btn_withdraw = tk.Button(dashboard_screen, text="Withdraw", command=withdraw)
    btn_withdraw.grid(row=3, column=1, pady=5)
    
 # Use a partial function to pass arguments to the update_info function
    btn_update_info = tk.Button(dashboard_screen, text="Update Info", command=lambda: update_info(dashboard_screen, name))
    btn_update_info.grid(row=4, column=0, pady=5)
    
 #customer support chat bot  
   
    btn_customer_support = tk.Button(dashboard_screen, text="Customer Support", command=open_customer_support)
    btn_customer_support.grid(row=4, column=1, pady=5)




  

 # Function to show all customer data for admin
def view_all_customers():
    admin_screen = tk.Toplevel(root)
    admin_screen.title("Admin Panel")

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customer_data = cursor.fetchall()
    conn.close()

    tree = ttk.Treeview(admin_screen, columns=("ID", "Name", "Gender","Age","Phone no","Email","Address", "password","Balance"))
    tree.heading("#1", text="ID", anchor="w")
    tree.heading("#2", text="Name", anchor="w")
    tree.heading("#3", text="Gender", anchor="w")
    tree.heading("#4", text="Age", anchor="w")
    tree.heading("#5", text="Phone no", anchor="w")    
    tree.heading("#6", text="Email", anchor="w")
    tree.heading("#7", text="Address", anchor="w")
    tree.heading("#8", text="password", anchor="w")
    tree.heading("#9", text="Balance", anchor="w")
    
     # Adjust column widths
    tree.column("#1",width=10)    #id
    tree.column("#2", width=100)  # Name
    tree.column("#3", width=50)  # Gender
    tree.column("#4", width=40)   # Age
    tree.column("#5", width=80)  # Phone
    tree.column("#6", width=130)  # Email
    tree.column("#7", width=160)  # Address
    tree.column("#8", width=70)  # password
    tree.column("#9",width=90)  #balances

    tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)



    for data in customer_data:
        tree.insert("", "end", values=data)

    tree.pack()

# Create the main application window
root = tk.Tk()
root.title("SR Bank")
root.configure(bg='green')



# Function to handle "Register" button click
def open_register_screen():
    global register_screen, entry_name, entry_gender,entry_age,entry_phone,entry_email,entry_address, entry_password, entry_balance
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")

    label_name = tk.Label(register_screen, text="Name:")
    label_name.grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(register_screen)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    label_gender = tk.Label(register_screen, text="Gender:")
    label_gender.grid(row=1, column=0, padx=5, pady=5)
    entry_gender = tk.Entry(register_screen)
    entry_gender.grid(row=1, column=1, padx=5, pady=5)
    
    label_age = tk.Label(register_screen, text="Age:")
    label_age.grid(row=2, column=0, padx=5, pady=5)
    entry_age = tk.Entry(register_screen)
    entry_age.grid(row=2, column=1, padx=5, pady=5)
    
    label_phone = tk.Label(register_screen, text="Phone no:")
    label_phone.grid(row=3, column=0, padx=5, pady=5)
    entry_phone = tk.Entry(register_screen, validate="key")
    entry_phone['validatecommand'] = (entry_phone.register(validate_phone_input), '%S')
    entry_phone.grid(row=3, column=1, padx=5, pady=5)
    
    label_email = tk.Label(register_screen, text="Email:")
    label_email.grid(row=4, column=0, padx=5, pady=5)
    entry_email = tk.Entry(register_screen)
    entry_email.grid(row=4, column=1, padx=5, pady=5)
    
    label_address = tk.Label(register_screen, text="Address:")
    label_address.grid(row=5, column=0, padx=5, pady=5)
    entry_address = tk.Entry(register_screen)
    entry_address.grid(row=5, column=1, padx=5, pady=5)

    label_password = tk.Label(register_screen, text="Password:")
    label_password.grid(row=6, column=0, padx=5, pady=5)
    entry_password = tk.Entry(register_screen, show="*")
    entry_password.grid(row=6, column=1, padx=5, pady=5)

    label_balance = tk.Label(register_screen, text="Balance:")
    label_balance.grid(row=7, column=0, padx=5, pady=5)
    entry_balance = tk.Entry(register_screen)
    entry_balance.grid(row=7, column=1, padx=5, pady=5)

    btn_submit = tk.Button(register_screen, text="Submit", command=register)
    btn_submit.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

# Function to handle "Login" button click
def open_login_screen():
    global login_screen, entry_username, entry_login_password
    login_screen = tk.Toplevel(root)
    login_screen.title("Login")

    label_username = tk.Label(login_screen, text="Username:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(login_screen)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_login_password = tk.Label(login_screen, text="Password:")
    label_login_password.grid(row=1, column=0, padx=5, pady=5)
    entry_login_password = tk.Entry(login_screen, show="*")
    entry_login_password.grid(row=1, column=1, padx=5, pady=5)

    btn_login_submit = tk.Button(login_screen, text="Login", command=login)
    btn_login_submit.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

# Function to handle the update button click and open the update window
def update_info(dashboard_screen, name):
    update_screen = tk.Toplevel(dashboard_screen)
    update_screen.title("Update Information")

def start_update_process(name):
    # Get the current customer information
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT phone, email, address FROM customers WHERE name = ?", (name,))
    customer_info = cursor.fetchone()
    conn.close()

    # Create a new window for update
    update_screen = tk.Toplevel()
    update_screen.title("Update Information")

    # Display old information
    tk.Label(update_screen, text="Old Phone no: " + customer_info[0]).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(update_screen, text="Old Email: " + customer_info[1]).grid(row=1, column=0, padx=5, pady=5)
    tk.Label(update_screen, text="Old Address: " + customer_info[2]).grid(row=2, column=0, padx=5, pady=5)

    # Create entry fields for new information
    entry_new_phone_var = tk.StringVar()
    tk.Entry(update_screen, textvariable=entry_new_phone_var).grid(row=3, column=1, padx=5, pady=5)
    tk.Label(update_screen, text="New Phone no:").grid(row=3, column=0, padx=5, pady=5)

    entry_new_email_var = tk.StringVar()
    tk.Entry(update_screen, textvariable=entry_new_email_var).grid(row=4, column=1, padx=5, pady=5)
    tk.Label(update_screen, text="New Email:").grid(row=4, column=0, padx=5, pady=5)

    entry_new_address_var = tk.StringVar()
    tk.Entry(update_screen, textvariable=entry_new_address_var).grid(row=5, column=1, padx=5, pady=5)
    tk.Label(update_screen, text="New Address:").grid(row=5, column=0, padx=5, pady=5)

    # Function to update the data
    def update_data():
        new_phone = entry_new_phone_var.get()
        new_email = entry_new_email_var.get()
        new_address = entry_new_address_var.get()

        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        if new_phone:
            cursor.execute("UPDATE customers SET phone = ? WHERE name = ?", (new_phone, name))
        if new_email:
            cursor.execute("UPDATE customers SET email = ? WHERE name = ?", (new_email, name))
        if new_address:
            cursor.execute("UPDATE customers SET address = ? WHERE name = ?", (new_address, name))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Data updated successfully.")
        update_screen.destroy()

    tk.Button(update_screen, text="Update", command=update_data).grid(row=6, column=0, columnspan=2, padx=5, pady=10)
 
 # Modify the existing update_info function
def update_info(dashboard_screen, name):
    start_update_process(name)   




# Function to add user query and bot response to the database


def add_query_response(query, response):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chatbot (query, response) VALUES (?, ?)", (query, response))
    conn.commit()
    conn.close()

# Function to handle user queries and generate chatbot responses
def handle_query(user_query):
    # Define the rules and corresponding responses
    rules = [
        {
            "rule": "i was face problem during withdraw money",
            "response": "Dear User currently bank server down so please try after some time."
        },
        {
            "rule":"i want to forget password",
            "response":"dear user you can go now on account dashboard and click on update button for new password when you enter new password old will be automaticaly destroy and new will be update."
        },
        {
          "rule":"how can i change email or password",
          "response":"click on update button for change email or password."  
        },
        {
            "rule":"what is my account balance",
            "response": "Your current account balance you can see on your personal information sorry for that but i have not permittion to fetch any users personal information . ."
        },
        {
            "rule":"how many intrest provide me this bank",
            "response":"This Bank provide you 4.5% intrest ,also provide 7% on fd ."
        },
        {
            "rule":"what is your name",
            "response":"i'm your Ai tool for here to help regarding bank related problem."
        },
        
        {
            "rule": "transfer money",
            "response": "You can transfer money to another account by clicking on the 'Transfer' button on your dashboard.but currently it was in build condition so wait few days for this new feature ."
        },
        # Add more rules and responses as needed
    ]

    # Set a threshold for similarity matching
    similarity_threshold = 0.45

    # Check if the user query matches any of the rules
    matched_rule = None
    for rule in rules:
        similarity = SequenceMatcher(None, user_query.lower(), rule["rule"].lower()).ratio()
        if similarity >= similarity_threshold:
            matched_rule = rule
            break

    # If a matching rule is found, respond with the corresponding response
    if matched_rule:
        response = matched_rule["response"]
        add_query_response(user_query, response)
        return response

    # If no matching rule is found, respond with a default message
    default_response = "Sorry, I am not able to assist you with that.please provide me more information about it."
    add_query_response(user_query, default_response)
    return default_response
#customer support button
    # Create chatbot table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS chatbot
                      (id INTEGER PRIMARY KEY, query TEXT, response TEXT)''')
    conn.commit()
    conn.close()
# Function to handle customer support button click
def open_customer_support():
    customer_support_screen = tk.Toplevel(root)
    customer_support_screen.title("Customer Support")

    chat_log = tk.Text(customer_support_screen, width=60, height=15)
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Use fill and expand options

    user_input = tk.Text(customer_support_screen, width=50, height=3)
    user_input.pack(padx=10, pady=10, fill=tk.X, expand=True)  # Use fill and expand options

    # Function to add bot response to the chat log
    def add_bot_response(response):
        chat_log.insert(tk.END, "Bot: " + response + "\n")
        chat_log.see(tk.END)

    # Function to handle user interactions with the chatbot
    def chat_with_bot():
        user_query = user_input.get("1.0", tk.END).strip()
        if user_query:
            bot_response = handle_query(user_query)
            add_bot_response(bot_response)

            # Clear the user input field
            user_input.delete("1.0", tk.END)

    send_button = tk.Button(customer_support_screen, text="Send", command=chat_with_bot)
    send_button.pack(pady=10)


# Add labels and buttons for the main screen
label_welcome = tk.Label(root, text="Welcome to SR Bank", font=("Helvetica", 18, "bold"))
label_welcome.grid(row=0, column=0, columnspan=2, pady=20)

btn_register = tk.Button(root, text="Register", font=("Helvetica", 12), command=open_register_screen)
btn_register.grid(row=1, column=0, padx=10, pady=10)

btn_login = tk.Button(root, text="Login", font=("Helvetica", 12), command=open_login_screen)
btn_login.grid(row=1, column=1, padx=10, pady=10)


# Create the database table if it doesn't exist
create_table()

create_chatbot_table()

root.mainloop()


# In[ ]:




