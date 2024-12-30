import tkinter as tk
from tkinter import messagebox,filedialog
from tkcalendar import Calendar
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from transformers import pipeline
#from PyPDF2 import PdfReader
#import pymupdf
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import threading
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

class SignIn:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper System")
        self.root.geometry("1000x750+0+0")
        self.color = "#2980b9"
        self.root.configure(bg=self.color)
        #self.root.attributes('-fullscreen', True)
        #width= self.root.winfo_screenwidth()               
        #height= self.root.winfo_screenheight()               
        #self.root.geometry("%dx%d" % (width/2, height/2))


        self.initialize_firebase()

        self.create_header()
        self.create_left_frame()
        self.create_right_frame()

    def initialize_firebase(self):
        """Initialize Firebase."""
        service_account_key_path = "serviceAccountKey.json"
        cred = credentials.Certificate(service_account_key_path)
        try:
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print("Firebase already initialized.")

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

        image_path = r"egyetemi-logo.jpg"  # Replace with your image file
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.left_frame, image=self.tk_image, bg="#2980b9")
        self.image_label.grid(row=0, column=1, sticky="nsew",pady=20)

        resized_image = self.image.resize((200, 200))
        self.tk_resized_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_resized_image)
        self.image_label.image = self.tk_resized_image  

        tk.Label(self.left_frame, text="Email", bg=self.color, font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.email_entry = tk.Entry(self.left_frame, width=30)
        self.email_entry.grid(row=1, column=1)

        tk.Label(self.left_frame, text="Password", bg=self.color, font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self.left_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1)
        
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.left_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#2980b9", fg="white", font=("Helvetica", 12)).grid(row=2, column=2)

        self.text_button = tk.Label(self.left_frame, text="don't have an account?SignUp", fg="white",bg="#2980b9", cursor="hand2")
        self.text_button.grid(row=3, column=1)

        self.text_button.bind("<Button-1>", lambda event: self.open_new_window(SignUp))

        signin_button = tk.Button(self.left_frame, text="Sign In", bg="green", fg="white", font=("Arial", 12), command=self.sign_in)
        signin_button.grid(row=6, column=0, columnspan=2, pady=20)

    def create_right_frame(self):
        """Create the right frame for the image."""
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        image_path = r"shs.jpg"  
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.right_frame, image=self.tk_image, bg="white")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        self.right_frame.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        """Resize the image dynamically to fit the frame."""
        frame_width = event.width
        frame_height = event.height
        resized_image = self.image.resize((frame_width, frame_height))
        self.tk_resized_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_resized_image)
        self.image_label.image = self.tk_resized_image  

    def sign_in(self):
        """Handle the sign-up logic."""
        try:
            email = self.email_entry.get()
            password = self.password_entry.get()

            if not email or not password:
                messagebox.showwarning("Validation Error", "All fields are required!")
                return
            user = self.auth.sign_in_with_email_and_password(email, password)

            messagebox.showinfo("Success", "signIn successfully!")

            self.open_new_window(Dashboard)
        except Exception as e:
            messagebox.showerror("Firebase Error", f"Error: {e}")
            print(f"Full Error Trace: {e}")
    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def open_new_window(self,window):
         self.root.destroy()
         root=tk.Tk()
         obj=window(root)
         root.mainloop() 
         print("new window")


