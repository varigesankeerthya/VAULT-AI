
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import date


def generate_monthly_report(
    expenses,
    budget,
    savings_goals,
    filename="VAULT_AI_Monthly_Report.pdf"
):

    current_month = date.today().strftime("%Y-%m")
    month_name = date.today().strftime("%B %Y")

    monthly_expenses = [
        expense for expense in expenses
        if expense[4].startswith(current_month)
    ]

    total_expenses = sum(
        expense[1] for expense in monthly_expenses
    )

    category_totals = {}

    for expense in monthly_expenses:
        category = expense[2]
        amount = expense[1]

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    elements = []

    elements.append(
        Paragraph("VAULT AI - Monthly Finance Report", styles["Title"])
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(f"Report Month: {month_name}", styles["Heading2"])
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph("1. Monthly Expense Summary", styles["Heading2"])
    )

    summary_data = [
        ["Description", "Amount"],
        ["Total Expenses", f"Rs. {total_expenses:,.2f}"],
        ["Monthly Budget", f"Rs. {budget:,.2f}"],
        ["Remaining Budget", f"Rs. {budget - total_expenses:,.2f}"]
    ]

    summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B53")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(summary_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("2. Category-wise Expenses", styles["Heading2"])
    )

    category_data = [["Category", "Amount"]]

    for category, amount in category_totals.items():
        category_data.append([
            category,
            f"Rs. {amount:,.2f}"
        ])

    if not category_totals:
        category_data.append(["No expenses", "Rs. 0.00"])

    category_table = Table(
        category_data,
        colWidths=[3 * inch, 2 * inch]
    )

    category_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B53")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(category_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("3. Expense Transactions", styles["Heading2"])
    )

    transaction_data = [
        ["Date", "Category", "Description", "Amount"]
    ]

    for expense in monthly_expenses:
        transaction_data.append([
            expense[4],
            expense[2],
            str(expense[3] or "-"),
            f"Rs. {expense[1]:,.2f}"
        ])

    if not monthly_expenses:
        transaction_data.append([
            "-", "No expenses", "-", "Rs. 0.00"
        ])

    transaction_table = Table(
        transaction_data,
        colWidths=[1.1 * inch, 1.2 * inch, 2.2 * inch, 1.2 * inch],
        repeatRows=1
    )

    transaction_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B53")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("FONTSIZE", (0, 0), (-1, -1), 8)
    ]))

    elements.append(transaction_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("4. Savings Goals", styles["Heading2"])
    )

    savings_data = [
        ["Goal", "Target", "Saved", "Remaining"]
    ]

    for goal in savings_goals:
        goal_id, name, target, saved = goal

        savings_data.append([
            str(name),
            f"Rs. {target:,.2f}",
            f"Rs. {saved:,.2f}",
            f"Rs. {max(target - saved, 0):,.2f}"
        ])

    if not savings_goals:
        savings_data.append([
            "No goals", "-", "-", "-"
        ])

    savings_table = Table(
        savings_data,
        colWidths=[1.5 * inch, 1.3 * inch, 1.3 * inch, 1.3 * inch],
        repeatRows=1
    )

    savings_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B53")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("FONTSIZE", (0, 0), (-1, -1), 8)
    ]))

    elements.append(savings_table)

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "VAULT AI | Spend Smart. Save Smarter.",
            styles["Italic"]
        )
    )

    document.build(elements)

    return filename
