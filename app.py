import streamlit as st
from streamlit_lottie import st_lottie
import streamlit_authenticator as stauth
import requests
import pickle
import pandas as pd
import datetime
import plotly.express as px

# -------------------------
# 1. Page Configuration
# -------------------------
st.set_page_config(
    page_title="AI Expense Tracker",
    page_icon=":money_with_wings:",
    layout="wide"
)

# -------------------------
# 2. Password Hashing and Authentication Setup
# -------------------------
hashed_passwords = stauth.Hasher(["Riddhi@123"]).generate()
credentials = {
    "usernames": {
        "riddhi": {
            "name": "Riddhi",
            "password": hashed_passwords[0]
        }
    }
}
authenticator = stauth.Authenticate(
    credentials,
    "expense_tracker_app",
    "auth_key",
    cookie_expiry_days=30
)

# -------------------------
# --------------------------
# 3. Login Form
# --------------------------
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Invalid username or password")
    st.stop()  # 👈 Stops rest of app from rendering

elif authentication_status is None:
    st.warning("Please enter your username and password")
    st.stop()  # 👈 Stops rest of app from rendering

elif authentication_status:
    st.success(f"Welcome {name}! 👋")
    authenticator.logout("Logout", "sidebar")

    # ✅ Initialize history session state (optional but recommended)
    if "history" not in st.session_state:
        st.session_state.history = []


    # -------------------------
    # 4. Load Animation Loader
    # -------------------------
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # -------------------------
    # 5. Custom Styling
    # -------------------------
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Outfit', sans-serif;
            background-color: #0F1117;
            color: #F1F1F1;
        }
        .main {
            padding: 2rem;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stButton > button {
            background: linear-gradient(90deg, #00C9FF, #92FE9D);
            border: none;
            color: black;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #92FE9D, #00C9FF);
        }
        .stSidebar {
            background-color: #10151D;
        }
        .stProgress > div > div {
            background-image: linear-gradient(to right, #00F260, #0575E6);
        }
        h1, h2, h3, h4 {
            color: #F15BB5;
        }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------
    # 6. Load ML Models
    # -------------------------
    with open("expense_classifier.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)

    # -------------------------
    # 7. Session State Initialization
    # -------------------------
    if "history" not in st.session_state:
        st.session_state.history = []

    # -------------------------
    # 8. UI Layout and Functionalities
    # -------------------------
    st.markdown("""
        <div style='background: linear-gradient(to right, #9B5DE5, #F15BB5); padding: 2rem; border-radius: 12px; text-align: center;'>
            <h1 style='color: white; font-size: 2.5rem; margin: 0;'>💸 Smart AI-Powered Expense Tracker</h1>
            <p style='color: white; font-size: 1.2rem; margin-top: 0.5rem;'>Track, Predict, and Improve Your Financial Health 🚀</p>
        </div>
    """, unsafe_allow_html=True)

    # Your full app logic (input forms, prediction, charts, goals, insights, chatbot, etc.) should come here
    st.title("💸 AI Expense Tracker: Master Your Money with AI")

   

    # TIP: Paste the rest of your old app logic from your original file below this point!

# 6. Sidebar: Expense Input and Additional Features
# -------------------------
st.sidebar.header("Expense Input")
description = st.sidebar.text_input("Expense Description", "")
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, value=0.0, step=0.1)
date = st.sidebar.date_input("Date", value=datetime.date.today())

# New: Input for Monthly Budget
monthly_budget = st.sidebar.number_input("Monthly Budget (₹)", min_value=0.0, value=0.0, step=100.0)
# 🎯 Savings Goal Tracker
st.sidebar.markdown("### 🎯 Savings Goal Tracker")
savings_goal = st.sidebar.number_input("Savings Goal (₹)", min_value=0.0, step=500.0)
goal_date = st.sidebar.date_input("Target Date", value=datetime.date.today())


if st.sidebar.button("Predict Category"):
    if description and amount > 0:
        input_text = f"{description} ₹{amount}"
        input_vector = vectorizer.transform([input_text])
        prediction = model.predict(input_vector)
        category = label_encoder.inverse_transform(prediction)[0]
        st.sidebar.success(f"Predicted Category: **{category}**")
        
        # Save the prediction details into session state history
        st.session_state.history.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Description": description,
            "Amount": amount,
            "Predicted Category": category
        })
    else:
        st.sidebar.warning("Please provide a description and an amount greater than 0.")

st.sidebar.markdown("---")
if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.sidebar.info("History cleared!")

if st.sidebar.button("Export History as CSV"):
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        csv = history_df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("No history to export.")

# -------------------------

# 7. Display Prediction History and Charts on the main page
# -------------------------
st.write("## 📊 Prediction History")
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.datafram(history_df)

    import plotly.graph_objects as go

    category_counts = history_df["Predicted Category"].value_counts()

    fig = go.Figure(data=[
        go.Bar(
            x=category_counts.index,
            y=category_counts.values,
            marker_color="#9B5DE5"  # Violet
        )
    ])

    fig.update_layout(
        title="📊 Category-wise Expense Breakdown",
        xaxis_title="Category",
        yaxis_title="Total Entries",
        template="plotly_dark",
        plot_bgcolor="#0B0F14",
        paper_bgcolor="#0B0F14",
        font=dict(color="#F0F0F0")
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No predictions yet.")

# -------------------------
# 8. Filter Predictions by Date and Daily Expense Chart
# -------------------------
st.write("## 🗓️ Filter by Date Range")
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    history_df["Date"] = pd.to_datetime(history_df["Date"])

    default_dates = [history_df["Date"].min(), history_df["Date"].max()]
    start_date, end_date = st.date_input("Select Date Range", default_dates)

    filtered_df = history_df[
        (history_df["Date"] >= pd.to_datetime(start_date)) &
        (history_df["Date"] <= pd.to_datetime(end_date))
    ]

    st.write("### Filtered Prediction History")
    st.table(filtered_df)

    if not filtered_df.empty:
        daily_expenses = filtered_df.groupby("Date")["Amount"].sum().reset_index()

        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Scatter(
                x=daily_expenses["Date"],
                y=daily_expenses["Amount"],
                mode='lines+markers',
                line=dict(color="#00BFFF", width=3),
                marker=dict(size=8),
                name="Daily Spend"
            )
        ])

        fig.update_layout(
            title="📅 Daily Spending Pattern",
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            template="plotly_dark",
            plot_bgcolor="#0B0F14",
            paper_bgcolor="#0B0F14",
            font=dict(color="#F0F0F0"),
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No predictions in the selected date range.")
else:
    st.write("No predictions to filter.")

# -------------------------
# 9. Monthly Budget Tracker
# -------------------------
st.write("## 💰 Monthly Budget Overview")
if monthly_budget > 0 and st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    history_df["Date"] = pd.to_datetime(history_df["Date"])

    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    current_month_df = history_df[
        (history_df["Date"].dt.year == current_year) & (history_df["Date"].dt.month == current_month)
    ]

    total_spent = current_month_df["Amount"].sum()
    percent_spent = min(total_spent / monthly_budget, 1.0)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Spent This Month", f"₹{total_spent:.2f}")

    with col2:
        remaining = monthly_budget - total_spent
        st.metric("📉 Remaining Budget", f"₹{remaining:.2f}")
        st.progress(percent_spent)

    st.write("### Spending by Category This Month")
    if not current_month_df.empty:
        monthly_category_counts = current_month_df["Predicted Category"].value_counts()
        st.bar_chart(monthly_category_counts)

        st.write("### Category Breakdown (Pie Chart)")
        pie_chart = px.pie(
            current_month_df, 
            names="Predicted Category", 
            values="Amount", 
            title="Expense Distribution by Category"
        )
        st.plotly_chart(pie_chart)
    else:
        st.write("No expenses recorded for the current month.")

else:
    st.write("Set a monthly budget in the sidebar to track your spending.")
# -------------------------
# 10. Financial Recommendations Section
# -------------------------
with st.expander("💡 Personalized Financial Advice & Warnings"):
    st.write("Based on your spending history, here are some personalized recommendations:")
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        # Calculate total expenses in the current month
        history_df["Date"] = pd.to_datetime(history_df["Date"])
        current_month_df = history_df[
            (history_df["Date"].dt.year == datetime.date.today().year) & 
            (history_df["Date"].dt.month == datetime.date.today().month)
        ]
        if not current_month_df.empty:
            total_monthly = current_month_df["Amount"].sum()
            # Calculate percentage spent per category
            category_pct = (current_month_df.groupby("Predicted Category")["Amount"].sum() / total_monthly) * 100
            st.write("#### Spending Breakdown (Current Month):")
            st.write(category_pct.round(2).to_frame("Percentage"))
            
            # Provide suggestions if any category exceeds a threshold (e.g., 40%)
            recommendations = []
            for cat, pct in category_pct.items():
                if pct > 40:
                    recommendations.append(f"Your spending on **{cat}** is high ({pct:.1f}%). Consider reducing expenses in this category.")
            if recommendations:
                for rec in recommendations:
                    st.info(rec)
            else:
                st.success("Your spending appears balanced. Keep up the good work!")
        else:
            st.write("No data for the current month to analyze recommendations.")
    else:
        st.write("No expense history available to generate recommendations.")

# -------------------------
# 11. Chatbot Help Section
# -------------------------
with st.expander("🤖 Ask FinanceBot: Get Instant Money Tips"):
    st.write("Ask a question about managing your finances:")
    user_question = st.text_input("Your Question:", "")
    if st.button("Get Answer", key="chatbot"):
        # Simple keyword-based responses (expand as needed)
        if user_question:
            question_lower = user_question.lower()
            if "budget" in question_lower:
                st.write("**Tip:** To manage your budget, consider tracking your daily expenses and setting a realistic monthly limit.")
            elif "save" in question_lower or "savings" in question_lower:
                st.write("**Tip:** Try setting up a recurring transfer to your savings account each month. Small amounts add up over time!")
            elif "expense" in question_lower:
                st.write("**Tip:** Categorizing your expenses can help you identify areas to cut costs. Use the app to analyze your spending patterns.")
            elif "recommendation" in question_lower:
                st.write("**Tip:** Based on your history, focusing on reducing spending in your highest-cost category could free up funds for savings.")
            else:
                st.write("**Tip:** Keep track of your spending, set realistic goals, and review your expense history regularly for insights.")
        else:
            st.write("Please enter a question to get a response.")

# -------------------------
# -------------------------
# 13. AI Finance Coach Section
# -------------------------
with st.expander("💼 AI Finance Coach: Insights + Forecasts"):
    if monthly_budget > 0 and st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        df["Date"] = pd.to_datetime(df["Date"])

        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        current_df = df[(df["Date"].dt.month == current_month) & (df["Date"].dt.year == current_year)]

        if not current_df.empty:
            total_spent = current_df["Amount"].sum()
            balance = monthly_budget - total_spent
            category_total = current_df.groupby("Predicted Category")["Amount"].sum()
            category_percent = (category_total / total_spent) * 100

            st.subheader("🧠 Spending Insights")
            for cat, pct in category_percent.items():
                if pct > 40:
                    st.warning(f"⚠️ You're spending {pct:.1f}% on **{cat}**. Try reducing it to free up funds.")
                elif pct > 25:
                    st.info(f"💡 You spend {pct:.1f}% on **{cat}**. Keep an eye on it.")

            st.markdown("---")
            st.subheader("📈 Savings Forecast")
            st.write(f"**Total Monthly Budget:** ₹{monthly_budget}")
            st.write(f"**Total Spent This Month:** ₹{total_spent:.2f}")
            st.write(f"**Estimated Monthly Savings:** ₹{balance:.2f}")

            if balance > 0:
                months = [1, 3, 6, 12]
                forecast = {f"{m} month(s)": balance * m for m in months}
                forecast_df = pd.DataFrame.from_dict(forecast, orient="index", columns=["Estimated Savings (₹)"])

                st.line_chart(forecast_df)
                st.success("Based on your current spending, you're on track to save! 🎯")
            else:
                st.error("Your expenses have exceeded your monthly budget. Consider cutting back.")
        else:
            st.info("Add some expenses this month to get personalized advice.")
    else:
        st.info("Set a monthly budget and add expense records to get AI coaching.")

# 🎥 Add Finance Lottie Animation Below AI Coach
lottie_finance = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_t24tpvcu.json")
st_lottie(lottie_finance, speed=1, height=300, key="ai-finance")

# -------------------------
# 14. 🌟 Your Savings Goal Progress
# -------------------------
st.write("## 🌟 Your Savings Goal Progress")
with st.expander("📌 Track Progress Toward Your Goal"):
    if savings_goal > 0 and goal_date > datetime.date.today():
        if monthly_budget > 0 and st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            df["Date"] = pd.to_datetime(df["Date"])

            current_month = datetime.date.today().month
            current_year = datetime.date.today().year
            current_df = df[(df["Date"].dt.month == current_month) & (df["Date"].dt.year == current_year)]

            spent = current_df["Amount"].sum()
            saved = monthly_budget - spent if monthly_budget - spent > 0 else 0

            months_left = (goal_date.year - datetime.date.today().year) * 12 + (goal_date.month - datetime.date.today().month)
            monthly_needed = savings_goal / months_left if months_left > 0 else savings_goal

            progress = min(saved / savings_goal, 1.0)

            st.markdown(f"**Goal:** ₹{savings_goal:,.0f} by {goal_date.strftime('%B %d, %Y')}")
            st.markdown(f"**You need to save:** ₹{monthly_needed:,.0f} per month")
            st.markdown(f"**Saved so far this month:** ₹{saved:,.0f}")
            st.progress(progress)

            # Trophy animation 🎉
            if progress >= 1.0:
                trophy = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_touohxv0.json")
                if trophy:
                    st_lottie(trophy, height=200, key="goal-trophy")
                st.success("🎉 You've hit your savings goal! Great job!")
            elif progress > 0.5:
                st.info("💪 You're over halfway there — keep saving!")
            else:
                st.warning("📉 You're behind. Try to cut back expenses to catch up.")
        else:
            st.info("Set a monthly budget and add some expenses to start tracking.")
    else:
        st.info("Set a valid savings goal and target date in the sidebar.")


# 12. Footer
# -------------------------
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io/)")
