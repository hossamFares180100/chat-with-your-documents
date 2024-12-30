import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk
from transformers import pipeline
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import threading
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#2980b9")
        self.splash_frame = tk.Frame(root, bg="#2980b9", width=800, height=600)
        self.splash_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Loading message
        self.loading_label = tk.Label(self.splash_frame, text="Loading... Please wait.", bg="#2980b9", font=("Arial", 16))
        self.loading_label.pack(pady=20)
        
        # Loading animation (just a simple text for now, but you can use an animated GIF or spinner)
        self.spinner_label = tk.Label(self.splash_frame, text="🔄", font=("Arial", 50), bg="#2980b9")
        self.spinner_label.pack(pady=20)
        
    def remove_splash(self):
        """Remove the splash screen once loading is done."""
        self.splash_frame.destroy()


class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer and Q&A System")
        self.root.geometry("800x600")
        self.color="#2980b9"
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
    
        # Splash Screen initialization
        self.splash_screen = SplashScreen(self.root)
        threading.Thread(target=self.loadModels).start()
    def loadModels(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
        self.grammar_correct = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")
        self.spelling_correct = pipeline("text2text-generation",model="oliverguhr/spelling-correction-english-base")
        # Load GPT-2 (smaller size for faster inference)
        self.gpt = pipeline("text-generation", model="gpt2", max_length=1024,truncation=True)
        self.summarizer  = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # After models are loaded, remove the splash screen and initialize main application
        self.splash_screen.remove_splash()
        self.initialize_main_app()

    def initialize_main_app(self):
        # Top frame for PDF selection
        top_frame = tk.Frame(root, bg=self.color, height=50)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        header = tk.Label(top_frame, text="Student Helper System", bg="black", fg="white", font=("Arial", 20))
        header.pack(fill=tk.X)
        pdf_button = tk.Button(top_frame, text="Select PDF", command=self.select_pdf, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
        pdf_button.pack(pady=10, padx=10, side=tk.LEFT)
        
        self.pdf_label = tk.Label(top_frame, text="No PDF selected", bg=self.color, font=("Arial", 10))
        self.pdf_label.pack(side=tk.LEFT)
        
        # PDF display frame
        pdf_frame = tk.Frame(root, bg="white")
        pdf_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(10, 10))
        
        self.pdf_canvas = tk.Canvas(pdf_frame, bg="white")
        self.pdf_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Navigation buttons
        nav_frame = tk.Frame(root, bg=self.color)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        prev_button = tk.Button(nav_frame, text="Previous", command=self.show_previous_page, bg="#00796b", fg="white", font=("Arial", 10, "bold"))
        prev_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        next_button = tk.Button(nav_frame, text="Next", command=self.show_next_page, bg="#00796b", fg="white", font=("Arial", 10, "bold"))
        next_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Q&A section
        qa_frame = tk.Frame(root, bg="#4dd0e1", width=200)
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
        pdf_reader = PdfReader(path)
        txt = ""
        for page in pdf_reader.pages:
            txt += page.extract_text()
        self.pdf_content = txt
            
    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        self.read_pdf_content(pdf_path)
        if pdf_path:
            self.pdf_label.config(text=f"Selected PDF: {pdf_path}")
            self.load_pdf(pdf_path)
            self.chuncks=None
            self.vectorStore=None
    def load_pdf(self, path):
        # Convert PDF pages to images
        self.pdf_images = convert_from_path(path, dpi=100)
        self.current_page = 0
        self.show_page(self.current_page)
        
    def show_page(self, page_num):
        if 0 <= page_num < len(self.pdf_images):
            self.current_page = page_num
            img = self.pdf_images[page_num]
            
            # Resize image to fit canvas using the new Resampling.LANCZOS
            img = img.resize((self.pdf_canvas.winfo_width(), self.pdf_canvas.winfo_height()), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            
            # Display image on canvas
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
            # Disable the button to prevent multiple clicks
            self.answer_button.config(state="disabled")
            # Start a thread to process the answer so UI doesn't freeze
            threading.Thread(target=self.get_answer_fromPDF, args=(question,)).start()
            # Placeholder for answer generation
            #self.answer_text.set(self.get_answer_fromPDF(question))
        else:
            messagebox.showwarning("Input Required", "Please enter a question.")
    
    def correctGrammarAndSpelling(self,question):
        question = self.spelling_correct(question)[0]["generated_text"]
        result = self.grammar_correct(question)
        print(result[0]['generated_text'])
        return result[0]['generated_text']

        
        # Function to detect the language of a text
    def detect_language(self,text):
        return detect(text)

        # Load Translation Models
    def load_translation_model(self,src_lang, target_lang="en"):
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{target_lang}"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        return model, tokenizer
    
    def translate(self,text, model, tokenizer):
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    
    # Function to detect and translate language
    def process_translation(self,text):
        # Translate question to English
        self.que_lan = self.detect_language(text)
        if self.que_lan != "en":
            translation_model, translation_tokenizer = self.load_translation_model(self.que_lan, "en")
            translated_text = self.translate(text, translation_model, translation_tokenizer)
        else:
            translated_text = text
        return translated_text
    
    def translation_back(self,answer_in_english):
        # Answer in English (as per your existing process)
        #answer_in_english = "The capital of France is Paris"
        
        # Translate the answer back to the original language
        #lan = self.detect_language(answer_in_english)
        if self.que_lan!="en":
            translation_model_reverse, translation_tokenizer_reverse = self.load_translation_model("en", self.que_lan)
            translated_answer = "answer in english: "+answer_in_english+"\nanwer in "+self.que_lan+": " +self.translate(answer_in_english, translation_model_reverse, translation_tokenizer_reverse)
        else:
            translated_answer = answer_in_english
        return translated_answer
    
    def clean_and_summarize(self,content):
        """
        Cleans up the extracted text, removes unnecessary symbols, and summarizes the content.
        """
        # Cleaning up the text
        cleaned_content = content.replace("\\n", " ").replace("\\", "").strip()
        
        # Summarizing the cleaned content
        summary = self.summarizer(cleaned_content, max_length=150, min_length=40, do_sample=False)
        return summary[0]["summary_text"]

# Run the application
root = tk.Tk()
app = PDFViewerApp(root)
root.mainloop()
