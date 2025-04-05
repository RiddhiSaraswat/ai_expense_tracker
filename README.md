# ai_expense_tracker

# 💸 AI Expense Tracker — Your Smart Financial Assistant

Welcome to the **AI-Powered Expense Tracker**, a full-stack intelligent financial tool built with **Streamlit**, powered by **Machine Learning**, and designed to help users take control of their personal finances. Whether you're a student, working professional, or budgeting for your family — this tool gives you the power of AI to make smarter spending decisions.

---

## 🌟 What This Project Does

This app transforms raw financial behavior into **meaningful insights**. It allows users to:

- ✅ Log expenses and instantly get **AI-powered category predictions**
- ✅ Set and monitor a **monthly budget** with real-time tracking
- ✅ Define a **savings goal** and see progress visually
- ✅ Get **personalized financial coaching** based on spending behavior
- ✅ Visualize data through interactive charts and graphs
- ✅ Export your data for external reporting
- ✅ Access the app securely with **password-protected login authentication**

---

## 🔧 Technologies Used

| Area               | Tools / Libraries                             |
|--------------------|-----------------------------------------------|
| Frontend           | Streamlit                                     |
| Machine Learning   | Scikit-learn, Pickle                          |
| Visualization      | Plotly, Matplotlib                            |
| Authentication     | Streamlit Authenticator                       |
| Styling            | Custom CSS (glassmorphism + fonts + glow)     |
| Animations         | LottieFiles integration                       |
| Deployment         | Streamlit Cloud                               |

---

## 📌 Key Features

### 🔐 Secure Login System
- Password-protected login using **Streamlit Authenticator**
- Credentials hashed with `stauth.Hasher`

### 🧠 AI-Based Expense Categorization
- Trained model uses **TF-IDF + ML classifier**
- Predicts spending category from free-text inputs like `"Starbucks coffee ₹300"`

### 📊 Visual Dashboards
- Category-wise **bar chart** of all expenses
- **Daily expense timeline** with trend lines
- **Pie chart** for expense share across categories
- **Metric indicators** showing total spent & budget left

### 🎯 Savings Goal Tracker
- Set a target amount and deadline
- See dynamic updates, with motivational Lottie animations
- Calculates how much to save per month to meet your goal

### 💬 AI Finance Coach
- Analyzes your real-time spending
- Highlights areas where you're overspending
- Forecasts how much you'll save in 1/3/6/12 months

### 💡 Financial Tips Chatbot
- Ask questions like “How can I save more?” or “Tips to cut expenses”
- Responds based on smart keyword detection


---

## 🧠 Behind the Scenes

- **ML Model**: Trained on a custom expense dataset with multiple categories (Food, Transport, Entertainment, etc.)
- **Vectorization**: TF-IDF to convert user inputs into model-friendly format
- **Label Encoding**: Encodes/decodes predicted categories for user display
- **Session State**: Stores data during user session for dynamic updates
- **Custom CSS**: Modern look with blurred glass panels, glow text, and custom fonts

---

## 💡 Future Plans

- 📲 Mobile-friendly UI for better use on phones
- 🏦 Bank statement upload and auto-categorization
- 🧾 Monthly PDF financial reports
- 🔔 Notification alerts for overspending
- 🧠 Integration with large language models for smarter financial advice

---

