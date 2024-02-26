#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as    pd
import seaborn as   sns
import matplotlib.pyplot as plt


# In[21]:


df = pd.read_csv('./results.csv')
for i in [2,4,8,12,16,20,24,28,32,36,40,60,80]:
    df[f"S{i}"] = df['T1'] / df[f"T{i}"]


# In[22]:


df_20000 = pd.DataFrame(columns=["S", "T num"])
df_40000 = pd.DataFrame(columns=["S", "T num"])
for i in [2,4,8,12,16,20,24,28,32,36,40,60,80]:
    df_20000.loc[len(df_20000)] = [df.loc[0, f"S{i}"], int(i)]
    df_40000.loc[len(df_40000)] = [df.loc[1, f"S{i}"], int(i)]
df_20000["T num"] = df_20000["T num"].astype(int)
df_40000["T num"] = df_20000["T num"].astype(int)


# In[23]:


plt.figure(figsize=(10, 6))
plt.plot(df_20000["T num"], df_20000["S"], marker='o', label='M = 20000')
plt.plot(df_40000["T num"], df_40000["S"], marker='o', label='M = 40000')

# График y=x
plt.plot(df_20000["T num"], df_20000["T num"], linestyle='--', color='red', label='y=x')

plt.xlabel('T')
plt.ylabel('S')
plt.title('Dependency S on T')
plt.legend()
plt.xticks(df_20000["T num"])
plt.yticks(df_20000["S"])
plt.grid(True)
plt.savefig("plot.png")