class SignUp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper System")
        self.root.geometry("1000x750+0+0")
        self.color = "#2980b9"
        self.root.configure(bg=self.color)
        #self.root.attributes('-fullscreen', True)
        self.initialize_firebase()

        self.create_header()
        self.create_left_frame()
        self.create_right_frame()

    def initialize_firebase(self):
        """Initialize Firebase."""
        service_account_key_path = "serviceAccountKey.json"
        cred = credentials.Certificate(service_account_key_path)
        try:
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print("Firebase already initialized.")

        self.firestore_db = firestore.client()

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
        
        self.text_button = tk.Label(self.left_frame, text="already have an account?SignIn", fg="white",bg="#2980b9", cursor="hand2")
        self.text_button.grid(row=7, column=0)

        self.text_button.bind("<Button-1>", lambda event: self.on_click(SignIn))


    def create_right_frame(self):
        """Create the right frame for the image."""
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        image_path = r"shs_signup.jpg"  
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.right_frame, image=self.tk_image, bg="white")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        self.right_frame.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        """Resize the image dynamically to fit the frame."""
        frame_width = event.width
        frame_height = event.height
        resized_image = self.image.resize((frame_width, frame_height))
        self.tk_resized_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_resized_image)
        self.image_label.image = self.tk_resized_image  

    def sign_up(self):
        """Handle the sign-up logic."""
        try:
            name = self.name_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            dob = self.dob_calendar.get_date()
            gender = self.gender_var.get()

            if not name or not email or not password or not confirm_password or not dob or not gender:
                messagebox.showwarning("Validation Error", "All fields are required!")
                return
            if password != confirm_password:
                messagebox.showerror("Password Error", "Passwords do not match!")
                return

            user = self.auth.create_user_with_email_and_password(email, password)

            uid = user['localId']
            self.firestore_db.collection('users').document(uid).set({
                "name": name,
                "email": email,
                "dob": dob,
                "gender": gender
            })

            messagebox.showinfo("Success", "User registered successfully!")
            self.open_new_window(Dashboard)
        except Exception as e:
            messagebox.showerror("Firebase Error", f"Error: {e}")
            print(f"Full Error Trace: {e}")
    def open_new_window(self,window):
         self.root.destroy()
         root=tk.Tk()
         obj=window(root)
         root.mainloop() 
         print("new window")
    
    def on_click(self,window):
        self.open_new_window(window)



class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper System")
        self.root.geometry("1000x750+0+0")
        self.color = "#2980b9"
        self.root.configure(bg=self.color)
        #self.root.attributes('-fullscreen', True)
        self.create_header()
        self.create_left_frame()
        self.create_right_frame()

   
    def create_header(self):
        """Create the header of the app."""
        header = tk.Label(self.root, text="Student Helper System", bg="black", fg="white", font=("Arial", 20))
        header.pack(fill=tk.X)

    def create_left_frame(self):
        """Create the left frame for the sign-up form."""
        self.left_frame = tk.Frame(self.root, bg=self.color, width=400, padx=20, pady=120)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        
        image_path = r"egyetemi-logo.jpg"  
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.left_frame, image=self.tk_image, bg="#2980b9")
        self.image_label.grid(row=0, column=0,columnspan=(2), sticky="nsew",pady=20)

        resized_image = self.image.resize((200, 200))
        self.tk_resized_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_resized_image)
        self.image_label.image = self.tk_resized_image  

        tk.Button(self.left_frame, text="PDF QA", bg=self.color,fg="#ffffff",padx=30, font=("Arial", 12),command=self.openPDFwindow).grid(row=2, column=0,padx=10, sticky="w")
        tk.Button(self.left_frame, text="PDF simplification", bg=self.color,fg="#ffffff", font=("Arial", 12)).grid(row=2, column=1,padx=10, sticky="w")


   

    def create_right_frame(self):
        """Create the right frame for the GIF."""
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        gif_path = r"Quality Assurance.gif"  
        self.original_gif = Image.open(gif_path)

        self.frames = []
        try:
            while True:
                frame = self.original_gif.copy()
                self.frames.append(frame)
                self.original_gif.seek(self.original_gif.tell() + 1)
        except EOFError:
            pass  

        self.image_label = tk.Label(self.right_frame, bg="white")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        self.current_frame = 0
        self.resized_frames = []  
        self.animate_gif()

        self.right_frame.bind("<Configure>", self.resize_frames)
     
    def resize_frames(self, event):
        """Resize frames dynamically to fit the frame."""
        frame_width = event.width
        frame_height = event.height
        self.resized_frames = [
            ImageTk.PhotoImage(frame.resize((frame_width, frame_height)))
            for frame in self.frames
        ]
        
    def animate_gif(self):
        """Animate the GIF."""
        if self.resized_frames:  
            frame = self.resized_frames[self.current_frame]
            self.image_label.config(image=frame)
        elif self.frames:  
            frame = ImageTk.PhotoImage(self.frames[self.current_frame])
            self.image_label.config(image=frame)

        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(30, self.animate_gif)  
            
    def openPDFwindow(self):
        self.root.destroy()
        root=tk.Tk()
        obj=PDFViewerApp(root)
        root.mainloop() 
   


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x750+0+0")
        #self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#2980b9")
        self.splash_frame = tk.Frame(root, bg="#2980b9", width=800, height=600)
        self.splash_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.loading_label = tk.Label(self.splash_frame, text="Loading... Please wait.", bg="#2980b9", font=("Arial", 16))
        self.loading_label.pack(pady=20)
        
        self.spinner_label = tk.Label(self.splash_frame, text="🔄", font=("Arial", 50), bg="#2980b9")
        self.spinner_label.pack(pady=20)
        
    def remove_splash(self):
        """Remove the splash screen once loading is done."""
        self.splash_frame.destroy()


