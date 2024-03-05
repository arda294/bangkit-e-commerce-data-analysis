import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import locale

orders_with_payments = pd.read_csv('dashboard/orders_with_payments.csv')
orders_df = pd.read_csv('dashboard/orders.csv')
orders_with_payments['order_approved_at'] = pd.to_datetime(orders_with_payments['order_approved_at'])
orders_df['order_approved_at'] = pd.to_datetime(orders_df['order_approved_at'])
customer_rfm = pd.read_csv('dashboard/customer_rfm.csv')

st.title('E-Commerce Data Analysis :sparkle:')

col1, col2 = st.columns(2)

with col1:
    st.metric('Total Orders', orders_with_payments.size)

with col2:
    income = orders_with_payments.payment_value.sum()
    st.metric('Total Income', "${:,.2f}".format(income))

orders_by_date = orders_with_payments.groupby(pd.Grouper(key='order_approved_at', freq='M')).agg(
    income=('payment_value', 'sum')
).reset_index()

print(orders_by_date)

plt.figure(figsize=(8,4))
plot = sns.lineplot(orders_by_date, x='order_approved_at', y=orders_by_date.income.apply(lambda x: x/1000))
plot.set_title('Income Over Time')
plot.set_xlabel('Time')
plot.set_ylabel('Income (Thousand)')
st.pyplot(plot.get_figure())

st.subheader('Growth per Month in 2017')

col1, col2 = st.columns(2)

orders_2017 = orders_df[orders_df['order_approved_at'].dt.year == 2017]
orders_by_month_2017 = orders_2017['order_approved_at'].groupby(orders_2017['order_approved_at'].dt.month).count()

with col1:
    st.metric('Total Orders in 2017', orders_2017.size)

with col2:
    percent_growth = ((orders_by_month_2017[12] - orders_by_month_2017[1]) / orders_by_month_2017[1]) * 100
    st.metric('Growth in 2017', "{:.2f}%".format(percent_growth))

plot = sns.barplot(orders_by_month_2017, palette=sns.color_palette("husl", 2))
plot.set_title('Orders in 2017')
plot.set_xlabel('Month of the year')
plot.set_ylabel('Order Count')
plot.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des'])
st.pyplot(plot.get_figure())

with st.expander('See Explanation'):
    st.markdown("""
        We can see that there is a significant growth on the number of orders that reaches 693.71%. This can be further explained with RFM Analysis.
    """)

st.subheader('RFM Analysis')

st.markdown('#### Frequency (purchase) of Users')

plt.figure(figsize=(8,4))
plot = sns.histplot(customer_rfm['frequency'], bins=30)
plt.xlabel('Frequency')
plt.ylabel('User Count')
plt.title('User Buying Frequency Distribution')
st.pyplot(plot.get_figure())

with st.expander('See Explanation'):
    st.markdown("""
        Most of the users of this E-Commerce only buy Once or twice, over 96.71% of users only buy once. The data from the above histogram is filtered to have only repeat buyers.
    """)

st.markdown('#### Recency (Time since last purchase) of Users')

plt.figure(figsize=(8,4))
plot = sns.histplot(customer_rfm['recency'], bins=20)
plt.xlabel('Recency (Days)')
plt.ylabel('User Count')
plt.title('User Buying Recency Distribution')
st.pyplot(plot.get_figure())

with st.expander('See Explanation'):
    st.markdown("""
        We can infer from this recency histogram that most of repeat buyers have either bought recently or in the last 6-10 months. This insinuate that
        the E-Commerce has low user retention.
    """)

st.markdown('#### Monetary (Total Spending) of Users')

plt.figure(figsize=(8,4))
plot = sns.histplot(customer_rfm['monetary'], bins=20)
plt.xlabel('Monetary (Total Spending in USD)')
plt.ylabel('User Count')
plt.title('User Total Spending Distribution')
st.pyplot(plot.get_figure())

with st.expander('See Explanation'):
    st.markdown("""
        The monetary of users also reflects the amount of new users that use this E-Commerce. Hence why we see the histogram to be right skewed.
    """)

st.markdown('#### Segmentation based on RFM scores')

plt.figure(figsize=(14, 6))
plot = sns.barplot(customer_rfm['segment_result'].value_counts(), palette=sns.color_palette("husl", 8))
plt.title('User Segmentation')
plt.ylabel('User Count')
plt.xlabel('RFM Segment')
st.pyplot(plot.get_figure())

with st.expander('See Explanation'):
    st.markdown("""
        As we have learned before, this E-Commerce has alot of new customers. Most of the old customers are hibernating meaning that they spent a little amount and haven't
        spent in a long time. And the number of hibernating customer could increase based on the segment about to sleep. These are the users that haven't spent recently but have low frequency. We have many promising users meaning that they spent averagely but they spent pretty recently. This is to be suspected since we know that this
        E-Commerce have alot of new customers. We can also link the number of new customers to the growth of income in 2017. This E-Commerce has a low number of loyal users and champions (those who spent very recently and frequently).
        
        Based on all of this, we can infer that this E-Commerce has a low number of user retention. The cause of this can be further investigated using this dataset or by other means necessary.
    """)