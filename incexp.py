import streamlit as st
import sqlite3
import plotly.graph_objects as go
import pandas as pd

# Function to create the database and table if it doesn't exist
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert dummy data (only run this once to populate the database)
def insert_dummy_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)", 
              ("Sample Expense", 1000.50, "2025-04-17"))
    conn.commit()
    conn.close()

# Function to fetch expenses from the database
def fetch_expenses():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = c.fetchall()
    conn.close()
    return expenses

# Function to calculate total income, expenses, and remaining income
def calculate_totals(expenses):
    total_expenses = sum([expense[2] for expense in expenses])  # Assuming amount is in column 2
    total_income = 1000  # Replace with actual total income or fetch from another table
    remaining_income = total_income - total_expenses
    return total_income, total_expenses, remaining_income

# Function to format money in INR (Indian Rupees)
def format_inr(amount):
    return f"₹ {amount:,.2f}"

# Function to plot expenses over time using Plotly
def plot_expenses(expenses):
    # Assuming date is in column 3 and amount is in column 2
    dates = [expense[3] for expense in expenses]
    amounts = [expense[2] for expense in expenses]

    # Create a plot using Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=amounts, mode='lines+markers', name='Expense Amount'))

    # Customize the layout
    fig.update_layout(
        title="Expenses Over Time",
        xaxis_title="Date",
        yaxis_title="Amount (INR)",
        xaxis=dict(tickmode='linear'),
        template='plotly_dark'
    )

    return fig

# Main Streamlit app
def main():
    # Initialize the database and create the table if not exists
    init_db()

    # Uncomment below line to insert dummy data only once
    # insert_dummy_data()

    # Fetch the data from the database
    expenses = fetch_expenses()

    # Calculate totals (you can replace total_income with actual data)
    total_income, total_expenses, remaining_income = calculate_totals(expenses)

    # Show totals on the Streamlit app
    st.write(f"### Total Income: {format_inr(total_income)}")
    st.write(f"### Total Expenses: {format_inr(total_expenses)}")
    st.write(f"### Remaining Income: {format_inr(remaining_income)}")

    # Plot the expense graph using Plotly
    fig = plot_expenses(expenses)
    st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
