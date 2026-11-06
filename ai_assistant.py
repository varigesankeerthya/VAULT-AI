
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def ask_money_assistant(question, expenses):

    expense_details = ""

    for expense in expenses:
        expense_id, amount, category, description, expense_date = expense

        expense_details += (
            f"Date: {expense_date}, "
            f"Amount: ₹{amount}, "
            f"Category: {category}, "
            f"Description: {description}\n"
        )

    if not expense_details:
        expense_details = "No expenses have been recorded yet."

    prompt = f"""
You are VAULT AI, a friendly personal finance assistant.

Help users understand their expenses and improve their spending habits.

Recorded expenses:
{expense_details}

User's question:
{question}

Instructions:
1. Give simple and helpful answers.
2. Use recorded expenses when answering.
3. Never invent expense amounts or transactions.
4. Give practical money-saving suggestions.
5. Use Indian Rupees (₹).
6. If data is insufficient, clearly say so.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text or "Sorry, I couldn't generate a response."

    except Exception as e:
        return f"AI Assistant Error: {str(e)}"
