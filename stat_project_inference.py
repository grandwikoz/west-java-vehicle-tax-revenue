#!/usr/bin/env python
# coding: utf-8

# On the basis of the revenue itself, capita and GDP basis, does vehicle tax revenue in West Java grow?

# In[92]:


# load data
import pandas as pd
import numpy as np

# visualization
import matplotlib.pyplot as plt
import seaborn as sns

# modelling
import statsmodels.formula.api as smf


# In[93]:


from ipynb.fs.full.stat_project_dataset import *


# In[94]:


data_kendaraan.head()


# In[95]:


data_jalan.head()


# In[96]:


data_penduduk.head()


# In[97]:


data_pdrb.head()


# In[98]:


# make a total column of tax revenue
data_kendaraan['total'] = data_kendaraan['PKB DENDA']+data_kendaraan['PKB POKOK']+data_kendaraan['BBNKB 1 DENDA']+data_kendaraan['BBNKB 1 POKOK']+data_kendaraan['BBNKB 2 DENDA']+data_kendaraan['BBNKB 2 POKOK']


# In[99]:


data_kendaraan.head()


# In[100]:


data_kendaraan.tail()


# In[101]:


pertumbuhan_pajak = data_kendaraan[['kode_kabupaten_kota', 'tahun', 'total']]


# In[102]:


pertumbuhan_pajak.head()


# In[103]:


# Create a column showing year-to-year percentage change in revenue collection
pertumbuhan_pajak['total_change'] = (pertumbuhan_pajak[['total']].pct_change()*100).round(2)


# In[104]:


pertumbuhan_pajak.head()


# In[105]:


# Drop the first year (2014)

pertumbuhan_pajak = pertumbuhan_pajak.drop(pertumbuhan_pajak[pertumbuhan_pajak['tahun']==2014].index)


# In[106]:


pertumbuhan_pajak.head()


# In[107]:


pertumbuhan_pajak.isnull().sum()


# In[108]:


pertumbuhan_pajak['tahun'].unique()


# In[109]:


# Create two arrays of revenue growth

pertumbuhan_pajak_2020 = pertumbuhan_pajak[pertumbuhan_pajak['tahun']==2020]['total_change'].values
pertumbuhan_pajak_2021 = pertumbuhan_pajak[pertumbuhan_pajak['tahun']==2021]['total_change'].values


# In[110]:


pertumbuhan_pajak_2020


# In[111]:


pertumbuhan_pajak_2021


# In[112]:


np.var(pertumbuhan_pajak_2020), np.var(pertumbuhan_pajak_2021)


# In[113]:


# Statistic test for revenue change
# Does 2020 revenue grow in 2021?

from scipy import stats
ttest_pertumbuhan = stats.ttest_ind(a = pertumbuhan_pajak_2021, 
                         b = pertumbuhan_pajak_2020, 
                         equal_var=False, 
                         alternative = "greater")


# In[114]:


ttest_pertumbuhan.pvalue


# In[115]:


ttest_pertumbuhan.statistic


# In[116]:


# Conclusion rule
if ttest_pertumbuhan.pvalue<0.05:
    print("Reject the null hypothesis")
else:
    print("Failed to reject the Null hypothesis")


# In[117]:


df_pertumbuhan = len(pertumbuhan_pajak_2021)+len(pertumbuhan_pajak_2020)-2
df_pertumbuhan


# In[118]:


# plot sample distribution 
x = np.arange(-4, 14, 0.001)
plt.plot(x, stats.t.pdf(x, df = df_pertumbuhan), 
         color='blue')

# plot alpha region
x_alpha = np.arange(stats.t.ppf(1-0.05, df = df_pertumbuhan), 4, 0.01)
y_alpha = stats.t.pdf(x_alpha, df = df_pertumbuhan)
plt.fill_between(x = x_alpha, 
                 y1 = y_alpha,
                 facecolor = 'red',
                 alpha = 0.35, 
                 label = 'alpha')

# plot pvalue
x_pvalue = np.arange(ttest_pertumbuhan.statistic, 4, 0.01)
y_pvalue = stats.t.pdf(x_pvalue, df = df_pertumbuhan)

