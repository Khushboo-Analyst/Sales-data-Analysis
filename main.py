import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = r"C:\Users\bkhus\OneDrive\Documents\python_test_dataset_flights_6months.csv"
df = pd.read_csv(file_path)

# Convert booking_date to datetime format for analysis
df['booking_date'] = pd.to_datetime(df['booking_date'], format='%d-%m-%Y')

# Short-term Analysis

# 1. Total Sales by Payment Method
# Group by payment method and sum up the selling prices
payment_sales = df.groupby("payment_method")["selling_price"].sum().reset_index()

# Plotting total sales by payment method
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='payment_method', y='selling_price', data=payment_sales)

# Adding data labels on the bars for better readability
for p in ax.patches:
    ax.annotate(f'₹{p.get_height():,.0f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 5),
                textcoords='offset points')

plt.title('Total Sales by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# 2. Refund Status Analysis
# Analyze refund status to get count and average amount
refund_analysis = df.groupby("refund_status").agg(
    refund_count=('refund_amount', 'count'),
    avg_refund_amount=('refund_amount', 'mean')
).reset_index()

# Plotting refund count by refund status
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='refund_status', y='refund_count', data=refund_analysis, color='salmon')

# Adding data labels on the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.0f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 5),
                textcoords='offset points')

plt.title('Refund Count by Refund Status')
plt.xlabel('Refund Status')
plt.ylabel('Count')
plt.show()

# Plotting average refund amount by refund status
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='refund_status', y='avg_refund_amount', data=refund_analysis, color='skyblue')

# Adding data labels on the bars
for p in ax.patches:
    ax.annotate(f'₹{p.get_height():,.2f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 5),
                textcoords='offset points')

plt.title('Average Refund Amount by Refund Status')
plt.xlabel('Refund Status')
plt.ylabel('Average Refund Amount')
plt.show()

# 3. Sales Channel Performance
# Group by channel and sum up the selling prices
channel_performance = df.groupby("channel_of_booking")["selling_price"].sum().reset_index()

# Plotting sales channel performance
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='channel_of_booking', y='selling_price', data=channel_performance)

# Adding data labels on the bars
for p in ax.patches:
    ax.annotate(f'₹{p.get_height():,.2f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 5),
                textcoords='offset points')

plt.title('Sales Channel Performance')
plt.xlabel('Channel of Booking')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# 4. Monthly Revenue
# Group by month and sum up the selling prices
monthly_revenue = df.groupby(df['booking_date'].dt.to_period("M"))["selling_price"].sum().reset_index()
monthly_revenue.columns = ['Month', 'Monthly_Revenue']

# Convert 'Month' to string for plotting
monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)
monthly_revenue['Monthly_Revenue'] = pd.to_numeric(monthly_revenue['Monthly_Revenue'], errors='coerce')
monthly_revenue = monthly_revenue.dropna(subset=['Monthly_Revenue'])

# Plotting monthly revenue
plt.figure(figsize=(12, 6))
ax= sns.lineplot(x='Month', y='Monthly_Revenue', data=monthly_revenue, marker='o')

# Add labels on data points
for i in range(len(monthly_revenue)):
    ax.text(monthly_revenue['Month'].iloc[i],
            monthly_revenue['Monthly_Revenue'].iloc[i],
            f'₹{monthly_revenue["Monthly_Revenue"].iloc[i]:,.0f}',
            ha='center',
            va='bottom')

