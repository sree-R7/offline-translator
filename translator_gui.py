#!/usr/bin/env python3
"""
Offline English-Spanish Translator GUI Using Tkinter 
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from languagemodel import run_translation

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline English ↔ Spanish Translator")
        self.root.geometry("800x600")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Set up the main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Offline Translation Tool", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Left side - Input
        input_frame = ttk.LabelFrame(main_frame, text="Input Text", padding="5")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, 
                                                     width=35, height=20,
                                                     font=('Arial', 11))
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Middle - Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=1, sticky=(tk.N, tk.S), padx=10, pady=50)
        
        # Translation direction
        direction_label = ttk.Label(control_frame, text="Direction:", 
                                   font=('Arial', 10, 'bold'))
        direction_label.grid(row=0, column=0, pady=(0, 5))
        
        self.direction_var = tk.StringVar(value="EN→ES")
        
        ttk.Radiobutton(control_frame, text="English → Spanish", 
                       variable=self.direction_var, value="EN→ES").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(control_frame, text="Spanish → English", 
                       variable=self.direction_var, value="ES→EN").grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Translate button
        self.translate_btn = ttk.Button(control_frame, text="Translate →", 
                                       command=self.translate,
                                       style='Accent.TButton')
        self.translate_btn.grid(row=3, column=0, pady=20)
        
        # Clear buttons
        ttk.Button(control_frame, text="Clear Input", 
                  command=self.clear_input).grid(row=4, column=0, pady=2)
        ttk.Button(control_frame, text="Clear Output", 
                  command=self.clear_output).grid(row=5, column=0, pady=2)
        ttk.Button(control_frame, text="Clear Both", 
                  command=self.clear_both).grid(row=6, column=0, pady=2)
        
        # Copy button
        ttk.Button(control_frame, text="Copy Output", 
                  command=self.copy_output).grid(row=7, column=0, pady=20)
        
        # Right side - Output
        output_frame = ttk.LabelFrame(main_frame, text="Translated Text", padding="5")
        output_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                      width=35, height=20,
                                                      font=('Arial', 11))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure button style
        style.configure('Accent.TButton', font=('Arial', 11, 'bold'))
        
        # Bind keyboard shortcuts
        root.bind('<Control-Return>', lambda e: self.translate())
        root.bind('<Control-t>', lambda e: self.translate())
        root.bind('<Control-l>', lambda e: self.clear_both())
        
        # Initialize models in background
        self.init_models()
        
    def init_models(self):
        """Initialize models in a background thread"""
        def load():
            self.status_var.set("Loading models... This may take a moment on first run.")
            try:
                # Do a dummy translation to load models
                _ = run_translation("test", "E")
                _ = run_translation("test", "S")
                self.status_var.set("Ready - Models loaded successfully")
            except Exception as e:
                self.status_var.set(f"Error loading models: {str(e)}")
                messagebox.showerror("Model Loading Error", 
                                   f"Failed to load translation models:\n{str(e)}")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def translate(self):
        """Perform translation"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("No Input", "Please enter text to translate.")
            return
        
        # Determine target language
        direction = self.direction_var.get()
        target_lang = "S" if direction == "EN→ES" else "E"
        
        # Disable button and show status
        self.translate_btn.config(state='disabled')
        self.status_var.set("Translating...")
        
        # Perform translation in background thread
        def do_translation():
            try:
                translated = run_translation(input_text, target_lang)
                
                # Update UI in main thread
                self.root.after(0, self._update_output, translated)
            except Exception as e:
                self.root.after(0, self._show_error, str(e))
        
        thread = threading.Thread(target=do_translation, daemon=True)
        thread.start()
    
    def _update_output(self, translated_text):
        """Update output text (called in main thread)"""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", translated_text)
        self.translate_btn.config(state='normal')
        self.status_var.set("Translation complete")
    
    def _show_error(self, error_msg):
        """Show error message (called in main thread)"""
        messagebox.showerror("Translation Error", f"Translation failed:\n{error_msg}")
        self.translate_btn.config(state='normal')
        self.status_var.set("Translation failed")
    
    def clear_input(self):
        """Clear input text"""
        self.input_text.delete("1.0", tk.END)
        self.status_var.set("Input cleared")
    
    def clear_output(self):
        """Clear output text"""
        self.output_text.delete("1.0", tk.END)
        self.status_var.set("Output cleared")
    
    def clear_both(self):
        """Clear both input and output"""
        self.clear_input()
        self.clear_output()
        self.status_var.set("All text cleared")
    
    def copy_output(self):
        """Copy output text to clipboard"""
        output = self.output_text.get("1.0", tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            self.status_var.set("Output copied to clipboard")
        else:
            messagebox.showinfo("Nothing to Copy", "Output is empty.")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