plt.fill_between(x = x_pvalue, 
                 y1 = y_pvalue,
                 facecolor = 'green',
                 alpha = 0.35, 
                 label = 'pvalue')

# plot t-crit and t-stats
plt.axvline(np.round(ttest_pertumbuhan.statistic, 4), 
            color ="green", 
            linestyle = "--", 
            label ="t-stat")

t_crit = np.round(stats.t.ppf(1-0.05, df = df_pertumbuhan), 4)
plt.axvline(t_crit, 
            color ="red", 
            linestyle = "--", 
            label ="t-crit")

plt.legend()
plt.xlabel("t")
plt.ylabel("density")


plt.title(f't Distribution Plot with df = {df_pertumbuhan} \n\n t-statistic = {np.round(ttest_pertumbuhan.statistic, 4)}, t_crit = {np.round(t_crit,4)}, alpha = 0.05');


# In[119]:


# Array of current tax year

tahun_pertumbuhan_pajak = pertumbuhan_pajak['tahun'].unique().tolist()


# In[120]:


tahun_pertumbuhan_pajak


# In[121]:


# Array of subsequent tax year

tahun_pertumbuhan_pajak_2 = []
for tahun in tahun_pertumbuhan_pajak:
    tahun_2 = tahun + 1
    tahun_pertumbuhan_pajak_2.append(tahun_2)


# In[122]:


tahun_pertumbuhan_pajak_2


# In[123]:


# Build a dataframe to store statistic test of annual tax revenue change based on the revenue itself

ttest_pertumbuhan_pvalue = []
ttest_pertumbuhan_tstat = []
for tahun in tahun_pertumbuhan_pajak:
    pertumbuhan_pajak_1 = pertumbuhan_pajak[pertumbuhan_pajak['tahun']==tahun+1]['total_change'].values
    pertumbuhan_pajak_2 = pertumbuhan_pajak[pertumbuhan_pajak['tahun']==tahun]['total_change'].values
    ttest_pertumbuhan = stats.ttest_ind(a = pertumbuhan_pajak_1, 
                         b = pertumbuhan_pajak_2, 
                         equal_var=False, 
                         alternative = "greater")
    ttest_pertumbuhan_pvalue.append(ttest_pertumbuhan.pvalue)
    ttest_pertumbuhan_tstat.append(ttest_pertumbuhan.statistic)
    
    
ttest_pertumbuhan_all = {'tahun_1':tahun_pertumbuhan_pajak,'tahun_2':tahun_pertumbuhan_pajak_2, 'p_value':ttest_pertumbuhan_pvalue, 't_stat':ttest_pertumbuhan_tstat}
ttest_pertumbuhan_all = pd.DataFrame(ttest_pertumbuhan_all)


# In[124]:


ttest_pertumbuhan_all


# In[125]:


ttest_pertumbuhan_all = ttest_pertumbuhan_all.drop(ttest_pertumbuhan_all.tail(1).index)


# In[126]:


ttest_pertumbuhan_all


# In[127]:


data_pdrb.head()


# In[128]:


data_kendaraan.head()


# In[129]:


data_kendaraan['tahun']


# In[130]:


data_pdrb['tahun']=data_pdrb['tahun'].astype(int)
data_pdrb['tahun']


# In[131]:


data_penduduk['tahun'] = data_penduduk['tahun'].astype(int)
data_penduduk.info()


# In[132]:


pajak_to_pdrb = data_kendaraan[['kode_kabupaten_kota', 'tahun', 'total']].merge(data_pdrb[['kode_kabupaten_kota','tahun', 'jumlah']], on=['kode_kabupaten_kota', 'tahun']).merge(data_penduduk[['kode_kabupaten_kota', 'tahun', 'jumlah']], on=['kode_kabupaten_kota', 'tahun'])


# In[133]:


pajak_to_pdrb.head()


# In[134]:


pajak_to_pdrb = pajak_to_pdrb.rename(columns=str).rename(columns={'total':'pajak',
                                                                 'jumlah_x':'pdrb',
                                                                 'jumlah_y':'penduduk'})


# In[135]:


pajak_to_pdrb.head()


