
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

from database import (
    create_table, add_expense, get_expenses, delete_expense,
    set_monthly_budget, get_monthly_budget,
    add_savings_goal, get_savings_goals,
    update_savings, delete_savings_goal,
    create_challenge, get_challenges,
    complete_challenge, delete_challenge
)

from ai_assistant import ask_money_assistant
from pdf_report import generate_monthly_report


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="VAULT AI | Personal Finance",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# PROFESSIONAL UI THEME
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #0B1120;
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263449;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #172554, #1E1B4B);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #3730A3;
}

[data-testid="stMetricLabel"] {
    color: #C4B5FD !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

h1 {
    color: #A78BFA !important;
}

h2, h3 {
    color: #C4B5FD !important;
}

p, label {
    color: #CBD5E1;
}

.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #6D28D9);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #5B21B6;
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: #059669;
    color: white;
    border-radius: 9px;
    border: none;
    font-weight: 600;
}

div[data-testid="stProgressBar"] > div > div {
    background-color: #8B5CF6;
}

div[data-testid="stForm"] {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111827;
    border-color: #334155;
    border-radius: 12px;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE AND DATA
# --------------------------------------------------

create_table()

expenses = get_expenses()
goals = get_savings_goals()

df = pd.DataFrame(
    expenses,
    columns=["ID", "Amount", "Category", "Description", "Date"]
)

today = date.today()
today_string = today.isoformat()
current_month = today.strftime("%Y-%m")

total_expenses = float(df["Amount"].sum()) if not df.empty else 0

monthly_expenses = (
    float(df[df["Date"].str.startswith(current_month)]["Amount"].sum())
    if not df.empty else 0
)

today_expenses = (
    float(df[df["Date"] == today_string]["Amount"].sum())
    if not df.empty else 0
)

current_budget = get_monthly_budget()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🔐 VAULT AI")
    st.caption("YOUR PERSONAL FINANCE ASSISTANT")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "💰 Expenses",
            "🎯 Budget",
            "💎 Savings Goals",
            "🚫 No-Spend Challenge",
            "📊 Analytics",
            "📄 PDF Reports",
            "🤖 AI Assistant"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### 💜 Smart Money Management")
    st.caption("Spend Smart. Save Smarter.")

    st.divider()

    st.caption("VAULT AI | Version 1.0")


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.title("🔐 VAULT AI")
st.markdown("### Your Money. Your Control.")

st.caption(
    f"Welcome to your personal finance dashboard | "
    f"{today.strftime('%d %B %Y')}"
)

st.divider()


# --------------------------------------------------
# 1. DASHBOARD
# --------------------------------------------------

if page == "🏠 Dashboard":

    st.header("🏠 Finance Dashboard")

    st.write("Here is your financial overview.")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}"
    )

    col2.metric(
        "This Month",
        f"₹{monthly_expenses:,.2f}"
    )

    col3.metric(
        "Today's Expenses",
        f"₹{today_expenses:,.2f}"
    )

    st.divider()

    st.subheader("🎯 Monthly Budget Overview")

    if current_budget > 0:

        remaining = current_budget - monthly_expenses
        percentage = monthly_expenses / current_budget * 100

        col1, col2, col3 = st.columns(3)

        col1.metric("Monthly Budget", f"₹{current_budget:,.2f}")
        col2.metric("Amount Spent", f"₹{monthly_expenses:,.2f}")
        col3.metric("Remaining", f"₹{remaining:,.2f}")

        st.write(f"Budget Used: {percentage:.1f}%")

        st.progress(min(percentage / 100, 1.0))

        if percentage >= 100:
            st.error("🚨 You have exceeded your monthly budget!")
        elif percentage >= 80:
            st.warning("⚠️ You have used 80% or more of your budget.")
        else:
            st.success("✅ You are within your monthly budget.")

    else:
        st.info("Set your monthly budget from the Budget section.")

    st.divider()

    st.subheader("💎 Your Savings Goals")

    if goals:

        for goal in goals:

            goal_id, name, target, saved = goal

            progress = min(saved / target, 1.0) if target > 0 else 0

            st.write(f"**{name}**")

            st.progress(progress)

            st.caption(
                f"Saved ₹{saved:,.2f} of ₹{target:,.2f} "
                f"({progress * 100:.1f}%)"
            )

    else:
        st.info("Create your first savings goal!")

    st.divider()

    st.subheader("📋 Recent Transactions")

    if not df.empty:

        st.dataframe(
            df.head(5),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No transactions recorded yet.")

    st.divider()

    if not df.empty:

        st.subheader("📊 Spending by Category")

        category_data = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            category_data,
            names="Category",
            values="Amount",
            hole=0.55,
            title="Your Spending Distribution",
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            font_color="#F1F5F9"
        )

        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# 2. EXPENSE TRACKING
