import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from PIL import Image, ImageTk

class SignIn:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper System")
        self.root.geometry("800x600")
        self.color = "#2980b9"
        self.root.configure(bg=self.color)

        # Firebase setup
        self.initialize_firebase()

        # GUI Components
        self.create_header()
        self.create_left_frame()
        self.create_right_frame()

    def initialize_firebase(self):
        """Initialize Firebase."""
        # Firebase admin setup
        service_account_key_path = "serviceAccountKey.json"
        cred = credentials.Certificate(service_account_key_path)
        try:
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print("Firebase already initialized.")

        # Firebase config for Pyrebase
        firebase_config = {
            "apiKey": "AIzaSyDz26pW1o-cDk8-eOnoHcJt4m1lM4ZfYG4",
            "authDomain": "student-helper-system-35ccd.firebaseapp.com",
            "projectId": "student-helper-system-35ccd",
            "storageBucket": "student-helper-system-35ccd.firebasestorage.app",
            "messagingSenderId": "693757805149",
            "appId": "1:693757805149:web:e00a5f8d303c530faa43b4",
            "databaseURL": "https://console.firebase.google.com/u/1/project/student-helper-system-35ccd/database/student-helper-system-35ccd-default-rtdb/data/~2F"
        }
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()

    def create_header(self):
        """Create the header of the app."""
        header = tk.Label(self.root, text="Student Helper System", bg="black", fg="white", font=("Arial", 20))
        header.pack(fill=tk.X)

    def create_left_frame(self):
        """Create the left frame for the sign-up form."""
        self.left_frame = tk.Frame(self.root, bg=self.color, width=400, padx=20, pady=20)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)


        tk.Label(self.left_frame, text="Email", bg=self.color, font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.email_entry = tk.Entry(self.left_frame, width=30)
        self.email_entry.grid(row=0, column=1)

        tk.Label(self.left_frame, text="Password", bg=self.color, font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.left_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1)
        
        # Show Password Checkbutton
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.left_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#2980b9", fg="white", font=("Helvetica", 12)).grid(row=1, column=2)

        self.text_button = tk.Label(self.left_frame, text="don't have an account?SignUp", fg="white",bg="#2980b9", cursor="hand2")
        self.text_button.grid(row=2, column=1)
        # Bind the label to a click event
        self.text_button.bind("<Button-1>", lambda event: self.on_click())

        signin_button = tk.Button(self.left_frame, text="Sign In", bg="green", fg="white", font=("Arial", 12), command=self.sign_up)
        signin_button.grid(row=6, column=0, columnspan=2, pady=20)

    def create_right_frame(self):
        """Create the right frame for the image."""
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load image
        image_path = r"E:\pannonia\AI lab\project\shs.jpg"  # Replace with your image file
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Create label for image
        self.image_label = tk.Label(self.right_frame, image=self.tk_image, bg="white")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Bind resize event
        self.right_frame.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        """Resize the image dynamically to fit the frame."""
        frame_width = event.width
        frame_height = event.height
        resized_image = self.image.resize((frame_width, frame_height))
        self.tk_resized_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_resized_image)
        self.image_label.image = self.tk_resized_image  # Keep a reference to avoid garbage collection

    def sign_up(self):
        """Handle the sign-up logic."""
        try:
            email = self.email_entry.get()
            password = self.password_entry.get()

            # Validation
            if not email or not password:
                messagebox.showwarning("Validation Error", "All fields are required!")
                return
            # Create user in Firebase Authentication
            user = self.auth.sign_in_with_email_and_password(email, password)

            messagebox.showinfo("Success", "User registered successfully!")
        except Exception as e:
            messagebox.showerror("Firebase Error", f"Error: {e}")
            print(f"Full Error Trace: {e}")
    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

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

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SignIn(root)
    root.mainloop()
