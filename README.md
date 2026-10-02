# 💰 Finora – Personal Finance Management System

**Take control of your money. Track smarter. Plan better.**

Finora is a full-stack Personal Finance Management System designed to help users manage their income, expenses, budgets and savings goals in one place. It provides an intuitive dashboard, financial analytics, transaction management and an AI-powered financial assistant to make personal finance management easier and more organized.

Built using **Python, FastAPI, MongoDB and Google Gemini AI**, Finora combines secure user authentication with an interactive web interface to provide a centralized financial management experience.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [AI Financial Assistant](#-ai-financial-assistant)
- [Security](#-security)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🚀 Project Overview

Managing personal finances can become difficult when income, expenses, budgets and savings are tracked separately.

Finora addresses this problem by providing a centralized platform where users can:

- Monitor their overall financial situation.
- Record and manage income and expenses.
- Create monthly and category-wise budgets.
- Set and track savings goals.
- Analyze financial activities through analytics.
- Manage recurring transactions.
- Receive notifications about important financial activities.
- Get financial insights through an integrated AI assistant.

The application is designed with a user-friendly interface and a modular backend architecture, making it easier to maintain and extend.

---

## ✨ Key Features

### 1. 🔐 User Authentication
- User registration and login.
- Secure password hashing using bcrypt.
- JWT-based authentication.
- Protected user-specific operations.
- User profile management.
- Profile picture upload and management.
- Update personal account information.

### 2. 📊 Interactive Dashboard
- Overview of total income and expenses.
- Automatic balance calculation.
- Monthly financial summaries.
- Recent transaction overview.
- Quick access to important financial features.

### 3. 💸 Expense Management
- Add new expenses.
- View existing expenses.
- Edit expense details.
- Delete transactions.
- Organize expenses by category.
- Search and filter transactions.

### 4. 💵 Income Management
- Record different sources of income.
- Update income records.
- Delete income entries.
- View income history.
- Track total and monthly income.

### 5. 🎯 Budget Management
- Create monthly budgets.
- Set category-wise spending limits.
- Track actual spending against budgets.
- Receive notifications when spending reaches 80% of a budget.
- Receive alerts when a budget is exceeded.

### 6. 🏆 Savings Goals
- Create personal savings goals.
- Set target amounts.
- Track savings progress.
- Monitor completed and ongoing goals.
- Receive notifications when a goal is achieved.

### 7. 📈 Financial Analytics
- Analyze income and expenses.
- View financial summaries.
- Monitor spending patterns.
- Understand financial performance over different periods.

### 8. 🔄 Recurring Transactions
- Manage recurring income and expenses.
- Store transaction frequency and details.
- Keep track of regular financial activities.

### 9. 🔔 Notification Management
- View financial notifications.
- Track read and unread notifications.
- Mark individual notifications as read.
- Mark all notifications as read.
- Delete notifications.

### 10. 🤖 Finora AI – Intelligent Financial Assistant

Finora integrates Google Gemini AI to provide an interactive financial assistant.

Features include:
- AI-powered financial conversations.
- Answers based on the user's available financial information.
- Income and expense summaries.
- Budget-related insights.
- Savings goal information.
- General personal finance guidance.

The AI assistant retrieves relevant financial information from the application and uses it as context when generating responses.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API development |
| MongoDB Atlas | NoSQL database |
| PyMongo | MongoDB connectivity |
| HTML5 | Frontend structure |
| CSS3 | Frontend styling |
| JavaScript | Frontend interactions and API integration |
| Jinja2 | Server-side HTML templating |
| JWT | Authentication and authorization |
| bcrypt | Password hashing |
| Pydantic | Data validation |
| Google Gemini AI | AI-powered financial assistant |
| Google Gen AI SDK | Gemini API integration |
| Uvicorn | ASGI server |
| Docker | Containerization |
| Swagger UI | API documentation and testing |
| Postman | API testing |

---

## 🏗️ Project Architecture

Finora follows a modular client-server architecture.

```text
                 ┌──────────────────────────┐
                 │       User Interface     │
                 │                          │
                 │   HTML / CSS / JavaScript│
                 │        + Jinja2          │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │       FastAPI Backend    │
                 │                          │
                 │   Authentication         │
                 │   Expense Management     │
                 │   Income Management      │
                 │   Budget Management      │
                 │   Goals & Analytics      │
                 │   Notifications          │
                 │   Recurring Transactions │
                 └────────────┬─────────────┘
                              │
                 ┌────────────┴─────────────┐
                 ▼                          ▼
       ┌──────────────────┐       ┌──────────────────┐
       │   MongoDB Atlas  │       │   Google Gemini  │
       │                  │       │       AI         │
       │  User Data       │       │                  │
       │  Income          │       │  Financial       │
       │  Expenses        │       │  Conversations   │
       │  Budgets         │       │  & Insights      │
       │  Goals           │       │                  │
       └──────────────────┘       └──────────────────┘
```

---

## 📁 Project Structure

```text
personal-finance-manager/
│
├── app/
│   ├── database/
│   │   ├── mongodb.py
│   │   └── test_connection.py
│   │
│   ├── models/
│   │   ├── budget.py
│   │   ├── expense.py
│   │   ├── goal.py
│   │   ├── income.py
│   │   └── user.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── expenses.py
│   │   ├── income.py
│   │   ├── budgets.py
│   │   ├── goals.py
│   │   ├── analytics.py
│   │   ├── recurring.py
│   │   ├── notifications.py
│   │   ├── budget_tracking.py
│   │   ├── transaction_search.py
│   │   ├── pages.py
│   │   └── ai.py
│   │
│   ├── schemas/
│   │   ├── budget.py
│   │   ├── expense.py
│   │   ├── goal.py
│   │   ├── income.py
│   │   ├── recurring.py
│   │   └── user.py
│   │
│   ├── security/
│   │   └── jwt.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── analytics_service.py
│   │   ├── auth_service.py
│   │   ├── budget_service.py
│   │   └── expense_service.py
│   │
│   ├── static/
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── ai.html
│   │   ├── analytics.html
│   │   ├── base.html
│   │   ├── budgets.html
│   │   ├── dashboard.html
│   │   ├── expenses.html
│   │   ├── goals.html
│   │   ├── income.html
│   │   ├── login.html
│   │   ├── notifications.html
│   │   ├── profile.html
│   │   ├── recurring.html
│   │   └── register.html
│   │
│   ├── utils/
│   │   └── helpers.py
│   │
│   └── main.py
│
├── uploads/
│   └── profile_pictures/
│
├── .gitignore
├── Dockerfile
├── requirements.txt
├── README.md
└── schemas.py
```

---

## ⚙️ Installation and Setup

Follow these steps to run Finora locally.

### Prerequisites

Make sure you have installed:

- Python 3.10 or above.
- MongoDB Atlas account.
- Git.
- Google AI Studio API key for Gemini AI features.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Aritra022/Personal-Finance-Manager-Finora.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Personal-Finance-Manager-Finora
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory.

Add your own configuration values:

```env
MONGO_URL=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key
```

Also configure any JWT secret and other environment variables required by your application's authentication and database configuration.

**Important:** Never upload your `.env` file or expose your API keys, database credentials or JWT secrets publicly.

### Step 6: Run the Application

```bash
python -m uvicorn app.main:app --reload
```

### Step 7: Open Finora

Open your browser and visit:

**Application:**
http://127.0.0.1:8000/

**Swagger API Documentation:**
http://127.0.0.1:8000/docs

---

## 🔗 API Endpoints

Finora provides REST API endpoints for its main functionalities.

| Module | Endpoint | Method |
|---|---|---|
| Authentication | `/auth/register` | POST |
| Authentication | `/auth/login` | POST |
| User Profile | `/auth/me` | GET |
| Dashboard | `/dashboard-data/` | GET |
| Expenses | `/expenses/` | GET / POST |
| Income | `/income/` | GET / POST |
| Budgets | `/budgets/` | GET / POST |
| Goals | `/goals/` | GET / POST |
| Analytics | `/analytics/` | GET |
| Recurring Transactions | `/recurring/` | GET / POST |
| Notifications | `/notifications/` | GET |
| AI Assistant | `/ai/chat` | POST |

Additional endpoints support update, delete, search and other operations.

For the complete API documentation, run the application and visit:

http://127.0.0.1:8000/docs

---

## 🤖 AI Financial Assistant

One of Finora's key features is its integration with **Google Gemini AI**.

The assistant uses the user's available financial information as context to generate relevant responses.

Example questions:

- How much have I spent this month?
- What is my total income?
- Which budget has exceeded its limit?
- How much money have I saved?
- Give me a summary of my financial situation.

### AI Integration Workflow

1. The user submits a question through the Finora AI interface.
2. The frontend sends the request to the FastAPI backend.
3. The backend verifies the user's JWT authentication.
4. Relevant financial information is retrieved from MongoDB.
5. The information and user's question are passed to Gemini AI.
6. Gemini generates a response.
7. The response is returned to the frontend and displayed in the chat interface.

---

## 🔒 Security

Finora incorporates several security practices:

- JWT-based authentication for protected APIs.
- Password hashing using bcrypt.
- User-specific access to financial records.
- Pydantic-based request validation.
- Environment variables for sensitive configuration.
- Profile picture file-type and file-size validation.
- Authentication checks before accessing financial information.

---

## 🔮 Future Enhancements

Potential improvements for future versions include:

- Cloud deployment and production hosting.
- Advanced financial reports and visualizations.
- Export financial reports to PDF and Excel.
- Email and push notifications.
- Improved AI-driven spending recommendations.
- Multi-currency support.
- Mobile application integration.
- Enhanced recurring transaction automation.

---

## 🤝 Contributing

Contributions, suggestions and feedback are welcome!

If you would like to contribute:

1. Fork this repository.
2. Create a new feature branch.
3. Make your changes.
4. Commit your changes.
5. Push your branch.
6. Open a Pull Request.

---

## 👨‍💻 Author

**Aritra Bhunia**

B.Tech in Information Technology

- GitHub: [@Aritra022](https://github.com/Aritra022)
- Project Repository: [Finora – Personal Finance Manager](https://github.com/Aritra022/Personal-Finance-Manager-Finora)

---

## ⭐ Support

If you find this project interesting or useful, consider giving the repository a ⭐ on GitHub.

**Finora – Your finances, organized in one place.**

*Built with Python, FastAPI, MongoDB and Gemini AI.*