plt.title('Monthly Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.show()

# 5. Weekly Revenue
# Group by week and sum up the selling prices
weekly_revenue = df.groupby(df['booking_date'].dt.to_period("W"))["selling_price"].sum().reset_index()
weekly_revenue.columns = ['Week', 'Weekly_Revenue']

# Convert 'Week' to string for plotting
weekly_revenue['Week'] = weekly_revenue['Week'].astype(str)
weekly_revenue['Weekly_Revenue'] = pd.to_numeric(weekly_revenue['Weekly_Revenue'], errors='coerce')
weekly_revenue = weekly_revenue.dropna(subset=['Weekly_Revenue'])

# Plotting weekly revenue
plt.figure(figsize=(12, 6))
ax = sns.lineplot(x='Week', y='Weekly_Revenue', data=weekly_revenue, marker='o')

# Add labels on data points
for i in range(len(weekly_revenue)):
    ax.text(weekly_revenue['Week'].iloc[i],
            weekly_revenue['Weekly_Revenue'].iloc[i],
            f'₹{weekly_revenue["Weekly_Revenue"].iloc[i]:,.0f}',
            ha='center',
            va='top',
            rotation=90)

plt.title('Weekly Revenue')
plt.xlabel('Week')
plt.ylabel('Revenue')
plt.xticks(rotation=90)
plt.show()

# 6. Coupon Effectiveness
# Calculate average selling price based on coupon usage
coupon_effectiveness = df.groupby("Coupon USed?")["selling_price"].mean().reset_index()

# Calculate coupon usage proportions for pie chart
coupon_counts = df["Coupon USed?"].value_counts()

# Plotting coupon usage proportions
plt.figure(figsize=(8, 8))
plt.pie(coupon_counts, labels=coupon_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Coupon Usage Proportion')
plt.show()

# 7. Customer Loyalty Analysis
# Determine loyal customers who made more than one purchase in the last 60 days
df = df.sort_values(by=['buyer_id', 'booking_date'])
df['prev_booking_date'] = df.groupby('buyer_id')['booking_date'].shift(1)
df['days_between_bookings'] = (df['booking_date'] - df['prev_booking_date']).dt.days
loyal_customers = df[df['days_between_bookings'] <= 60]['buyer_id'].unique()
df['is_loyal'] = df['buyer_id'].isin(loyal_customers)

# Summarize customer data
customer_summary = df.groupby('buyer_id').agg({
    'selling_price': 'sum',
    'refund_amount': 'sum',
    'is_loyal': 'max',
    'days_between_bookings': 'mean'
})

print(customer_summary)

# Plotting Customer Loyalty vs Selling Price
plt.figure(figsize=(12, 6))
sns.boxplot(x='is_loyal', y='selling_price', data=df)
plt.title('Customer Loyalty vs Selling Price')
plt.xlabel('Is Loyal')
plt.ylabel('Selling Price (₹)')
plt.show()

# Plotting Customer Loyalty vs Refund Amount
plt.figure(figsize=(12, 6))
sns.boxplot(x='is_loyal', y='refund_amount', data=df)
plt.title('Customer Loyalty vs Refund Amount')
plt.xlabel('Is Loyal')
plt.ylabel('Refund Amount (₹)')
plt.show()

# 8. Total Revenue, Profit, and Refunds
# Calculate total profit and refunds
df['profit'] = df['selling_price'] - df['costprice'] - df[df['refund_status'] == 'Yes']['refund_amount']
total_revenue = df['selling_price'].sum()
total_profit = df['profit'].sum()
total_refund = df[df['refund_status'] == 'Yes']['refund_amount'].sum()

# Create a DataFrame for metrics and plot
plt.figure(figsize=(10, 6))
metrics = pd.DataFrame({
    'Metric': ['Total Revenue', 'Total Profit', 'Total Refund'],
    'Amount': [total_revenue, total_profit, total_refund]
})
ax = sns.barplot(x='Metric', y='Amount', data=metrics)

# Adding data labels on the bars
for p in ax.patches:
    ax.annotate(f'₹{p.get_height():,.0f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center',
                va='center_baseline',
                xytext=(0, 10),  # Offset label slightly above the bar
                textcoords='offset points')

plt.title('Total Revenue, Profit, and Refunds')
plt.xlabel('Metric')
plt.ylabel('Amount (₹)')
plt.show()