# --------------------------------------------------

elif page == "💰 Expenses":

    st.header("💰 Expense Management")

    st.write("Record and manage your daily expenses.")

    with st.form("expense_form", clear_on_submit=True):

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food", "Travel", "Shopping", "Bills",
                "Education", "Health", "Entertainment", "Other"
            ]
        )

        description = st.text_input("Description")

        submitted = st.form_submit_button("➕ Add Expense")

        if submitted:

            if amount <= 0:
                st.error("Enter an amount greater than zero.")

            else:
                add_expense(amount, category, description)
                st.success("Expense saved successfully!")
                st.rerun()

    st.divider()

    st.subheader("📋 Expense History")

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        selected_id = st.selectbox(
            "Select Expense ID to delete",
            df["ID"].tolist()
        )

        if st.button("🗑️ Delete Selected Expense"):

            delete_expense(selected_id)
            st.success("Expense deleted!")
            st.rerun()

    else:
        st.info("No expenses recorded yet.")


# --------------------------------------------------
# 3. BUDGET MANAGEMENT
# --------------------------------------------------

elif page == "🎯 Budget":

    st.header("🎯 Smart Monthly Budget")

    st.write("Set a spending limit and monitor your monthly expenses.")

    current_budget = get_monthly_budget()

    with st.form("budget_form"):

        budget_amount = st.number_input(
            "Set Monthly Budget (₹)",
            min_value=0.0,
            value=float(current_budget),
            step=500.0
        )

        submitted = st.form_submit_button("Save Budget")

        if submitted:

            if budget_amount <= 0:
                st.error("Enter a budget greater than zero.")

            else:
                set_monthly_budget(budget_amount)
                st.success("Monthly budget saved!")
                st.rerun()

    if current_budget > 0:

        remaining = current_budget - monthly_expenses
        percentage = monthly_expenses / current_budget * 100

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric("Budget", f"₹{current_budget:,.2f}")
        col2.metric("Spent", f"₹{monthly_expenses:,.2f}")
        col3.metric("Remaining", f"₹{remaining:,.2f}")

        st.write(f"Budget Usage: {percentage:.1f}%")

        st.progress(min(percentage / 100, 1.0))

        if percentage >= 100:
            st.error("🚨 Budget Exceeded!")
        elif percentage >= 80:
            st.warning("⚠️ You have used 80% or more of your budget.")
        else:
            st.success("✅ You are within your budget!")

    else:
        st.info("Set a monthly budget to activate smart alerts.")


# --------------------------------------------------
# 4. SAVINGS GOALS
# --------------------------------------------------

