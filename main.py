import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from rembg import remove


class RembgGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("BackGround Remover")
    self.root.geometry("780x620")
    self.root.resizable(False, False)

    self.BG_DARK = "#121212"          
    self.FRAME_BG = "#1E1E1E"         
    self.TEXT_COLOR = "#E0E0E0"       
    self.TEXT_MUTED = "#888888"       
    self.ACCENT_COLOR = "#007AFF"    
    self.ACCENT_HOVER = "#005BB5"     
    self.SUCCESS_COLOR = "#34C759"    
    self.SUCCESS_HOVER = "#248A3D"    
    self.DISABLED_BG = "#333333"      
    self.DISABLED_FG = "#666666"     

    self.root.configure(bg=self.BG_DARK)

    self.input_path = None
    self.output_img = None

    title_label = tk.Label(
        root,
        text="Background Remover Pro",
        font=("Segoe UI", 20, "bold"),
        fg=self.TEXT_COLOR,
        bg=self.BG_DARK,
    )
    title_label.pack(pady=(20, 15))

    top_frame = tk.Frame(root, bg=self.BG_DARK)
    top_frame.pack(fill="x", padx=30, pady=5)

    self.btn_select = tk.Button(
        top_frame,
        text="📂 Choose Image",
        font=("Segoe UI", 10, "bold"),
        bg=self.ACCENT_COLOR,
        fg="white",
        activebackground=self.ACCENT_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8,
        command=self.select_image,
    )
    self.btn_select.pack(side="left")

    self.lbl_path = tk.Label(
        top_frame,
        text="No file selected...",
        font=("Segoe UI", 10),
        fg=self.TEXT_MUTED,
        bg=self.BG_DARK,
    )
    self.lbl_path.pack(side="left", padx=15)

    preview_container = tk.Frame(root, bg=self.BG_DARK)
    preview_container.pack(fill="both", expand=True, padx=30, pady=15)

    orig_card = tk.LabelFrame(
        preview_container,
        text=" Original Image ",
        font=("Segoe UI", 10, "bold"),
        fg=self.TEXT_COLOR,
        bg=self.FRAME_BG,
        bd=1,
        relief="solid",
    )
    orig_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    self.lbl_orig = tk.Label(
        orig_card,
        text="Image preview will appear here",
        font=("Segoe UI", 10),
        fg=self.TEXT_MUTED,
        bg=self.FRAME_BG,
    )
    self.lbl_orig.pack(expand=True, fill="both", padx=10, pady=10)

    result_card = tk.LabelFrame(
        preview_container,
        text=" Processed Result ",
        font=("Segoe UI", 10, "bold"),
        fg=self.TEXT_COLOR,
        bg=self.FRAME_BG,
        bd=1,
        relief="solid",
    )
    result_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    self.lbl_result = tk.Label(
        result_card,
        text="Result will appear here",
        font=("Segoe UI", 10),
        fg=self.TEXT_MUTED,
        bg=self.FRAME_BG,
    )
    self.lbl_result.pack(expand=True, fill="both", padx=10, pady=10)

    preview_container.grid_columnconfigure(0, weight=1)
    preview_container.grid_columnconfigure(1, weight=1)
    preview_container.grid_rowconfigure(0, weight=1)

    self.lbl_status = tk.Label(
        root,
        text="Ready. Please select an image to begin.",
        font=("Segoe UI", 10),
        fg=self.TEXT_MUTED,
        bg=self.BG_DARK,
    )
    self.lbl_status.pack(pady=5)

    bottom_frame = tk.Frame(root, bg=self.BG_DARK)
    bottom_frame.pack(fill="x", padx=30, pady=(10, 25))

    self.btn_remove = tk.Button(
        bottom_frame,
        text="✨ Remove Background",
        font=("Segoe UI", 11, "bold"),
        bg=self.DISABLED_BG,
        fg=self.DISABLED_FG,
        activebackground=self.ACCENT_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        pady=10,
        state="disabled",
        command=self.start_removal_thread,
    )
    self.btn_remove.pack(side="left", expand=True, fill="x", padx=(0, 10))

    self.btn_save = tk.Button(
        bottom_frame,
        text="💾 Save Result",
        font=("Segoe UI", 11, "bold"),
        bg=self.DISABLED_BG,
        fg=self.DISABLED_FG,
        activebackground=self.SUCCESS_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        pady=10,
        state="disabled",
        command=self.save_image,
    )
    self.btn_save.pack(side="right", expand=True, fill="x", padx=(10, 0))

  def select_image(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp *.bmp")]
    )

    if file_path:
      self.input_path = file_path
      
      display_name = os.path.basename(file_path)
      if len(display_name) > 30:
          display_name = display_name[:27] + "..."
          
      self.lbl_path.config(text=display_name, fg=self.TEXT_COLOR)

      img = Image.open(file_path)
      img.thumbnail((260, 260))
      self.tk_orig = ImageTk.PhotoImage(img)
      self.lbl_orig.config(image=self.tk_orig, text="")

      self.lbl_result.config(image="", text="Awaiting processing...")

      self.btn_remove.config(state="normal", bg=self.ACCENT_COLOR, fg="white")
      self.btn_save.config(state="disabled", bg=self.DISABLED_BG, fg=self.DISABLED_FG)
      self.lbl_status.config(
          text="Image loaded successfully. Ready to process.", fg=self.TEXT_COLOR
      )

  def start_removal_thread(self):
    self.btn_remove.config(state="disabled", bg=self.DISABLED_BG, fg=self.DISABLED_FG)
    self.btn_select.config(state="disabled", bg=self.DISABLED_BG, fg="white")
    
    self.lbl_status.config(
        text="⏳ Removing background, please wait...", fg="#5AC8FA" 
    )

    threading.Thread(target=self.process_background_removal).start()

  def process_background_removal(self):
    try:
      orig_img = Image.open(self.input_path)
      self.output_img = remove(orig_img)
      self.root.after(0, self.on_removal_complete)
    except Exception as e:
      self.root.after(0, lambda: self.on_removal_error(str(e)))

  def on_removal_complete(self):
    # Preview Output Image
    preview_img = self.output_img.copy()
    preview_img.thumbnail((260, 260))
    self.tk_result = ImageTk.PhotoImage(preview_img)

    self.lbl_result.config(image=self.tk_result, text="")
    
    self.lbl_status.config(
        text="✔ Background removed successfully!", fg=self.SUCCESS_COLOR
    )

    self.btn_select.config(state="normal", bg=self.ACCENT_COLOR, fg="white")
    self.btn_remove.config(state="normal", bg=self.ACCENT_COLOR, fg="white")
    self.btn_save.config(state="normal", bg=self.SUCCESS_COLOR, fg="white")

  def on_removal_error(self, err_msg):
    self.btn_select.config(state="normal", bg=self.ACCENT_COLOR, fg="white")
    self.btn_remove.config(state="normal", bg=self.ACCENT_COLOR, fg="white")
    
    self.lbl_status.config(text="✖ Error occurred during processing.", fg="#FF3B30")
    messagebox.showerror("Error", f"Failed to remove background:\n{err_msg}")

  def save_image(self):
    if self.output_img:
      save_path = filedialog.asksaveasfilename(
          defaultextension=".png",
          filetypes=[("PNG Image", "*.png")],
          initialfile="processed_image.png",
      )
      if save_path:
        self.output_img.save(save_path)
        messagebox.showinfo("Success", "Image saved successfully!")
        self.lbl_status.config(text=f"✔ Saved to: {os.path.basename(save_path)}", fg=self.SUCCESS_COLOR)


if __name__ == "__main__":
  root = tk.Tk()
  app = RembgGUI(root)
  root.mainloop()