import tkinter as tk
from tkinter import ttk, messagebox,filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from PIL import Image, ImageTk


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Helper System")
        self.root.geometry("800x600")
        self.color = "#2980b9"
        self.root.configure(bg=self.color)

        # GUI Components
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
        
        
        # Load image
        image_path = r"E:\pannonia\AI lab\project\egyetemi-logo.jpg"  # Replace with your image file
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Create label for image
        self.image_label = tk.Label(self.left_frame, image=self.tk_image, bg="#2980b9")
        self.image_label.grid(row=0, column=0,columnspan=(2), sticky="nsew",pady=20)

        resized_image = self.image.resize((200, 200))
        self.tk_resized_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_resized_image)
        self.image_label.image = self.tk_resized_image  # Keep a reference to avoid garbage collection

        tk.Button(self.left_frame, text="PDF QA", bg=self.color,fg="#ffffff",padx=30, font=("Arial", 12)).grid(row=2, column=0,padx=10, sticky="w")
        tk.Button(self.left_frame, text="PDF simplification", bg=self.color,fg="#ffffff", font=("Arial", 12)).grid(row=2, column=1,padx=10, sticky="w")


   

    def create_right_frame(self):
        """Create the right frame for the GIF."""
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load GIF
        gif_path = r"E:\pannonia\AI lab\project\Quality Assurance.gif"  # Replace with your GIF file
        self.original_gif = Image.open(gif_path)

        # Extract frames
        self.frames = []
        try:
            while True:
                frame = self.original_gif.copy()
                self.frames.append(frame)
                self.original_gif.seek(self.original_gif.tell() + 1)
        except EOFError:
            pass  # End of GIF frames

        # Create label for GIF
        self.image_label = tk.Label(self.right_frame, bg="white")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Start animation
        self.current_frame = 0
        self.resized_frames = []  # Store resized frames for dynamic resizing
        self.animate_gif()

        # Bind resize event
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
        if self.resized_frames:  # Use resized frames if available
            frame = self.resized_frames[self.current_frame]
            self.image_label.config(image=frame)
        elif self.frames:  # Fallback to original frames if not resized yet
            frame = ImageTk.PhotoImage(self.frames[self.current_frame])
            self.image_label.config(image=frame)

        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(30, self.animate_gif)  # Adjust timing as needed    
            

    def open_new_window(self,window):
         root=tk.Tk()
         obj=window(root)
         root.mainloop() 
         
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
