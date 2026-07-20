# 📚 Library Management System

> A modern and responsive **Library Management System** built with **Django** to simplify library operations for administrators and students. The system provides secure authentication, efficient book management, and an intuitive user interface.

---

## ✨ Overview

The Library Management System is a web application designed to automate the daily activities of a library. It allows administrators to manage books and students while enabling students to browse available books, view issued books, and manage their profiles.

---

## 🚀 Features

### 👨‍💼 Admin Module

- Secure Admin Authentication
- Interactive Admin Dashboard
- Add New Books
- Update Book Details
- Delete Books
- Manage Categories & Authors
- View Registered Students
- Issue Books
- Return Books
- View Issued Books
- Automatic Fine Calculation for Late Returns

---

### 👨‍🎓 Student Module

- Student Registration
- Secure Login
- Student Dashboard
- Browse Available Books
- View Issued Books
- Profile Management
- Change Password

---

## 🛠️ Built With

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Django | Backend Framework |
| HTML5 | Structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| SQLite | Database |
| Django Authentication | User Authentication |
| Git & GitHub | Version Control |

---

## 📁 Project Structure

```text
library_project/
│
├── library_project/
│
├── library_app/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   └── images/
│   │
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── student/
│   │   ├── partials/
│   │   └── common/
│   │
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── utils.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/techiebella/library.git
```

### 2️⃣ Navigate to the Project

```bash
cd library
```

### 3️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### 4️⃣ Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 6️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

### 7️⃣ Run the Development Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

# 📸 Screenshots

## 🏠 Home Page

<img width="100%" src="https://github.com/user-attachments/assets/355a8895-9666-4fbe-97d4-b087a08036bb">

---

## 📚 Book Management

<img width="100%" src="https://github.com/user-attachments/assets/6fb35cec-6091-4d59-ad41-384de224f2a3">

---

## 📊 Admin Dashboard

<img width="100%" src="https://github.com/user-attachments/assets/773364b1-6935-49e7-8427-825556e59760">

---

## 👨‍🎓 Student Management

<img width="100%" src="https://github.com/user-attachments/assets/afb51b42-65f0-4a9b-906f-b7ab184efc01">

---

## 🎯 Key Highlights

- Clean & Modern User Interface
- Responsive Design
- Role-Based Authentication
- Organized Project Structure
- Automatic Fine Calculation
- Easy Book Management
- Student Profile Management
- Django Best Practices

---

## 🌟 Future Enhancements

- Email Notifications
- QR Code Based Book Issue
- Barcode Scanner Integration
- Book Reservation System
- Reports & Analytics Dashboard
- Export to Excel & PDF
- Dark Mode
- PostgreSQL Support
- Docker Deployment
- Cloud Deployment

---

## 🤝 Contributing

Contributions are always welcome!

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Added new feature"
```

4. Push the branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👩‍💻 Developer

**Eswari**

💼 Computer Science Engineering Student

🔗 GitHub: https://github.com/techiebella

---

## ⭐ Support

If you found this project useful:

⭐ Star this repository

🍴 Fork it

📢 Share it with others

---

# Thank You ❤️
