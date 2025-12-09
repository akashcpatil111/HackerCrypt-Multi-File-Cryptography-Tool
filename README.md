# 🔐 Forensic File Encryption Tool (Batch Mode)

This is an advanced desktop application developed in Python for encrypting and decrypting files using a robust, custom stream cipher. It is designed for batch processing, security, and data integrity verification.

## ✨ Features & Highlights

This project demonstrates strong application development and cryptographic best practices, including:

* **AES-Like Stream Cipher:** Implements a custom encryption scheme using a salted hash-based keystream, making encrypted files completely unreadable and visually secure.
* **Data Integrity Verification:** Uses **SHA-256 Hashing** to calculate a unique fingerprint of the original file, which is stored in the encrypted header. Upon decryption, the hash is re-verified to guarantee the file is an exact, uncorrupted copy.
* **High Performance (Chunking):** Uses **chunk-based file processing** (8 KB chunks) for I/O operations, ensuring minimal memory consumption and efficient handling of multi-gigabyte files.
* **Responsive GUI (Threading):** Implements **multi-threading** (`threading` module) to run the intensive encryption/decryption tasks in the background, preventing the Tkinter GUI from freezing.
* **Secure Key Derivation:** Employs **BLAKE2b** and **Salting** (using the `secrets` module) to securely derive a unique cipher key for every file, even if the password is the same.
* **Batch Processing:** Supports selecting and processing multiple files in a single operation.

## 🛠️ Technologies Used

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **GUI** | `tkinter` | Standard Python GUI framework. |
| **Concurrency** | `threading` | Prevents the application from freezing during batch processing. |
| **Cryptography** | `hashlib` (SHA256, BLAKE2b) | Key derivation, salting, and integrity verification. |
| **Security** | `secrets` | Cryptographically secure generation of random salts. |
| **File I/O** | `os` | System interaction and file path management. |
| **Image Preview** | `PIL (Pillow)` | Handles image resizing and preview display. |

## 🚀 How to Run the Application

### Prerequisites

1.  **Python 3.x:** Ensure you have Python installed.
2.  **Dependencies:** Install the required third-party libraries:

    ```bash
    pip install Pillow
    ```
    *(Note: This project does not require OpenCV (`cv2`) or PyCryptodome, as all cryptographic and file operations are handled by standard Python libraries.)*

### Execution

1.  Save the entire Python code as `encrypt_tool.py`.
2.  Run the script from your terminal:

    ```bash
    python encrypt_tool.py
    ```

## 📝 Usage

1.  **Enter Password:** Provide a strong password in the text box. This is the **only key** needed for decryption.
2.  **Browse Files:** Click **Browse Files** to select the image(s) or any file(s) you wish to process.
3.  **Encrypt All:** Click **Encrypt All**. The original file remains, and a new file with the extension `_enc.bin` (e.g., `photo_enc.bin`) will be created in the same directory.
4.  **Decrypt All:** Select the encrypted `_enc.bin` file(s) and enter the **exact same password**. A new decrypted file with the `_dec` suffix (e.g., `photo_dec.bin`) will be created.

### Integrity Report
After decryption, the application provides a detailed report:
* **✅ Verified:** The decrypted file matches the original file exactly (hash check passed).
* **❌ Integrity Failed:** The password was wrong, or the file was corrupted/tampered with.

---

## 💡 Why This Project is Essential

This project demonstrates an understanding of **file-level security**. A computer login password only protects the device, but your files can be compromised if the storage is accessed directly or transferred to another device. This tool protects the data itself, ensuring **confidentiality** (only the key works) and **integrity** (the file is confirmed to be unaltered).
