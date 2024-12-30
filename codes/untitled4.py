import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class PDFSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Summarizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4c3")
        
        # Top Frame for selecting PDF
        top_frame = tk.Frame(root, bg="#9ccc65", height=60)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        
        pdf_button = tk.Button(top_frame, text="Select PDF", command=self.select_pdf, bg="#558b2f", fg="white", font=("Arial", 12, "bold"))
        pdf_button.pack(pady=15, padx=15, side=tk.LEFT)
        
        self.pdf_label = tk.Label(top_frame, text="No PDF selected", bg="#9ccc65", font=("Arial", 10, "italic"))
        self.pdf_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Summarization area
        summarize_frame = tk.Frame(root, bg="#c5e1a5")
        summarize_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        summarize_button = tk.Button(summarize_frame, text="Summarize", command=self.summarize_pdf, bg="#33691e", fg="white", font=("Arial", 12, "bold"))
        summarize_button.pack(pady=10)
        
        # Scrolled text box to display summary
        self.summary_box = scrolledtext.ScrolledText(summarize_frame, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", fg="#1b5e20", padx=10, pady=10, relief=tk.FLAT)
        self.summary_box.pack(fill=tk.BOTH, expand=True)
        self.summary_box.insert(tk.END, "Summary will appear here...")
        self.summary_box.config(state="disabled")  # Start in read-only mode
        
    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            self.pdf_label.config(text=f"Selected PDF: {pdf_path}")
            self.pdf_path = pdf_path
        else:
            self.pdf_label.config(text="No PDF selected")
        
    def summarize_pdf(self):
        if hasattr(self, 'pdf_path'):
            # Placeholder for summarization logic
            summary_text = f"Summarized text of PDF at {self.pdf_path}."
            
            # Display the summary in the summary box
            self.display_summary(summary_text)
        else:
            messagebox.showwarning("No PDF Selected", "Please select a PDF file first.")
    
    def display_summary(self, summary_text):
        self.summary_box.config(state="normal")  # Enable editing
        self.summary_box.delete("1.0", tk.END)  # Clear existing text
        self.summary_box.insert(tk.END, summary_text)
        self.summary_box.config(state="disabled")  # Disable editing again

# Run the application
root = tk.Tk()
app = PDFSummarizerApp(root)
root.mainloop()
