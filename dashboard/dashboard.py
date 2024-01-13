import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

all_df = pd.read_csv('all_data.csv')


def create_by_product_df(df):
    product_id_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_df = product_id_counts.sort_values(by='product_id', ascending=False)
    return sorted_df


def create_rfm(df):
   rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max", # mengambil tanggal order terakhir
    "review_creation_date": "nunique", # menghitung jumlah order
    "price": "sum" # menghitung jumlah revenue yang dihasilkan
})
   rfm_df.columns = ["customer_id", "max_order_timestamp", "Frequency", "monetary"]
   rfm_df['max_order_timestamp'] = pd.to_datetime(rfm_df['max_order_timestamp']).dt.date
   recent_date = pd.to_datetime(all_df["order_purchase_timestamp"]).dt.date.max()
   rfm_df["Recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
   return rfm_df


# SideBar

with st.sidebar:

    st.write('Copyright (C)')
    st.write('E-Commerce Public Dataset')

    
# calling functions
most_and_least_products_df=create_by_product_df(all_df)
rfm=create_rfm(all_df)


# Header

st.header('Brazilian Public Dataset :sparkles:')




# Top 5 Customer Cities 

top_cities = all_df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False).head(5)
st.subheader("Top Customer Cities")
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
plt.figure(figsize=(10, 6))
sns.barplot(x=top_cities.index, y=top_cities.values, palette=colors)
plt.title('Top 5 Customer Cities')
plt.xlabel('Customer City')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
st.pyplot(plt)

#  Most & Least Products 

st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Best Performing Product
product_id_counts = all_df.groupby('product_category_name_english')['product_id'].count().reset_index()
sorted_df = product_id_counts.sort_values(by='product_id', ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name_english", data=sorted_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("products with the highest sales", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="product_id", y="product_category_name_english", data=sorted_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("products with the lowest sales", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("most and least sold products", fontsize=20)
st.pyplot(plt)


#  Rating Customer By Service 
rating_service = all_df['review_score'].value_counts().sort_values(ascending=False)
st.subheader("Rating Customer By Service")
st.markdown(f"Rating Average  : **{rating_service.mean():.2f}**")
    

plt.figure(figsize=(10, 5))
sns.barplot(x=rating_service.index,
            y=rating_service.values,
            order=rating_service.index
            )

plt.title("Rating customers for service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Customer")
plt.xticks(fontsize=12)
st.pyplot(plt)


# RFM
st.subheader("RFM Best Value")
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

with tab1:
    plt.figure(figsize=(16, 8))
    sns.barplot(
        y="Recency", 
        x="customer_id", 
        data=rfm.sort_values(by="Recency", ascending=True).head(5), 
        palette=colors
    )
    
    plt.title("By Recency (Day)", loc="center", fontsize=18)
    plt.ylabel('')
    plt.xlabel("customer")
    plt.tick_params(axis ='x', labelsize=15)
    plt.xticks([])
    st.pyplot(plt)

with tab2:
    plt.figure(figsize=(16, 8))
    sns.barplot(
        y="Frequency", 
        x="customer_id", 
        data=rfm.sort_values(by="Frequency", ascending=False).head(5), 
        palette=colors
    )
    
    plt.ylabel('')
    plt.xlabel("customer")
    plt.title("By Frequency", loc="center", fontsize=18)
    plt.tick_params(axis ='x', labelsize=15)
    plt.xticks([])
    st.pyplot(plt)

with tab3:
    plt.figure(figsize=(16, 8))
    sns.barplot(
        y="monetary", 
        x="customer_id", 
        data=rfm.sort_values(by="monetary", ascending=False).head(5), 
        palette=colors
    )
    
    plt.ylabel('')
    plt.xlabel("customer")
    plt.title("By Monetary", loc="center", fontsize=18)
    plt.tick_params(axis ='x', labelsize=15)
    plt.xticks([])
    st.pyplot(plt)
