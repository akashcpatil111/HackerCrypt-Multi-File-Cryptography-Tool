import tkinter as tk
from tkinter import filedialog, Text, font
from hashlib import sha256, blake2b
from PIL import Image, ImageTk
import os
import secrets
import threading

# --- Core Encryption/Decryption Logic (from original code) ---

def password_to_key(password):
    """Convert password to a 256-bit key using SHA-256."""
    return sha256(password.encode()).digest()

def get_file_hash_chunked(file_path):
    """Generate SHA-256 hash of a file using chunk-based processing."""
    h = sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return None

# --- Main Application Class ---

class HackerCryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HackerCrypt v1.0")
        self.root.geometry("800x750")
        self.root.configure(bg="#0D0D0D")
        self.root.resizable(False, False)

        self.file_paths = []

        # --- Define Colors and Fonts ---
        self.BG_COLOR = "#0D0D0D"
        self.FG_COLOR = "#00FF41"
        self.ACCENT_COLOR = "#1A1A1A"
        self.BORDER_COLOR = "#00FF41"
        self.TITLE_FONT = font.Font(family="Courier New", size=24, weight="bold")
        self.LABEL_FONT = font.Font(family="Courier New", size=12)
        self.BUTTON_FONT = font.Font(family="Courier New", size=11, weight="bold")
        self.CONSOLE_FONT = font.Font(family="Courier New", size=10)

        self._create_widgets()

    def _create_widgets(self):
        # --- Main Title ---
        title_label = tk.Label(
            self.root,
            text="// HACKERCRYPT v1.0 //",
            font=self.TITLE_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        title_label.pack(pady=(20, 10))

        # --- Main Frame ---
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Left Column: Controls ---
        controls_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        controls_frame.grid(row=0, column=0, sticky="ns", padx=(0, 20))

        # --- Right Column: Preview & File List ---
        preview_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        preview_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)

        # --- Controls Widgets (Left Side) ---
        password_label = tk.Label(
            controls_frame,
            text="[ Master Key ]",
            font=self.LABEL_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        password_label.pack(pady=(10, 5), anchor="w")

        self.password_entry = tk.Entry(
            controls_frame,
            show="*",
            width=30,
            bg=self.ACCENT_COLOR,
            fg=self.FG_COLOR,
            insertbackground=self.FG_COLOR,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=self.BORDER_COLOR,
            highlightcolor=self.BORDER_COLOR
        )
        self.password_entry.pack(pady=5, ipady=4)

        # Buttons
        browse_btn = self._create_styled_button(controls_frame, "SELECT TARGETS", self.browse_files)
        browse_btn.pack(pady=(20, 10), fill="x")

        encrypt_btn = self._create_styled_button(controls_frame, "ENCRYPT BATCH", self.start_encrypt_thread)
        encrypt_btn.pack(pady=10, fill="x")

        decrypt_btn = self._create_styled_button(controls_frame, "DECRYPT BATCH", self.start_decrypt_thread)
        decrypt_btn.pack(pady=10, fill="x")

        # --- Preview & File List Widgets (Right Side) ---
        preview_label = tk.Label(
            preview_frame,
            text="[ IMAGE PREVIEW ]",
            font=self.LABEL_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        preview_label.pack(pady=(10, 5), anchor="w")

        self.image_preview_label = tk.Label(
            preview_frame,
            bg=self.ACCENT_COLOR,
            relief="solid",
            bd=1,
            width=45,
            height=15
        )
        self.image_preview_label.pack(pady=5, fill="both", expand=True)

        files_label = tk.Label(
            preview_frame,
            text="[ SELECTED FILES ]",
            font=self.LABEL_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        files_label.pack(pady=(15, 5), anchor="w")

        self.file_listbox = tk.Listbox(
            preview_frame,
            bg=self.ACCENT_COLOR,
            fg=self.FG_COLOR,
            font=self.CONSOLE_FONT,
            relief="solid",
            bd=1,
            height=5,
            highlightthickness=0
        )
        self.file_listbox.pack(pady=5, fill="x", expand=False)

        # --- Console Log ---
        console_frame = tk.Frame(
            self.root,
            bg=self.BG_COLOR,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=self.BORDER_COLOR
        )
        console_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.console = Text(
            console_frame,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            font=self.CONSOLE_FONT,
            relief="flat",
            state="disabled",
            height=10,
            wrap="word",
            insertbackground=self.FG_COLOR
        )
        self.console.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_message("Console initialized. Waiting for command...")

    def _create_styled_button(self, parent, text, command):
        """Helper function to create styled buttons."""
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=self.BUTTON_FONT,
            bg=self.ACCENT_COLOR,
            fg=self.FG_COLOR,
            activebackground=self.FG_COLOR,
            activeforeground=self.BG_COLOR,
            relief="solid",
            bd=1,
            pady=8,
            padx=10
        )

    def log_message(self, message):
        """Logs a message to the console widget."""
        self.console.config(state="normal")
        self.console.insert(tk.END, f">> {message}\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def browse_files(self):
        self.file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
        if self.file_paths:
            self.log_message(f"Selected {len(self.file_paths)} file(s).")
            self.update_file_list()
            self.show_image_preview(self.file_paths[0])
        else:
            self.log_message("File selection cancelled.")

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for path in self.file_paths:
            self.file_listbox.insert(tk.END, os.path.basename(path))

    def show_image_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_preview_label.config(image=img_tk, text="")
            self.image_preview_label.image = img_tk
        except Exception:
            self.image_preview_label.config(image=None, text="Preview N/A")
            self.image_preview_label.image = None

    # --- Threading Handlers ---
    def start_encrypt_thread(self):
        password = self.password_entry.get()
        if not password:
            self.log_message("ERROR: Master key cannot be empty.")
            return
        if not self.file_paths:
            self.log_message("ERROR: No target files selected.")
            return
            
        self.log_message("Starting encryption process in a background thread...")
        threading.Thread(target=self.encrypt_files_task, args=(self.file_paths, password), daemon=True).start()

    def start_decrypt_thread(self):
        password = self.password_entry.get()
        if not password:
            self.log_message("ERROR: Master key cannot be empty for decryption.")
            return
        if not self.file_paths:
            self.log_message("ERROR: No target files selected.")
            return

        self.log_message("Starting decryption process in a background thread...")
        threading.Thread(target=self.decrypt_files_task, args=(self.file_paths, password), daemon=True).start()

    # --- Core Tasks (run in threads) ---
    def encrypt_files_task(self, file_paths, password):
        key = password_to_key(password)
        
        for path in file_paths:
            try:
                salt = secrets.token_bytes(16)
                cipher_key = blake2b(key + salt, digest_size=32).digest()
                original_hash = get_file_hash_chunked(path)
                
                if original_hash is None:
                    self.root.after(0, self.log_message, f"SKIP: Could not find or read {os.path.basename(path)}")
                    continue
                
                enc_path = os.path.splitext(path)[0] + "_enc.bin"
                with open(path, "rb") as f_in, open(enc_path, "wb") as f_out:
                    header = salt + original_hash.encode()
                    f_out.write(header)
                    
                    chunk_index = 0
                    while chunk := f_in.read(8192):
                        encrypted_chunk = bytearray(len(chunk))
                        for i in range(len(chunk)):
                            encrypted_chunk[i] = chunk[i] ^ cipher_key[(chunk_index + i) % len(cipher_key)]
                        f_out.write(encrypted_chunk)
                        chunk_index += len(chunk)

                self.root.after(0, self.log_message, f"SUCCESS: Encrypted {os.path.basename(path)}")
            except Exception as e:
                self.root.after(0, self.log_message, f"FAIL: Encrypting {os.path.basename(path)} -> {e}")
        
        self.root.after(0, self.log_message, "Encryption batch complete.")

    def decrypt_files_task(self, file_paths, password):
        key = password_to_key(password)
        
        for path in file_paths:
            try:
                with open(path, "rb") as f_in:
                    header = f_in.read(16 + 64)
                    salt = header[:16]
                    original_hash_stored = header[16:].decode()
                    cipher_key = blake2b(key + salt, digest_size=32).digest()
                    
                    # Determine the decrypted file path
                    base_name, _ = os.path.splitext(path)
                    original_ext = ".bin" # Default extension if we can't determine original
                    
                    # A simple way to guess original extension if file name follows a pattern like `name.ext_enc.bin`
                    # This logic may need to be adjusted based on expected filenames.
                    parts = os.path.basename(base_name).split('.')
                    if len(parts) > 1 and parts[-1].endswith('_enc'):
                        original_ext = f".{parts[-2]}"
                        dec_base = base_name.replace(f'.{parts[-2]}_enc', '_dec')
                    else:
                        dec_base = base_name.replace('_enc', '_dec')

                    dec_path = dec_base + original_ext

                    with open(dec_path, "wb") as f_out:
                        chunk_index = 0
                        while chunk := f_in.read(8192):
                            decrypted_chunk = bytearray(len(chunk))
                            for i in range(len(chunk)):
                                decrypted_chunk[i] = chunk[i] ^ cipher_key[(chunk_index + i) % len(cipher_key)]
                            f_out.write(decrypted_chunk)
                            chunk_index += len(chunk)
                    
                    decrypted_hash = get_file_hash_chunked(dec_path)
                    if decrypted_hash == original_hash_stored:
                        self.root.after(0, self.log_message, f"SUCCESS: Decrypted & Verified {os.path.basename(path)}")
                    else:
                        self.root.after(0, self.log_message, f"FAIL: Integrity check failed for {os.path.basename(path)}. Wrong key or corrupt file.")
            except Exception as e:
                self.root.after(0, self.log_message, f"FAIL: Decrypting {os.path.basename(path)} -> {e}")

        self.root.after(0, self.log_message, "Decryption batch complete.")

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = HackerCryptApp(root)
    root.mainloop()
