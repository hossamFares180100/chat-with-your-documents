import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from PIL import Image, ImageTk


class SignUp:
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

        self.firestore_db = firestore.client()

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

        tk.Label(self.left_frame, text="Name", bg=self.color, font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self.left_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.left_frame, text="Email", bg=self.color, font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.email_entry = tk.Entry(self.left_frame, width=30)
        self.email_entry.grid(row=1, column=1)

        tk.Label(self.left_frame, text="Password", bg=self.color, font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self.left_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Label(self.left_frame, text="Confirm Password", bg=self.color, font=("Arial", 12)).grid(row=3, column=0, sticky="w")
        self.confirm_password_entry = tk.Entry(self.left_frame, width=30, show="*")
        self.confirm_password_entry.grid(row=3, column=1)

        tk.Label(self.left_frame, text="Date of Birth", bg=self.color, font=("Arial", 12)).grid(row=4, column=0, sticky="w")
        self.dob_calendar = Calendar(self.left_frame, selectmode="day")
        self.dob_calendar.grid(row=4, column=1, pady=10)

        tk.Label(self.left_frame, text="Gender", bg=self.color, font=("Arial", 12)).grid(row=5, column=0, sticky="w")
        self.gender_var = tk.StringVar()
        gender_frame = tk.Frame(self.left_frame, bg=self.color)
        gender_frame.grid(row=5, column=1, sticky="w")
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male", bg=self.color).pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female", bg=self.color).pack(side=tk.LEFT)

        signup_button = tk.Button(self.left_frame, text="Sign Up", bg="green", fg="white", font=("Arial", 12), command=self.sign_up)
        signup_button.grid(row=6, column=0, columnspan=2, pady=20)

    def create_right_frame(self):
        """Create the right frame for the image."""
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load image
        image_path = r"E:\pannonia\AI lab\project\shs_signup.jpg"  # Replace with your image file
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
            name = self.name_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            dob = self.dob_calendar.get_date()
            gender = self.gender_var.get()

            # Validation
            if not name or not email or not password or not confirm_password or not dob or not gender:
                messagebox.showwarning("Validation Error", "All fields are required!")
                return
            if password != confirm_password:
                messagebox.showerror("Password Error", "Passwords do not match!")
                return

            # Create user in Firebase Authentication
            user = self.auth.create_user_with_email_and_password(email, password)

            # Save user data in Firestore
            uid = user['localId']
            self.firestore_db.collection('users').document(uid).set({
                "name": name,
                "email": email,
                "dob": dob,
                "gender": gender
            })

            messagebox.showinfo("Success", "User registered successfully!")
        except Exception as e:
            messagebox.showerror("Firebase Error", f"Error: {e}")
            print(f"Full Error Trace: {e}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SignUp(root)
    root.mainloop()
