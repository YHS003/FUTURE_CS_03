# 🔐 Secure File Share (AES-128 Encryption)
**Future Interns – Cyber Security Internship | Task 3**

---

## 📘 Overview
This project was developed as **Task 3** of the **Future Interns Cyber Security Internship**.  
It demonstrates a secure file sharing web application that uses **AES-128 encryption** to protect uploaded files from unauthorized access.

---

## ⚙️ Features
- 🔒 Encrypt any uploaded file using **AES-128**.  
- 🔓 Decrypt and restore the original file easily.  
- 🌐 Simple and clean **Flask web interface**.  
- 🗂️ Encrypted files are automatically saved with the `.enc` extension.  
- ⚡ Works locally without a database or authentication system.  

---

## 🧩 How It Works
1. A user uploads a file via the web page.  
2. The backend generates a cipher and encrypts the file using **AES-128**.  
3. The encrypted file is stored locally with the `.enc` extension.  
4. Users can download the file or decrypt it again through the interface.  

---

## 🛠️ Technologies Used
- **Python 3**  
- **Flask** (for web server)  
- **PyCryptodome / Cryptography** (for AES encryption)  
- **HTML / CSS / Bootstrap** (for UI)

---

## 🚀 How to Run
1. Clone the repository:  
   ```bash
   git clone <your-repo-link>
   cd <project-folder>
   ```
2. Create a virtual environment and install dependencies:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the Flask app:  
   ```bash
   python3 app.py
   ```
4. Open your browser and go to:  
   ```
   http://127.0.0.1:5000/
   ```

---

## 📂 Project Structure
```
Secure-File-Share/
│
├── app.py
├── crypto.py
├── templates/
├── uploads_encrypted/
├── metadata.json
├── requirements.txt
└── README.md
```

---

## 🧑‍💻 Developer
**Yehya Hamdy Shehata**  
Cyber Security Intern @ Future Interns  
🔗 GitHub: [YHS003](https://github.com/YHS003)  
📅 Task: #3 – Secure File Share (AES-128)