class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer and Q&A System")
        self.root.geometry("1000x750+0+0")
        self.color="#2980b9"
        #self.root.attributes('-fullscreen', True)
        self.root.configure(bg=self.color)
        self.embeddings=None
        self.qa_pipeline=None
        self.gpt = None
        self.pdf_images = []
        self.current_page = 0
        self.pdf_content=""
        self.chuncks=None
        self.vectorStore=None
        self.grammar_correct = None
        self.spelling_correct = None
        self.summarizer = None
        self.que_lan="en"
    
        self.splash_screen = SplashScreen(self.root)
        threading.Thread(target=self.loadModels).start()
    def loadModels(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
        self.grammar_correct = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")
        self.spelling_correct = pipeline("text2text-generation",model="oliverguhr/spelling-correction-english-base")
        self.gpt = pipeline("text-generation", model="gpt2", max_length=1024,truncation=True)
        self.summarizer  = pipeline("summarization", model="facebook/bart-large-cnn")
        
        self.splash_screen.remove_splash()
        self.initialize_main_app()

    def initialize_main_app(self):
        top_frame = tk.Frame(self.root, bg=self.color, height=50)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        header = tk.Label(top_frame, text="Student Helper System", bg="black", fg="white", font=("Arial", 20))
        header.pack(fill=tk.X)
        pdf_button = tk.Button(top_frame, text="Select PDF", command=self.select_pdf, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
        pdf_button.pack(pady=10, padx=10, side=tk.LEFT)
        
        self.pdf_label = tk.Label(top_frame, text="No PDF selected", bg=self.color, font=("Arial", 10))
        self.pdf_label.pack(side=tk.LEFT)
        
        pdf_frame = tk.Frame(self.root, bg="white")
        pdf_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(10, 10))
        
        self.pdf_canvas = tk.Canvas(pdf_frame, bg="white")
        self.pdf_canvas.pack(fill=tk.BOTH, expand=True)
        
        nav_frame = tk.Frame(self.root, bg=self.color)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        prev_button = tk.Button(nav_frame, text="Previous", command=self.show_previous_page, bg="#00796b", fg="white", font=("Arial", 10, "bold"))
        prev_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        next_button = tk.Button(nav_frame, text="Next", command=self.show_next_page, bg="#00796b", fg="white", font=("Arial", 10, "bold"))
        next_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
        qa_frame = tk.Frame(self.root, bg="#4dd0e1", width=200)
        qa_frame.pack(fill=tk.Y, side=tk.RIGHT, padx=(0, 10), pady=10)
        
        question_label = tk.Label(qa_frame, text="Enter Question:", bg="#4dd0e1", font=("Arial", 10, "bold"))
        question_label.pack(pady=5, padx=5, anchor="w")
        
        self.question_entry = tk.Text(qa_frame, height=5, width=25, font=("Arial", 10))
        self.question_entry.pack(pady=5, padx=5)
        
        self.answer_button = tk.Button(qa_frame, text="Get Answer", command=self.get_answer, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
        self.answer_button.pack(pady=10, padx=5)
        
        self.answer_text = tk.StringVar()
        answer_label = tk.Label(qa_frame, textvariable=self.answer_text, wraplength=150, bg="#4dd0e1", font=("Arial", 10), justify="left")
        answer_label.pack(pady=5, padx=5, anchor="w")

   

    def read_pdf_content(self,path):
        with pdfplumber.open(path) as pdf:
            txt = ""
            for page in pdf.pages:
                txt += page.extract_text() 
            self.pdf_content = txt

                
        '''
        pdf_reader = PdfReader(path)
        txt = ""
        for page in pdf_reader.pages:
            txt += page.extract_text()
        self.pdf_content = txt
          '''  
    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        self.read_pdf_content(pdf_path)
        if pdf_path:
            self.pdf_label.config(text=f"Selected PDF: {pdf_path}")
            self.load_pdf(pdf_path)
            self.chuncks=None
            self.vectorStore=None
    def load_pdf(self, path):
        self.pdf_images = convert_from_path(path, dpi=100)
        self.current_page = 0
        self.show_page(self.current_page)
        
    def show_page(self, page_num):
        if 0 <= page_num < len(self.pdf_images):
            self.current_page = page_num
            img = self.pdf_images[page_num]
            
            img = img.resize((self.pdf_canvas.winfo_width(), self.pdf_canvas.winfo_height()), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            
            self.pdf_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
        
    def show_previous_page(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
        
    def show_next_page(self):
        if self.current_page < len(self.pdf_images) - 1:
            self.show_page(self.current_page + 1)
    
    def get_answer_fromPDF(self,question):
        txt_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        if self.chuncks:
            pass
        else:
            self.chunks = txt_splitter.split_text(text=self.pdf_content)    
            self.vectorStore = FAISS.from_texts(self.chunks, embedding=self.embeddings)
        docs = self.vectorStore.similarity_search(query=question, k=3)  # most three similar chunks
        answers = [self.qa_pipeline(question=question, context=doc.page_content) for doc in docs]
        prompt = (
        f"Question: {question}\n"
        f"Context: {docs}\n"
        f"Primary Answer: {answers[0]['answer']}\n"
        "Validate the answer and provide additional information if necessary."
    )
        more_details = self.gpt(prompt)
        self.answer_text.set( self.translation_back(answers[0]["answer"]))
        messagebox.showinfo("more info", self.translation_back(self.clean_and_summarize(more_details[0]["generated_text"])))
        self.answer_button.config(state="active")
            
    def get_answer(self):
        question = self.question_entry.get("1.0", tk.END).strip()
        if question:
            question = self.process_translation(question)
            question = self.correctGrammarAndSpelling(question)
            self.answer_text.set("Loading...")
            self.answer_button.config(state="disabled")
            threading.Thread(target=self.get_answer_fromPDF, args=(question,)).start()
        else:
            messagebox.showwarning("Input Required", "Please enter a question.")
    
    def correctGrammarAndSpelling(self,question):
        question = self.spelling_correct(question)[0]["generated_text"]
        result = self.grammar_correct(question)
        print(result[0]['generated_text'])
        return result[0]['generated_text']

        
    def detect_language(self,text):
        return detect(text)

    def load_translation_model(self,src_lang, target_lang="en"):
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{target_lang}"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        return model, tokenizer
    
    def translate(self,text, model, tokenizer):
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    
    def process_translation(self,text):
        self.que_lan = self.detect_language(text)
        if self.que_lan != "en":
            translation_model, translation_tokenizer = self.load_translation_model(self.que_lan, "en")
            translated_text = self.translate(text, translation_model, translation_tokenizer)
        else:
            translated_text = text
        return translated_text
    
    def translation_back(self,answer_in_english):
        if self.que_lan!="en":
            translation_model_reverse, translation_tokenizer_reverse = self.load_translation_model("en", self.que_lan)
            translated_answer = "answer in english: "+answer_in_english+"\n\n\nanwer in "+self.que_lan+": " +self.translate(answer_in_english, translation_model_reverse, translation_tokenizer_reverse)
        else:
            translated_answer = answer_in_english
        return translated_answer
    
    def clean_and_summarize(self,content):
        """
        Cleans up the extracted text, removes unnecessary symbols, and summarizes the content.
        """
        cleaned_content = content.replace("\\n", " ").replace("\\", "").strip()
        
        summary = self.summarizer(cleaned_content, max_length=150, min_length=40, do_sample=False)
        return summary[0]["summary_text"]




if __name__ == "__main__":
    root = tk.Tk()
    app = SignIn(root)
    root.mainloop()
