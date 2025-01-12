# Resume Evaluation Application

A full-stack AI-powered application that evaluates candidate resumes against job descriptions with precision. This project combines **FastAPI**, **React.js**, **PostgreSQL**, and **Docker** to deliver a seamless experience for both technical exploration and HR solution innovation.

---

## ✨ Features

- **AI-Powered Evaluation**  
  Compare resumes with job descriptions using an LLM-based scoring algorithm.
  
- **Base64 PDF Parsing**  
  Extract text from Base64-encoded PDFs for seamless resume processing.

- **Data-Driven Architecture**  
  Store job, candidate, and evaluation details efficiently in **PostgreSQL**.

- **Interactive Frontend**  
  A user-friendly React-based interface to manage and view evaluations.

- **Dockerized Setup**  
  Simple containerized deployment for backend, frontend, and database services.

---

## 🚀 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Frontend**: [React.js](https://reactjs.org/)  
- **Database**: PostgreSQL  
- **PDF Processing**: PyPDF2  
- **Containerization**: Docker, Docker Compose  

---

## 📂 Project Structure

```plaintext
├── backend/         # FastAPI backend
│   ├── app/         # Main application logic
│   ├── models.py    # SQLAlchemy models
│   ├── database.py  # Database connection logic
│   └── main.py      # API endpoints
├── frontend/        # React.js frontend
│   ├── public/      # Static files
│   └── src/         # React components
├── docker-compose.yml  # Docker container orchestration
└── README.md        # Project documentation
