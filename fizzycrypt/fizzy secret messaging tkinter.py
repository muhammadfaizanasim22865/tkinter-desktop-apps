import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

# -----------------------
# Secret Encoder
# -----------------------
class SecretEncoder:
    def __init__(self, message):
        self.message = message

    def encode(self):
        reversed_msg = self.message[::-1]
        secret = ""
        for i in range(len(reversed_msg)):
            secret += reversed_msg[i]
            if i < len(reversed_msg) - 1:
                secret += "01" * random.randint(1, 3)
        return secret


# -----------------------
# Decoder
# -----------------------
class Translate:
    def __init__(self, msg):
        self.msg = msg

    def decoding(self):
        cleaned = self.msg.replace("0", "").replace("1", "")
        decoded = cleaned[::-1]
        return decoded


# -----------------------
# Fizzy Detection
# -----------------------
def is_fizzy(text):
    if not text.strip():
        return False
    zeros_ones = len(re.findall(r"[01]", text))
    ratio = zeros_ones / len(text)
    return ratio > 0.2


def is_normal(text):
    return not is_fizzy(text)


# -----------------------
# Main App
# -----------------------
class FizzyApp:
    def __init__(self, parent_window, mode):
        self.parent_window = parent_window
        self.root = tk.Toplevel()
        self.root.title("Fizzy Language Encoder & Decoder")
        self.root.geometry("650x560")
        self.root.configure(bg="#121417")
        self.root.resizable(False, False)

        # Colors
        bg_dark = "#121417"
        panel_bg = "#1e2227"
        entry_bg = "#252a30"
        text_fg = "#e0e0e0"
        accent = "#00bfa5"
        button_color = "#6c63ff"
        button_hover = "#8c84ff"
        blue_color = "#2b8eff"
        green_color = "#00bfa5"

        # ttk Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background=bg_dark, foreground=text_fg, font=("Segoe UI", 11))

        # Title
        ttk.Label(
            self.root,
            text="SECRET MESSAGING BY FIZZY",
            font=("Segoe UI Semibold", 18),
            foreground=accent,
            background=bg_dark
        ).pack(pady=(25, 10))

        self.mode = mode

        # Mode display
        ttk.Label(
            self.root,
            text=f"Mode Selected: {self.mode.upper()}",
            font=("Segoe UI", 12, "bold"),
            background=bg_dark,
            foreground=blue_color if self.mode == "encode" else green_color
        ).pack(pady=5)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=panel_bg, bd=0, highlightthickness=1, highlightbackground=accent)
        input_frame.pack(pady=15)
        ttk.Label(input_frame, text="Enter your message:", background=panel_bg, foreground=text_fg).pack(anchor="w", padx=10, pady=5)
        self.input_text = tk.Text(input_frame, height=6, width=70, bg=entry_bg, fg=text_fg,
                                  insertbackground="white", wrap="word", font=("Consolas", 10),
                                  relief="flat")
        self.input_text.pack(padx=10, pady=(0, 10))

        # Process Button
        self.process_button = tk.Label(
            self.root,
            text="Process",
            bg=button_color,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.process_button.pack(pady=10)
        self.process_button.bind("<Button-1>", lambda e: self.process())
        self.process_button.bind("<Enter>", lambda e: self.process_button.config(bg=button_hover))
        self.process_button.bind("<Leave>", lambda e: self.process_button.config(bg=button_color))

        # Output Frame
        output_frame = tk.Frame(self.root, bg=panel_bg, bd=0, highlightthickness=1, highlightbackground=accent)
        output_frame.pack(pady=10)
        ttk.Label(output_frame, text="Result:", background=panel_bg, foreground=text_fg).pack(anchor="w", padx=10, pady=5)
        self.output_text = tk.Text(output_frame, height=6, width=70, bg=entry_bg, fg="#7ef9c9",
                                   insertbackground="white", wrap="word", font=("Consolas", 10),
                                   relief="flat", state="disabled")
        self.output_text.pack(padx=10, pady=(0, 10))

        # Back Button
        self.back_button = tk.Label(
            self.root,
            text="← Back to Mode Selection",
            bg="#30343a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.back_button.pack(pady=(5, 15))
        self.back_button.bind("<Button-1>", lambda e: self.go_back())
        self.back_button.bind("<Enter>", lambda e: self.back_button.config(bg="#454a50"))
        self.back_button.bind("<Leave>", lambda e: self.back_button.config(bg="#30343a"))

        # Footer
        ttk.Label(self.root, text="Designed by Faizan  |  Fizzy Encoder v3.6",
                  font=("Segoe UI", 9, "italic"),
                  background=bg_dark,
                  foreground="#707070").pack(side="bottom", pady=10)

    def go_back(self):
        self.root.destroy()
        self.parent_window.deiconify()  # show the mode selection window again

    def process(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter a message first!")
            return

        if self.mode == "encode":
            if is_fizzy(text):
                messagebox.showinfo("Notice", "This message already looks fizzy! Encoding skipped.")
                return
            result = SecretEncoder(text).encode()
        else:
            if is_normal(text):
                messagebox.showinfo("Notice", "This message doesn’t look fizzy! Decoding skipped.")
                return
            result = Translate(text).decoding()

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)
        self.output_text.config(state="disabled")


# -----------------------
# Mode Selection Window
# -----------------------
class ModeSelectWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Choose Mode - Fizzy Encoder")
        self.root.geometry("480x300")
        self.root.configure(bg="#121417")
        self.root.resizable(False, False)

        blue_color = "#2b8eff"
        blue_hover = "#4da0ff"
        green_color = "#00bfa5"
        green_hover = "#26d7b7"

        ttk.Label(
            root,
            text="Fizzy Language Tool",
            font=("Segoe UI Semibold", 20),
            background="#121417",
            foreground="#00bfa5"
        ).pack(pady=(40, 20))

        ttk.Label(
            root,
            text="Select a mode to continue:",
            font=("Segoe UI", 12),
            background="#121417",
            foreground="#e0e0e0"
        ).pack(pady=(0, 20))

        button_frame = tk.Frame(root, bg="#121417")
        button_frame.pack()

        # Encode Button
        encode_btn = tk.Label(
            button_frame,
            text="Encode",
            bg=blue_color,
            fg="white",
            font=("Segoe UI", 13, "bold"),
            padx=40,
            pady=12,
            cursor="hand2"
        )
        encode_btn.grid(row=0, column=0, padx=15)
        encode_btn.bind("<Enter>", lambda e: encode_btn.config(bg=blue_hover))
        encode_btn.bind("<Leave>", lambda e: encode_btn.config(bg=blue_color))
        encode_btn.bind("<Button-1>", lambda e: self.open_main("encode"))

        # Decode Button
        decode_btn = tk.Label(
            button_frame,
            text="Decode",
            bg=green_color,
            fg="white",
            font=("Segoe UI", 13, "bold"),
            padx=40,
            pady=12,
            cursor="hand2"
        )
        decode_btn.grid(row=0, column=1, padx=15)
        decode_btn.bind("<Enter>", lambda e: decode_btn.config(bg=green_hover))
        decode_btn.bind("<Leave>", lambda e: decode_btn.config(bg=green_color))
        decode_btn.bind("<Button-1>", lambda e: self.open_main("decode"))

        ttk.Label(
            root,
            text="Designed by Faizan  |  Fizzy Encoder v3.6",
            font=("Segoe UI", 9, "italic"),
            background="#121417",
            foreground="#707070"
        ).pack(side="bottom", pady=15)

    def open_main(self, mode):
        FizzyApp(self.root, mode)
        self.root.withdraw()  # hide mode window when main app opens


# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    ModeSelectWindow(root)
    root.mainloop()
