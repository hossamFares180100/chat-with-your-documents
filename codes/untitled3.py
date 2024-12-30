import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from transformers import pipeline
from PyPDF2 import PdfReader
import threading

class PDFSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Summarizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f7f9fb")
        self.pdf_content=""
        self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")
        # Top frame for PDF selection
        top_frame = tk.Frame(root, bg="#d1e0e0", height=50)
        top_frame.pack(fill=tk.X, side=tk.TOP)

        self.pdf_label = tk.Label(top_frame, text="No PDF selected", bg="#d1e0e0", font=("Arial", 10))
        self.pdf_label.pack(side=tk.LEFT, padx=10)

        select_pdf_button = tk.Button(
            top_frame, text="Select PDF", command=self.select_pdf,
            bg="#00796b", fg="white", font=("Arial", 12, "bold")
        )
        select_pdf_button.pack(pady=10, padx=10, side=tk.RIGHT)

        # Main frame for summary display
        main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        summary_label = tk.Label(main_frame, text="Summarization", bg="white", fg="#00796b", font=("Arial", 14, "bold"))
        summary_label.pack(anchor="w", pady=(0, 10))

        # ScrolledText widget for displaying the summary
        self.summary_text = ScrolledText(main_frame, wrap=tk.WORD, font=("Arial", 12), bg="#f0f4f8", fg="#333333", height=20)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.summary_text.config(state="disabled")

        # Bottom frame for Summarize button
        bottom_frame = tk.Frame(root, bg="#d1e0e0", height=50)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        summarize_button = tk.Button(
            bottom_frame, text="Summarize", command=self.summarize_pdf,
            bg="#00796b", fg="white", font=("Arial", 12, "bold")
        )
        summarize_button.pack(pady=10, padx=10)

    def read_pdf_content(self,path):
        pdf_reader = PdfReader(path)
        txt = ""
        for page in pdf_reader.pages:
            txt += page.extract_text()
        self.pdf_content = txt
    
    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            self.pdf_label.config(text=f"Selected PDF: {pdf_path}")
            self.pdf_path = pdf_path
            self.read_pdf_content(self.pdf_path)
        else:
            self.pdf_label.config(text="No PDF selected")
            self.pdf_path = None

        
    def summarize_pdf(self):
        if not hasattr(self, 'pdf_path') or not self.pdf_path:
            messagebox.showwarning("No PDF", "Please select a PDF file to summarize.")
            return

        # Display loading message
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, "Summarizing... please wait.")
        self.summary_text.config(state="disabled")

        # Here you would call your summarization function, which takes time.
        threading.Thread(target=self.display_summary,).start()
        
        # This is a placeholder for the actual summarization processing.

    def display_summary(self):
        # Clear and display the summary in the text widget
        summary_content = self.summarizer(self.pdf_content, max_length=10000, min_length=30, do_sample=False)

        # Update summary text widget with the result
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary_content)
        self.summary_text.config(state="normal")
    

# Run the application
root = tk.Tk()
app = PDFSummarizerApp(root)
root.mainloop()