elif page == "💎 Savings Goals":

    st.header("💎 Savings Goal Tracker")

    st.write("Create goals and track your savings progress.")

    with st.form("savings_goal_form"):

        goal_name = st.text_input(
            "Goal Name",
            placeholder="Example: Buy a Laptop"
        )

        target_amount = st.number_input(
            "Target Amount (₹)",
            min_value=0.0,
            step=500.0
        )

        submitted = st.form_submit_button("Create Goal")

        if submitted:

            if not goal_name.strip():
                st.error("Please enter a goal name.")

            elif target_amount <= 0:
                st.error("Enter a target amount greater than zero.")

            else:
                add_savings_goal(goal_name.strip(), target_amount)
                st.success("Savings goal created!")
                st.rerun()

    st.divider()

    goals = get_savings_goals()

    if goals:

        for goal in goals:

            goal_id, name, target, saved = goal

            remaining = max(target - saved, 0)
            progress = min(saved / target, 1.0) if target > 0 else 0

            with st.container(border=True):

                st.subheader(f"💰 {name}")

                col1, col2, col3 = st.columns(3)

                col1.metric("Target", f"₹{target:,.2f}")
                col2.metric("Saved", f"₹{saved:,.2f}")
                col3.metric("Remaining", f"₹{remaining:,.2f}")

                st.progress(progress)

                st.write(f"Progress: {progress * 100:.1f}%")

                if saved >= target:
                    st.success("🎉 Goal achieved!")

                else:

                    with st.form(f"add_savings_{goal_id}"):

                        saving_amount = st.number_input(
                            "Add Savings (₹)",
                            min_value=0.0,
                            step=100.0,
                            key=f"saving_{goal_id}"
                        )

                        submitted = st.form_submit_button("Add Money")

                        if submitted:

                            if saving_amount <= 0:
                                st.error("Enter an amount greater than zero.")

                            else:
                                update_savings(goal_id, saving_amount)
                                st.success("Savings updated!")
                                st.rerun()

                if st.button(
                    "Delete Goal",
                    key=f"delete_goal_{goal_id}"
                ):
                    delete_savings_goal(goal_id)
                    st.rerun()

    else:
        st.info("Create your first savings goal!")


# --------------------------------------------------
# 5. NO-SPEND CHALLENGE
# --------------------------------------------------

elif page == "🚫 No-Spend Challenge":

    st.header("🚫 No-Spend Challenge")

    st.write("Challenge yourself to avoid unnecessary spending!")

    with st.form("challenge_form"):

        challenge_name = st.text_input(
            "Challenge Name",
            placeholder="Example: No Shopping Challenge"
        )

        duration = st.selectbox(
            "Challenge Duration",
            [3, 7, 30],
            format_func=lambda x: f"{x} Days"
        )

        submitted = st.form_submit_button("Start Challenge")

        if submitted:

            if not challenge_name.strip():
                st.error("Please enter a challenge name.")

            else:
                create_challenge(challenge_name.strip(), duration)
                st.success("Your challenge has started!")
                st.rerun()

    st.divider()

    challenges = get_challenges()

    if challenges:

        for challenge in challenges:

            challenge_id, name, duration, start_date, status = challenge

            start = date.fromisoformat(start_date)
            end_date = start + timedelta(days=duration - 1)

            elapsed_days = max(
                0,
                min((date.today() - start).days + 1, duration)
            )

            progress = elapsed_days / duration

            if status == "Completed":
                progress = 1.0

            with st.container(border=True):

                st.subheader(f"🏆 {name}")

                col1, col2, col3 = st.columns(3)

                col1.metric("Duration", f"{duration} Days")
                col2.metric("Days Counted", f"{elapsed_days}/{duration}")
                col3.metric("End Date", end_date.strftime("%d %b %Y"))

                st.progress(progress)

                if status == "Completed":

                    st.success("🎉 Challenge completed!")

                elif date.today() >= end_date:

                    st.warning(
                        "Challenge period has ended. "
                        "Review your progress before marking it completed."
                    )

                    if st.button(
                        "Mark Completed",
                        key=f"complete_{challenge_id}"
                    ):
                        complete_challenge(challenge_id)
                        st.rerun()

                else:
                    st.info(f"Status: {status}")

                if st.button(
                    "Delete Challenge",
                    key=f"delete_challenge_{challenge_id}"
                ):
                    delete_challenge(challenge_id)
                    st.rerun()

    else:
        st.info("Start your first No-Spend Challenge!")


# --------------------------------------------------
# 6. ANALYTICS AND PERSONALITY
# --------------------------------------------------

