#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# Load the dataset
df = pd.read_csv("flipkart_smartphones.csv")


# In[3]:


# top 5 rows
df.head(5)


# In[4]:


# check info
print(df.info())


# In[5]:


df.isnull().sum()


# In[6]:


df.isnull().sum().sum()


# In[7]:


# Drop completely empty columns
df = df.dropna(axis=1, how='all')


# In[8]:


# Fill missing numerical values with median
for col in ["memory", "storage", "battery_capacity"]:
    df[col] = df[col].fillna(df[col].median())


# In[9]:


# Fill missing categorical values with "Unknown"
for col in ["colour", "processor", "front_camera", "battery_type"]:
    df[col] = df[col].fillna("Unknown")


# In[10]:


# Drop duplicate entries
df = df.drop_duplicates()


# In[11]:


# Check dataset info
print(df.info())


# In[12]:


df.to_csv('updated_data.csv')


# In[13]:


plt.figure(figsize=(8, 5))
sns.histplot(df["discounted_price"], bins=30, kde=True, color="blue")
plt.title("Price Distribution of Smartphones")
plt.xlabel("Discounted Price (INR)")
plt.ylabel("Count")
plt.show()


# In[14]:


plt.figure(figsize=(10, 5))
brand_counts = df["brand"].value_counts().head(10)  # Top 10 brands
sns.barplot(x=brand_counts.index, y=brand_counts.values, palette="viridis")
plt.xticks(rotation=45)
plt.title("Top 10 Smartphone Brands by Count")
plt.xlabel("Brand")
plt.ylabel("Number of Smartphones")
plt.show()


# In[15]:


plt.figure(figsize=(10, 5))
brand_ratings = df.groupby("brand")["ratings"].mean().sort_values(ascending=False).head(10)
sns.barplot(x=brand_ratings.index, y=brand_ratings.values, palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Top 10 Brands by Average Rating")
plt.xlabel("Brand")
plt.ylabel("Average Rating")
plt.ylim(3.5, 5)  # Rating scale
plt.show()


# In[16]:


plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["discounted_price"], y=df["ratings"], alpha=0.5, color="red")
plt.title("Price vs. Ratings")
plt.xlabel("Discounted Price (INR)")
plt.ylabel("Ratings")
plt.show()


# In[17]:


plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["battery_capacity"], y=df["discounted_price"], alpha=0.5, color="blue")
plt.title("Battery Capacity vs. Price (Scatter Plot)")
plt.xlabel("Battery Capacity (mAh)")
plt.ylabel("Discounted Price (INR)")
plt.show()


# In[ ]:




