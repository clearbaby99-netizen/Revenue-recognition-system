"""
Group 3 - Task 3: Jupyter Notebook Data Analysis Demo
Each '# --- Cell N ---' marker below represents one Jupyter code cell.
Data comes from the Task 2 Revenue Recognition project.
"""

import pandas as pd

# --- Cell 1: Load the revenue data into a DataFrame ---
data = {
    "invoice_no": [1001, 1002, 1003],
    "client": ["Zimplow Holdings", "Delta Corporation", "Innscor Africa"],
    "project": ["Office Website Redesign", "ERP Support Retainer", "Warehouse Automation System"],
    "contract_type": ["Fixed-Price", "Time-and-Materials", "Cost-Plus"],
    "revenue": [9000.00, 6200.00, 35840.00],
}
df = pd.DataFrame(data)
print(df)

# --- Cell 2: Real-life question 1 - What is our total revenue recognised so far? ---
total_revenue = df["revenue"].sum()
print(f"\nTotal revenue recognised: ${total_revenue:,.2f}")

# --- Cell 3: Real-life question 2 - Which contract type is the biggest revenue driver? ---
by_type = df.groupby("contract_type")["revenue"].sum().sort_values(ascending=False)
print("\nRevenue by contract type:")
print(by_type)

# --- Cell 4: Real-life question 3 - Which single project generated the most revenue? ---
top_project = df.loc[df["revenue"].idxmax()]
print(f"\nTop-earning project: {top_project['project']} ({top_project['client']}) "
      f"-> ${top_project['revenue']:,.2f}")

# --- Cell 5: Real-life question 4 - What share of total revenue does each client represent? ---
df["pct_of_total"] = (df["revenue"] / total_revenue * 100).round(1)
print("\nRevenue share by client:")
print(df[["client", "revenue", "pct_of_total"]])
