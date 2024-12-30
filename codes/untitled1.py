import tkinter as tk
class LoginScreen:
    def __init__(self,root):
        self.root = root
        self.root.title("LogIn Screen")

        self.screenW = self.root.winfo_screenwidth()
        self.screenH = self.root.winfo_screenheight()
        taskbar_height = 40  # Assuming the taskbar height is 40 pixels (you should adjust this according to your system)
        self.root.geometry("%dx%d+%d+%d" % (self.screenW, self.screenH - taskbar_height, -12, 0))
        self.root.resizable(False, False)


        # Background color
        self.root.configure(bg="#2980b9")
        #self.root.configure(bg="#000000")

        ################title######
        lbl_title = tk.Label(self.root, text="Student Helper System", font=("times new roman", 40, "bold"), bg="black", fg="silver", bd=4, relief=tk.RIDGE)
        # lbl_title.place(x=0,y=0,width=self.screenW,height=50)
        lbl_title.pack()

        ########### logo#########

        # Header Label
        self.header_label = tk.Label(self.root, text="Welcome In LogIn Screen", font=("Helvetica", 28, "bold"), bg="#2980b9", fg="white")
        self.header_label.pack(pady=40)

        # Username Label and Entry
        self.username_label = tk.Label(self.root, text="Name:", font=("Helvetica", 16), bg="#2980b9", fg="white")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self.root, text="Password:", font=("Helvetica", 16), bg="#2980b9", fg="white")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 16))
        self.password_entry.pack(pady=5)

        # Show Password Checkbutton
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.root, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#2980b9", fg="white", font=("Helvetica", 12))
        self.show_password_checkbutton.place(x=self.screenW-620,y=self.screenH-555)
        #self.show_password_checkbutton.pack(pady=5)
        # Create a label that behaves like a button
        text_button = tk.Label(root, text="don't have an account?SignUp", fg="white",bg="#2980b9", cursor="hand2")
        text_button.pack()
        # Bind the label to a click event
        text_button.bind("<Button-1>", lambda event: self.on_click())
        
        # Login Button
        self.login_button = tk.Button(self.root, text="Sign In", command=self.login, font=("Helvetica", 16), bg="#2c3e50", fg="white", relief="raised", padx=10)
        self.login_button.pack(pady=20, ipadx=10, ipady=5)

    def on_click(x):
        '''
        dp = DataBase()
        username = self.username_entry.get()
        password = self.password_entry.get()
        dp.addStudent(username,password)
        '''
        print("Signup completed")
        #self.root.destroy()
        # Open the new window
        #self.open_new_window()
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        '''
        dp = DataBase()
        students = dp.showAllStudents()
        for i in students:
            # Check if username and password are correct
            if username == i[0] and password == i[1]:
                messagebox.showinfo("Sign In", "Sign In Successfull!")
                # Close the login window
                self.root.destroy()
                # Open the new window
                self.open_new_window()
                break
        else:
            messagebox.showerror("Sign In", "اUserName Or Password Incorrect")
        '''
        tk.messagebox.showinfo("info", username+"   "+password)
    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def open_new_window(self):
        '''
         root=Tk()
         obj=Dashboard(root)
         root.mainloop() 
        '''
        print("new window")

# Initialize and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