# In[136]:


pajak_to_pdrb['pdrb_total'] = pajak_to_pdrb['pdrb']*pajak_to_pdrb['penduduk']


# In[137]:


pajak_to_pdrb.head()


# In[138]:


# Calculating revenue to GDP percentage

pajak_to_pdrb['pajak_pct'] = (pajak_to_pdrb['pajak']/pajak_to_pdrb['pdrb_total']*100)


# In[139]:


pajak_to_pdrb.head()


# In[140]:


pajak_to_pdrb['tahun'].unique()


# In[141]:


# Create two arrays of revenue growth

pajak_to_pdrb_2019 = list(pajak_to_pdrb[pajak_to_pdrb['tahun']==2019]['pajak_pct'].values)
pajak_to_pdrb_2020 = list(pajak_to_pdrb[pajak_to_pdrb['tahun']==2020]['pajak_pct'].values)


# In[142]:


pajak_to_pdrb_2019


# In[143]:


pajak_to_pdrb_2020


# In[144]:


np.var(pajak_to_pdrb_2019), np.var(pajak_to_pdrb_2020)


# In[145]:


# Statistic test for revenue to RGDP change
# Does 2020 ratio grow in 2021?

ttest_pajak_to_pdrb = stats.ttest_ind(a = pajak_to_pdrb_2020, 
                         b = pajak_to_pdrb_2019, 
                         equal_var=False, 
                         alternative = "greater")


# In[146]:


ttest_pajak_to_pdrb.pvalue


# In[147]:


ttest_pajak_to_pdrb.statistic


# In[148]:


tahun_pajak_to_pdrb_1 = pajak_to_pdrb['tahun'].unique().tolist()


# In[149]:


tahun_pajak_to_pdrb_1


# In[150]:


tahun_pajak_to_pdrb_2 = []
for tahun in tahun_pajak_to_pdrb_1:
    tahun_2 = tahun + 1
    tahun_pajak_to_pdrb_2.append(tahun_2)


# In[151]:


tahun_pajak_to_pdrb_2


# In[152]:


# Build a dataframe to store statistic test of annual tax revenue change based on percentage to RGDP

ttest_pajak_to_pdrb_pvalue = []
ttest_pajak_to_pdrb_tstat = []
for tahun in tahun_pajak_to_pdrb_1:
    pajak_to_pdrb_1 = list(pajak_to_pdrb[pajak_to_pdrb['tahun']==tahun+1]['pajak_pct'].values)
    pajak_to_pdrb_2 = list(pajak_to_pdrb[pajak_to_pdrb['tahun']==tahun]['pajak_pct'].values)
    ttest_pajak_to_pdrb = stats.ttest_ind(a = pajak_to_pdrb_1, 
                         b = pajak_to_pdrb_2, 
                         equal_var=False, 
                         alternative = "greater")
    ttest_pajak_to_pdrb_pvalue.append(ttest_pajak_to_pdrb.pvalue)
    ttest_pajak_to_pdrb_tstat.append(ttest_pajak_to_pdrb.statistic)
    
    
ttest_pajak_to_pdrb_all = {'tahun_1':tahun_pajak_to_pdrb_1,'tahun_2':tahun_pajak_to_pdrb_2, 'p_value':ttest_pajak_to_pdrb_pvalue, 't_stat':ttest_pajak_to_pdrb_tstat}
ttest_pajak_to_pdrb_all = pd.DataFrame(ttest_pajak_to_pdrb_all)


# In[153]:


ttest_pajak_to_pdrb_all


# In[154]:


ttest_pajak_to_pdrb_all = ttest_pajak_to_pdrb_all.drop(ttest_pajak_to_pdrb_all.tail(1).index)


# In[155]:


ttest_pajak_to_pdrb_all


# In[156]:


data_penduduk.head()


# In[157]:


data_penduduk['tahun'].info()


# In[158]:


data_penduduk['tahun'] = data_penduduk['tahun'].astype(int)


# In[159]:


data_penduduk['tahun'].info()


# In[160]:


pajak_per_orang = data_kendaraan[['kode_kabupaten_kota', 'tahun', 'total']].merge(data_penduduk[['kode_kabupaten_kota','tahun', 'jumlah']], on=['kode_kabupaten_kota', 'tahun'])


# In[161]:


pajak_per_orang.head()


# In[162]:


pajak_per_orang = pajak_per_orang.rename(columns=str).rename(columns={'total':'pajak',
                                                                 'jumlah':'penduduk'})


# In[163]:


pajak_per_orang.head()


# In[164]:


pajak_per_orang['pajak_per_orang'] = pajak_per_orang['pajak']/pajak_per_orang['penduduk']


# In[165]:


pajak_per_orang.head()


# In[166]:


pajak_per_orang['tahun'].unique()


# In[167]:


pajak_per_orang_2020 = list(pajak_per_orang[pajak_per_orang['tahun']==2020]['pajak_per_orang'].values)
pajak_per_orang_2019 = list(pajak_per_orang[pajak_per_orang['tahun']==2019]['pajak_per_orang'].values)


# In[168]:


np.var(pajak_per_orang_2020), np.var(pajak_per_orang_2019)


# In[169]:


# Statistic test for revenue per capita change
# Does 2020 ratio grow in 2021?

ttest_pajak_per_orang = stats.ttest_ind(a = pajak_per_orang_2020, 
                         b = pajak_per_orang_2019, 
                         equal_var=False, 
                         alternative = "greater")


# In[170]:


ttest_pajak_per_orang.pvalue


# In[171]:


ttest_pajak_per_orang.statistic


# In[172]:


tahun_pajak_per_orang_1 = pajak_per_orang['tahun'].unique().tolist()
tahun_pajak_per_orang_2 = []
for tahun in tahun_pajak_per_orang_1:
    tahun_2 = tahun + 1
    tahun_pajak_per_orang_2.append(tahun_2)


# In[173]:


tahun_pajak_per_orang_1


# In[174]:


tahun_pajak_per_orang_2


# In[175]:


# Build a dataframe to store statistic test of annual tax revenue change on per capita basis

ttest_pajak_per_orang_pvalue = []
ttest_pajak_per_orang_tstat = []
for tahun in tahun_pajak_per_orang_1:
    pajak_per_orang_1 = list(pajak_per_orang[pajak_per_orang['tahun']==tahun+1]['pajak_per_orang'].values)
    pajak_per_orang_2 = list(pajak_per_orang[pajak_per_orang['tahun']==tahun]['pajak_per_orang'].values)
    ttest_pajak_per_orang = stats.ttest_ind(a = pajak_per_orang_1, 
                         b = pajak_per_orang_2, 
                         equal_var=False, 
                         alternative = "greater")
    ttest_pajak_per_orang_pvalue.append(ttest_pajak_per_orang.pvalue)
    ttest_pajak_per_orang_tstat.append(ttest_pajak_per_orang.statistic)
    
    
ttest_pajak_per_orang_all = {'tahun_1':tahun_pajak_per_orang_1,'tahun_2':tahun_pajak_per_orang_2, 'p_value':ttest_pajak_per_orang_pvalue, 't_stat':ttest_pajak_per_orang_tstat}
ttest_pajak_per_orang_all = pd.DataFrame(ttest_pajak_per_orang_all)


# In[176]:


ttest_pajak_per_orang_all


# In[177]:


ttest_pajak_per_orang_all = ttest_pajak_per_orang_all.drop(ttest_pajak_per_orang_all.tail(1).index)


# In[178]:


ttest_pajak_per_orang_all


# Based on this test, we could safely say that there is no sufficient ground to say that there is an increase in revenue per capita in West Java for 2014 - 2019. T Test gives us large P values for all available years.

# In[179]:


ttest_pertumbuhan_all


# Based on this test, there is a mixed result of t test on tax revenue growth in West Java. In 2015, 2018 and 2020 there is a strong evidence to believe that a growth did happen while in 2016, 2017 and 2019 there is not much case for such.

# In[180]:


ttest_pajak_to_pdrb_all


# Based on this test, we could safely say that there is no sufficient ground to say that there is an increase in revenue to RGDP in West Java for 2014 - 2019. T Test gives us large P values for all available years.