elif page == "📊 Analytics":

    st.header("📊 Spending Analytics")

    if not df.empty:

        category_data = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        st.subheader("Category-wise Expenses")

        fig1 = px.pie(
            category_data,
            names="Category",
            values="Amount",
            hole=0.5,
            title="Where Does Your Money Go?",
            template="plotly_dark"
        )

        fig1.update_layout(
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            font_color="#F1F5F9"
        )

        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        st.subheader("Monthly Spending")

        monthly_df = df.copy()

        monthly_df["Month"] = pd.to_datetime(
            monthly_df["Date"]
        ).dt.strftime("%Y-%m")

        monthly_data = (
            monthly_df.groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        fig2 = px.bar(
            monthly_data,
            x="Month",
            y="Amount",
            title="Monthly Expense Overview",
            template="plotly_dark"
        )

        fig2.update_layout(
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            font_color="#F1F5F9"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        st.subheader("🧠 Spending Personality Analysis")

        category_personality = (
            df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        highest_category = category_personality.index[0]
        highest_amount = category_personality.iloc[0]

        percentage = highest_amount / total_expenses * 100

        personalities = {
            "Food": "🍔 Foodie Spender",
            "Travel": "✈️ Travel Enthusiast",
            "Shopping": "🛍️ Shopping Lover",
            "Bills": "📄 Responsible Bill Payer",
            "Education": "📚 Knowledge Investor",
            "Health": "💚 Health Conscious Spender",
            "Entertainment": "🎬 Entertainment Lover",
            "Other": "🌟 Unique Spender"
        }

        suggestions = {
            "Food": "Try home cooking and plan your food expenses.",
            "Travel": "Use public transport and plan trips in advance.",
            "Shopping": "Avoid impulse purchases and compare prices.",
            "Bills": "Review subscriptions and reduce unnecessary bills.",
            "Education": "Look for free learning resources and student discounts.",
            "Health": "Plan health-related expenses and compare costs.",
            "Entertainment": "Set a monthly entertainment limit.",
            "Other": "Review miscellaneous expenses."
        }

        st.subheader(
            f"Your Personality: {personalities.get(highest_category)}"
        )

        st.metric(
            "Highest Spending Category",
            highest_category,
            f"{percentage:.1f}% of total expenses"
        )

        st.metric(
            "Amount Spent",
            f"₹{highest_amount:,.2f}"
        )

        st.info(f"💡 Money-saving tip: {suggestions.get(highest_category)}")

        st.bar_chart(category_personality)

    else:
        st.info("Add expenses to unlock spending analytics.")


# --------------------------------------------------
# 7. MONTHLY PDF REPORTS
# --------------------------------------------------

elif page == "📄 PDF Reports":

    st.header("📄 Monthly Finance Reports")

    st.write(
        "Generate and download your personal finance report "
        "with expense history, budget and savings information."
    )

    st.info(
        "The current report generator creates a report for the current month."
    )

    if st.button("📄 Generate Monthly PDF Report"):

        try:

            report_file = generate_monthly_report(
                expenses,
                current_budget,
                get_savings_goals()
            )

            with open(report_file, "rb") as file:
                st.session_state["monthly_report_pdf"] = file.read()

            st.success("Your monthly PDF report is ready!")

        except Exception as e:

            st.error(f"Unable to generate PDF: {e}")

    if "monthly_report_pdf" in st.session_state:

        st.download_button(
            label="⬇️ Download Monthly PDF Report",
            data=st.session_state["monthly_report_pdf"],
            file_name=f"VAULT_AI_Report_{current_month}.pdf",
            mime="application/pdf"
        )


# --------------------------------------------------
# 8. AI MONEY ASSISTANT
# --------------------------------------------------

elif page == "🤖 AI Assistant":

    st.header("🤖 VAULT AI Money Assistant")

    st.write(
        "Your personal AI finance buddy. "
        "Ask questions about your expenses and spending habits."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask VAULT AI about your money..."
    )

    if user_question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):

            with st.spinner("VAULT AI is thinking..."):

                answer = ask_money_assistant(
                    user_question,
                    get_expenses()
                )

                st.markdown(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

    if st.button("Clear Chat History"):

        st.session_state.chat_history = []
        st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<div style='text-align:center; color:#A78BFA;'>"
    "🔐 <b>VAULT AI</b> | Spend Smart. Save Smarter."
    "</div>",
    unsafe_allow_html=True
)
