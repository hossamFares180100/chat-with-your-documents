import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tkinter.scrolledtext import ScrolledText

# Load T5 model and tokenizer
model_name = "t5-small"  # Use a fine-tuned simplification model if available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function to simplify text chunk
def simplify_text(text, max_length=150):
    input_text = f"Simplify for a beginner audience: {text}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=0.9,
        top_p=0.85,
        num_beams=3,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to split text into chunks
def chunk_text(text, chunk_size=400):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n".join(pages)

# Process and simplify large PDF content
def simplify_large_pdf(pdf_path):
    # Step 1: Extract text
    raw_text = extract_text_from_pdf(pdf_path)
    print("Extracted text from PDF.")

    # Step 2: Chunk and simplify text
    simplified_chunks = []
    for chunk in chunk_text(raw_text):
        simplified_chunk = simplify_text(chunk)
        simplified_chunks.append(simplified_chunk)

    # Step 3: Combine simplified chunks
    simplified_text = "\n".join(simplified_chunks)
    print("Simplified text processing complete.")
    return raw_text, simplified_text

# Tkinter GUI Application
class PDFSimplifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Simplifier")
        self.root.geometry("1000x600")  # Set window size

        # Add padding to the window for better appearance
        self.root.config(padx=20, pady=20)

        # Top Frame for File Selection Button
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", padx=10, pady=10)

        self.load_button = tk.Button(self.top_frame, text="Select PDF", command=self.load_pdf, width=20, height=2, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.load_button.pack(pady=10)

        # Frame to hold left and right panels for displaying content
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side="top", fill="both", expand=True)

        # Left Frame (Original PDF content)
        self.left_frame = tk.Frame(self.content_frame, width=500, height=600)
        self.left_frame.pack(side="left", padx=10, pady=10, fill="y")

        self.original_text_box = ScrolledText(self.left_frame, wrap=tk.WORD, width=60, height=25, font=("Arial", 12))
        self.original_text_box.pack(padx=10, pady=10)

        # Right Frame (Simplified PDF content)
        self.right_frame = tk.Frame(self.content_frame, width=500, height=600)
        self.right_frame.pack(side="right", padx=10, pady=10, fill="y")

        self.simplified_text_box = ScrolledText(self.right_frame, wrap=tk.WORD, width=60, height=25, font=("Arial", 12))
        self.simplified_text_box.pack(padx=10, pady=10)

    def load_pdf(self):
        # Open file dialog to select PDF
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        
        if pdf_path:
            try:
                # Simplify the PDF content
                original_text, simplified_text = simplify_large_pdf(pdf_path)

                # Display the original and simplified texts in the respective text boxes
                self.original_text_box.delete(1.0, tk.END)
                self.original_text_box.insert(tk.END, original_text)

                self.simplified_text_box.delete(1.0, tk.END)
                self.simplified_text_box.insert(tk.END, simplified_text)

                # Inform the user
                messagebox.showinfo("Success", "PDF processed and simplified successfully.")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while processing the PDF: {str(e)}")

# Initialize and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSimplifierApp(root)
    root.mainloop()
