import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class SecretCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("420x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a1a")
        
        # Calculator state
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Secret mode state
        self.secret_mode = False
        self.secret_sequence = ""
        self.secret_code = "7355608"
        
        # Create main container with scrollbar
        self.main_canvas = tk.Canvas(self.root, bg="#1a1a1a", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#1a1a1a")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.canvas_frame = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Make scrollable frame expand to canvas width
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Create UI
        self.create_calculator_ui()
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_canvas_configure(self, event):
        """Make the scrollable frame match canvas width"""
        self.main_canvas.itemconfig(self.canvas_frame, width=event.width)
        
    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_calculator_ui(self):
        """Create the main calculator interface"""
        # Display frame
        display_frame = tk.Frame(self.scrollable_frame, bg="#2b2b2b", pady=15)
        display_frame.pack(fill="x", padx=0)
        
        # Result display
        self.display = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            font=("Arial", 28, "bold"),
            justify="right",
            bd=0,
            bg="#2b2b2b",
            fg="white",
            state="readonly"
        )
        self.display.pack(fill="both", padx=25, pady=10)
        
        # Secret mode indicator
        self.mode_label = tk.Label(
            display_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg="#2b2b2b",
            fg="#00ff00"
        )
        self.mode_label.pack(pady=3)
        
        # Instruction label
        self.hint_label = tk.Label(
            display_frame,
            text="Hint: Try entering 7355608",
            font=("Arial", 8, "italic"),
            bg="#2b2b2b",
            fg="#666666"
        )
        self.hint_label.pack(pady=(0, 5))
        
        # Button frame with fixed height
        button_frame = tk.Frame(self.scrollable_frame, bg="#1a1a1a")
        button_frame.pack(fill="both", padx=15, pady=(10, 15))
        
        # Button layout for calculator
        buttons = [
            ['C', '←', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '']
        ]
        
        # Create buttons with better sizing
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if btn_text:
                    btn = tk.Button(
                        button_frame,
                        text=btn_text,
                        font=("Arial", 20, "bold"),
                        bg="#404040",
                        fg="white",
                        activebackground="#505050",
                        activeforeground="white",
                        bd=0,
                        command=lambda x=btn_text: self.button_click(x),
                        relief="flat",
                        cursor="hand2"
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=3, pady=3, ipady=10)
                    
                    if btn_text in ['/', '*', '-', '+', '=']:
                        btn.config(bg="#ff9500")
                    elif btn_text in ['C', '←']:
                        btn.config(bg="#a0a0a0", fg="black")
        
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
        
        # Create secret converter UI
        self.create_converter_ui()
        
    def create_converter_ui(self):
        """Create the hidden base converter interface"""
        self.converter_frame = tk.Frame(self.scrollable_frame, bg="#0a0a0a", relief="solid", bd=2)
        
        # Title with better styling
        title = tk.Label(
            self.converter_frame,
            text="🔐 SECRET BASE CONVERTER 🔐",
            font=("Arial", 13, "bold"),
            bg="#00ff00",
            fg="black",
            pady=12
        )
        title.pack(fill="x", pady=0)
        
        # Main content with padding
        content_frame = tk.Frame(self.converter_frame, bg="#0a0a0a")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Conversion type selector
        conv_container = tk.LabelFrame(
            content_frame,
            text="Conversion Type",
            font=("Arial", 10, "bold"),
            bg="#2b2b2b",
            fg="white",
            padx=12,
            pady=10
        )
        conv_container.pack(pady=(0, 12), fill="x")
        
        self.conversion_type = tk.StringVar(value="dec_to_bin")
        conversions = [
            ("Decimal → Binary", "dec_to_bin"),
            ("Binary → Hexadecimal", "bin_to_hex"),
            ("Hexadecimal → Binary", "hex_to_bin")
        ]
        
        for text, value in conversions:
            rb = tk.Radiobutton(
                conv_container,
                text=text,
                variable=self.conversion_type,
                value=value,
                font=("Arial", 10),
                bg="#2b2b2b",
                fg="white",
                selectcolor="#404040",
                activebackground="#2b2b2b",
                activeforeground="white",
                cursor="hand2"
            )
            rb.pack(anchor="w", pady=2)
        
        # Input section
        input_container = tk.LabelFrame(
            content_frame,
            text="Input Number",
            font=("Arial", 10, "bold"),
            bg="#2b2b2b",
            fg="#ffff00",
            padx=12,
            pady=10
        )
        input_container.pack(pady=(0, 12), fill="x")
        
        self.convert_input = tk.Entry(
            input_container,
            font=("Arial", 15),
            bg="#404040",
            fg="white",
            insertbackground="white",
            bd=2,
            relief="sunken"
        )
        self.convert_input.pack(fill="x", ipady=6)
        
        # Convert button with arrow
        btn_frame = tk.Frame(content_frame, bg="#0a0a0a")
        btn_frame.pack(pady=(5, 12), fill="x")
        
        tk.Label(
            btn_frame,
            text="👇 CLICK TO CONVERT 👇",
            font=("Arial", 9, "bold"),
            bg="#0a0a0a",
            fg="#ffff00"
        ).pack(pady=(0, 5))
        
        convert_btn = tk.Button(
            btn_frame,
            text="🔥 CONVERT NOW 🔥",
            font=("Arial", 13, "bold"),
            bg="#00ff00",
            fg="black",
            activebackground="#00cc00",
            activeforeground="black",
            command=self.perform_conversion,
            cursor="hand2",
            relief="raised",
            bd=3,
            height=2
        )
        convert_btn.pack(fill="x")
        
        # Output section
        output_container = tk.LabelFrame(
            content_frame,
            text="Result",
            font=("Arial", 10, "bold"),
            bg="#2b2b2b",
            fg="#00ff00",
            padx=12,
            pady=10
        )
        output_container.pack(pady=(0, 12), fill="x")
        
        # Output display
        self.convert_output = tk.Text(
            output_container,
            font=("Courier New", 16, "bold"),
            bg="#000000",
            fg="#00ff00",
            height=2,
            wrap="word",
            bd=2,
            relief="sunken",
            state="disabled"
        )
        self.convert_output.pack(fill="x")
        
        # Result indicator
        self.result_indicator = tk.Label(
            output_container,
            text="",
            font=("Arial", 9, "bold"),
            bg="#2b2b2b",
            fg="#ffff00"
        )
        self.result_indicator.pack(pady=(5, 0))
        
        # Exit button
        exit_btn = tk.Button(
            content_frame,
            text="❌ Close Secret Mode",
            font=("Arial", 10, "bold"),
            bg="#ff3333",
            fg="white",
            activebackground="#cc0000",
            activeforeground="white",
            command=self.toggle_secret_mode,
            cursor="hand2",
            height=2,
            relief="raised",
            bd=2
        )
        exit_btn.pack(pady=(5, 0), fill="x")
    
    def button_click(self, value):
        """Handle button clicks"""
        if value.isdigit():
            self.secret_sequence += value
            if len(self.secret_sequence) > 7:
                self.secret_sequence = self.secret_sequence[-7:]
            
            if self.secret_sequence == self.secret_code:
                self.toggle_secret_mode()
                self.secret_sequence = ""
                return
        
        if value == 'C':
            self.clear()
        elif value == '←':
            self.backspace()
        elif value == '=':
            self.calculate()
        else:
            self.append_input(value)
    
    def append_input(self, value):
        self.current_input += str(value)
        self.result_var.set(self.current_input)
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("0")
        self.secret_sequence = ""
    
    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.result_var.set(self.current_input if self.current_input else "0")
    
    def calculate(self):
        try:
            result = eval(self.current_input)
            self.result_var.set(str(result))
            self.current_input = str(result)
        except Exception:
            self.result_var.set("Error")
            self.current_input = ""
    
    def toggle_secret_mode(self):
        """Toggle secret mode"""
        self.secret_mode = not self.secret_mode
        
        if self.secret_mode:
            self.converter_frame.pack(fill="both", padx=15, pady=(0, 15))
            self.mode_label.config(text="🔓 SECRET MODE ACTIVATED!")
            self.hint_label.config(text="")
            self.clear()
            # Scroll to show converter
            self.root.after(100, lambda: self.main_canvas.yview_moveto(1.0))
        else:
            self.converter_frame.pack_forget()
            self.mode_label.config(text="")
            self.hint_label.config(text="Hint: Try entering 7355608")
            self.convert_input.delete(0, tk.END)
            self.convert_output.config(state="normal")
            self.convert_output.delete(1.0, tk.END)
            self.convert_output.config(state="disabled")
            self.result_indicator.config(text="")
            self.root.after(100, lambda: self.main_canvas.yview_moveto(0))
    
    def perform_conversion(self):
        """Perform base conversion"""
        input_value = self.convert_input.get().strip()
        
        if not input_value:
            messagebox.showwarning("No Input", "Please enter a number to convert!")
            return
        
        conv_type = self.conversion_type.get()
        
        try:
            if conv_type == "dec_to_bin":
                decimal = int(input_value, 10)
                result = bin(decimal)[2:]
                
            elif conv_type == "bin_to_hex":
                decimal = int(input_value, 2)
                result = hex(decimal)[2:].upper()
                
            elif conv_type == "hex_to_bin":
                decimal = int(input_value, 16)
                result = bin(decimal)[2:]
            
            # Display result
            self.convert_output.config(state="normal")
            self.convert_output.delete(1.0, tk.END)
            self.convert_output.insert(1.0, f"\n  ➜  {result}")
            self.convert_output.config(state="disabled")
            
            # Show indicator
            self.result_indicator.config(text="✅ Conversion Complete!")
            
            # Flash effect
            self.flash_output()
            
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                f"Please enter a valid {conv_type.split('_')[0].upper()} number."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Conversion error: {str(e)}")
    
    def flash_output(self):
        """Flash the output"""
        original_bg = self.convert_output.cget("bg")
        self.convert_output.config(bg="#00ff00")
        self.root.after(150, lambda: self.convert_output.config(bg=original_bg))

def main():
    root = tk.Tk()
    app = SecretCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()