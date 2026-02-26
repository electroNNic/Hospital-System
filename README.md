# 🏥 Hospital System (Flask + PostgreSQL)

A lightweight hospital admission management web app built with **Python (Flask)** and **PostgreSQL**.  
It supports login, viewing admission records, creating new admissions, and updating existing admissions via a simple web UI.

---

## ✨ Features

- Login page (supports users defined in database seed data)
- Admission list view
- Create new admission record
- Update admission record
- Basic UI with templates + static assets (HTML/CSS/JS)

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **DB Driver:** psycopg2
- **Frontend:** HTML (Jinja2 templates), CSS, jQuery

---

## 🗃️ Database Design (Schema)

SQL schema file: **`CSHschema.sql`**

Tables:
- `Administrator(UserName, Password, FirstName, LastName, Email)`
- `Patient(PatientID, Password, FirstName, LastName, Mobile)`
- `AdmissionType(AdmissionTypeID, AdmissionTypeName)`
- `Department(DeptId, DeptName)`
- `Admission(AdmissionID, AdmissionType, Department, Patient, Administrator, Fee, DischargeDate, Condition)`

Relationships:
- `Admission.AdmissionType` → `AdmissionType.AdmissionTypeID`
- `Admission.Department` → `Department.DeptId`
- `Admission.Patient` → `Patient.PatientID`
- `Admission.Administrator` → `Administrator.UserName`



