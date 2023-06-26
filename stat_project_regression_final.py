#!/usr/bin/env python
# coding: utf-8

# What is the relationship between tax revenue in West Java and some correlated variables, namely total population, total vehicles, GRDP, road category and road condition?

# In[1]:


# pandas and numpy
import pandas as pd
import numpy as np

# visualization
import matplotlib.pyplot as plt
import seaborn as sns

# modelling
import statsmodels.formula.api as smf

# cross validation using statsmodel prepartion
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score, cross_validate, KFold

# ignore warnings
import warnings
warnings.simplefilter('ignore')


# In[2]:


def print_coef_std_err(results):
    """
    Function to combine estimated coefficients and standard error in one DataFrame
    :param results: <statsmodels RegressionResultsWrapper> OLS regression results from statsmodel
    :return df: <pandas DataFrame>  combined estimated coefficient and standard error of model estimate
    """
    coef = results.params
    std_err = results.bse
    
    df = pd.DataFrame(data = np.transpose([coef, std_err]), 
                      index = coef.index, 
                      columns=["coef","std err"])
    return df

class StatsmodelsRegressor(BaseEstimator, RegressorMixin):
    """ A universal sklearn-style wrapper for statsmodels regressors """
    
    def __init__(self, sm_class, sm_formula):
        self.sm_class = sm_class
        self.sm_formula = sm_formula
        self.model = None
        self.result = None
 
    def fit(self, data, dummy):
        self.model = self.sm_class(self.sm_formula, data)
        self.result = self.model.fit()
 
    def predict(self,X):
        return self.result.predict(X)

def kfold_split(data, n_fold):
    """
    Function to combine estimated coefficients and standard error in one DataFrame
    :param data: <pandas DataFrame> 
    :param n_fold: <int> Number of fold in k-fold CV
    :return fold_train: <pandas DataFrame> Training Data
    :return fold_test: <pandas DataFrame> Testing Data
    """
    kfold = KFold(n_splits = n_fold, 
                  shuffle = True, 
                  random_state=123)
    fold_train = {}
    fold_test = {}

    for i, (train, test) in enumerate(kfold.split(data)):
        print(f"fold {i+1}, train data rows: {len(train)}, test data rows: {len(test)}")
        fold_train[i] = data.iloc[train].copy()
        fold_test[i] = data.iloc[test].copy()
        
    return (fold_train, fold_test)


# In[3]:


# make kfold variable with 5 splits
kfold = KFold(n_splits=5, shuffle = True, random_state=123)


# In[4]:


# upload dataset

from ipynb.fs.full.stat_project_dataset import *


# In[5]:


data_penduduk.info()


# In[6]:


data_penduduk['tahun'] = data_penduduk['tahun'].astype(int)
data_penduduk['jumlah'] = data_penduduk['jumlah'].astype(int)


# In[7]:


data_penduduk.info()


# In[8]:


data_penduduk.head()


# In[9]:


data_pdrb.info()


# In[10]:


data_pdrb['tahun'] = data_pdrb['tahun'].astype(int)
data_pdrb['jumlah'] = data_pdrb['jumlah'].astype(int)


# In[11]:


data_pdrb.info()


# In[12]:


data_pdrb.head()


# In[13]:


data_kendaraan.info()


# In[14]:


data_kendaraan['total_pajak'] = data_kendaraan['PKB DENDA']+data_kendaraan['PKB POKOK']+data_kendaraan['BBNKB 1 DENDA']+data_kendaraan['BBNKB 1 POKOK']+data_kendaraan['BBNKB 2 DENDA']+data_kendaraan['BBNKB 2 POKOK']
data_kendaraan['total_kendaraan'] = data_kendaraan['fungsi_dinas']+data_kendaraan['fungsi_pribadi']+data_kendaraan['fungsi_umum']


# In[15]:


data_kendaraan.info()


# In[16]:


data_kendaraan.head()


# In[17]:


data_jalan.info()


# In[18]:


data_jalan.head()


# In[19]:


# show which road quality counts the most

data_jalan[['BAIK', 'RUSAK BERAT', 'RUSAK RINGAN', 'SEDANG']].idxmax(axis=1).value_counts()


# In[20]:


data_jalan['kondisi_max'] = data_jalan[['BAIK', 'RUSAK BERAT', 'RUSAK RINGAN', 'SEDANG']].idxmax(axis=1)


# In[21]:


data_jalan.head()


# In[22]:


# show which road material counts the most

data_jalan[['aspal', 'lainnya', 'tidak_aspal']].idxmax(axis=1).value_counts()


# In[23]:


data_jalan['jenis_max'] = data_jalan[['aspal', 'lainnya', 'tidak_aspal']].idxmax(axis=1)


# In[24]:


data_jalan.head()


# In[25]:


# show which road authority category counts the most and since there is only one, it is deemed unproper to use it as variable

data_jalan[['wewenang_kabkota', 'wewenang_negara', 'wewenang_provinsi']].idxmax(axis=1).value_counts()


# In[26]:


reg_model_data = data_kendaraan[['kode_kabupaten_kota', 'tahun', 'total_pajak', 'total_kendaraan']].merge(data_pdrb[['kode_kabupaten_kota','tahun', 'jumlah']], on=['kode_kabupaten_kota', 'tahun']).merge(data_penduduk[['kode_kabupaten_kota', 'tahun', 'jumlah']], on=['kode_kabupaten_kota', 'tahun']).merge(data_jalan[['kode_kabupaten_kota', 'tahun', 'kondisi_max', 'jenis_max']], on=['kode_kabupaten_kota', 'tahun'])


# In[27]:


reg_model_data.info()


# In[28]:


reg_model_data.head()


# In[29]:


reg_model_data = reg_model_data.rename(columns={'jumlah_x':'pdrb_per_kapita',
                                               'jumlah_y':'jumlah_penduduk'})


# In[30]:


reg_model_data.head()


# In[31]:


reg_model_data['kendaraan_per_kapita'] = reg_model_data['total_kendaraan']/reg_model_data['jumlah_penduduk']


# In[32]:


reg_model_data = reg_model_data[['kode_kabupaten_kota', 'tahun', 'total_pajak', 'total_kendaraan', 'kendaraan_per_kapita', 'pdrb_per_kapita', 'jumlah_penduduk', 'kondisi_max', 'jenis_max']]


# In[33]:


reg_model_data.head()


# In[34]:


reg_model_data[['total_pajak', 'kendaraan_per_kapita', 'pdrb_per_kapita', 'jumlah_penduduk']].corr()


# In[35]:


sns.heatmap(reg_model_data[['total_pajak', 'kendaraan_per_kapita', 'pdrb_per_kapita', 'jumlah_penduduk']].corr(), vmin=-1, vmax=1, annot=True)


# As shown on the heatmap, there is a high correlation between two predictors, namely pdrb_per_kapita and kendaraan_per_kapita. Nevertheless, let's try to use all available predictors first and see what we'll get.

# In[36]:


# build a weighted model using total_kendaraan as weight
model_1 = smf.wls("total_pajak ~ kendaraan_per_kapita + pdrb_per_kapita + jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))",reg_model_data, weights=reg_model_data['total_kendaraan'])
result_1 = model_1.fit()


# In[37]:


print_coef_std_err(result_1)


# In[38]:


result_1.summary()


# In[39]:


result_model_1 = StatsmodelsRegressor(smf.ols, "total_pajak ~ kendaraan_per_kapita + pdrb_per_kapita + jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))")


# In[40]:


result_score_1 = cross_val_score(estimator = result_model_1,
                                       X = reg_model_data,
                                       y = reg_model_data["total_pajak"],
                                       cv = kfold,
                                       scoring = "r2")
result_score_1 = pd.DataFrame(data = result_score_1, 
                                    columns=["test_rsquared"])
result_score_1["folds"] = [f"Folds {i+1}" for i in range(5)]
result_score_1


# As shown on the summary and r squared test, even though we have a high r squared, there is an indication of a collinearity.
# Let's try with excluding pdrb_per_kapita since it has a very high P Value.

# In[41]:


# build a weighted model using total_kendaraan as weight excluding pdrb_per_kapita
model_2 = smf.wls("total_pajak ~ kendaraan_per_kapita + jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))",reg_model_data, weights=reg_model_data['total_kendaraan'])
result_2 = model_2.fit()


# In[42]:


print_coef_std_err(result_2)


# In[43]:


result_2.summary()


# In[44]:


result_model_2 = StatsmodelsRegressor(smf.ols, "total_pajak ~ kendaraan_per_kapita + jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))")


# In[45]:


result_score_2 = cross_val_score(estimator = result_model_2,
                                       X = reg_model_data,
                                       y = reg_model_data["total_pajak"],
                                       cv = kfold,
                                       scoring = "r2")
result_score_2 = pd.DataFrame(data = result_score_2, 
                                    columns=["test_rsquared"])
result_score_2["folds"] = [f"Folds {i+1}" for i in range(5)]
result_score_2


# Excluding pdrb_per_kapita doesn't necessarily imporve r squared not does it eliminate indication of multicollinearity. Let's try log transformation to see if we can fix this.

# In[46]:


reg_model_data_log = reg_model_data.copy()


# In[47]:


reg_model_data_log.head()


# In[48]:


reg_model_data_log['total_pajak'] = np.log(reg_model_data_log['total_pajak'])
reg_model_data_log['total_kendaraan'] = np.log(reg_model_data_log['total_kendaraan'])
reg_model_data_log['kendaraan_per_kapita'] = np.log(reg_model_data_log['kendaraan_per_kapita'])
reg_model_data_log['pdrb_per_kapita'] = np.log(reg_model_data_log['pdrb_per_kapita'])
reg_model_data_log['jumlah_penduduk'] = np.log(reg_model_data_log['jumlah_penduduk'])


# In[49]:


reg_model_data_log = reg_model_data_log.rename(columns={'total_pajak':'log_total_pajak',
                                                        'total_kendaraan':'log_total_kendaraan',
                                               'kendaraan_per_kapita':'log_kendaraan_per_kapita',
                                                     'pdrb_per_kapita':'log_pdrb_per_kapita',
                                                     'jumlah_penduduk':'log_jumlah_penduduk'})


# In[50]:


reg_model_data_log.head()


# In[51]:


sns.heatmap(reg_model_data_log[['log_total_pajak', 'log_kendaraan_per_kapita', 'log_pdrb_per_kapita', 'log_jumlah_penduduk']].corr(), vmin=-1, vmax=1, annot=True)


# As we can see, there is still a high correlation between pdrb_per_kapita and kendaraan_per_kapita even after log transformation.

# In[52]:


model_3 = smf.ols("log_total_pajak ~ log_kendaraan_per_kapita + log_pdrb_per_kapita + log_jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))",reg_model_data_log)
result_3 = model_3.fit()


# In[53]:


print_coef_std_err(result_3)


# In[54]:


result_3.summary()


# In[55]:


result_model_3 = StatsmodelsRegressor(smf.ols, "log_total_pajak ~ log_kendaraan_per_kapita + log_pdrb_per_kapita + log_jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))")


# In[56]:


result_score_3 = cross_val_score(estimator = result_model_3,
                                       X = reg_model_data_log,
                                       y = reg_model_data_log["log_total_pajak"],
                                       cv = kfold,
                                       scoring = "r2")
result_score_3 = pd.DataFrame(data = result_score_3, 
                                    columns=["test_rsquared"])
result_score_3["folds"] = [f"Folds {i+1}" for i in range(5)]
result_score_3


# Both summary and r squared test show a significant improvement of r squared. Not just that, pdrb_per_kapita in in log form shows a tiny enough value of just 0.02 which will pass a significance test of 5%. Still, we have a collinearity problem here. Let's see if excluding pdrb_per_kapita or kendaraan_per_kapita will finally fix this problem.

# In[57]:


model_4 = smf.ols("log_total_pajak ~  log_pdrb_per_kapita + log_jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))",reg_model_data_log)
result_4 = model_4.fit()


# In[58]:


print_coef_std_err(result_4)


# In[59]:


result_4.summary()


# In[60]:


result_model_4 = StatsmodelsRegressor(smf.ols, "log_total_pajak ~  log_pdrb_per_kapita + log_jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))")


# In[61]:


result_score_4 = cross_val_score(estimator = result_model_4,
                                       X = reg_model_data_log,
                                       y = reg_model_data_log["log_total_pajak"],
                                       cv = kfold,
                                       scoring = "r2")
result_score_4 = pd.DataFrame(data = result_score_4, 
                                    columns=["test_rsquared"])
result_score_4["folds"] = [f"Folds {i+1}" for i in range(5)]
result_score_4


# A clear improvement on the aspect of collinearity but through sacrifice of r squared which goes down quite significantly.

# In[62]:


model_5 = smf.ols("log_total_pajak ~  log_kendaraan_per_kapita + log_jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))",reg_model_data_log)
result_5 = model_5.fit()


# In[63]:


print_coef_std_err(result_5)


# In[64]:


result_5.summary()


# Using model_5, we could describe the model as:
# 
# log_total_pajak = 12.308 - 0.1776(C(tahun, reference='tahun') - 0.0242(C(jenis_max, reference='aspal') - 0.0601(C(kondisi_max, reference='BAIK') + 1.17164 X log_kendaraan_per_kapita + 1.1398 X log_jumlah_penduduk

# In[65]:


result_model_5 = StatsmodelsRegressor(smf.ols, "log_total_pajak ~  log_kendaraan_per_kapita + log_jumlah_penduduk + C(tahun, Treatment(reference=2019)) + C(jenis_max, Treatment(reference='aspal')) + C(kondisi_max, Treatment(reference='BAIK'))")


# In[66]:


result_score_5 = cross_val_score(estimator = result_model_5,
                                       X = reg_model_data_log,
                                       y = reg_model_data_log["log_total_pajak"],
                                       cv = kfold,
                                       scoring = "r2")
result_score_5 = pd.DataFrame(data = result_score_5, 
                                    columns=["test_rsquared"])
result_score_5["folds"] = [f"Folds {i+1}" for i in range(5)]
result_score_5


# We can see that P Value for jenis_max and kondisi_max is way too high and therefore unrelevant for the model. Ignoring those two, this model eliminates both the problem of deterioration of r squared and collinerarity. Thus we will use this as the final model and plot the prediction against observation.

# In[67]:


# Creating variables to store constant predictors

bukan_tahun_2019 = result_5.params['C(tahun, Treatment(reference=2019))[T.2020]']
bukan_jenis_aspal = result_5.params["C(jenis_max, Treatment(reference='aspal'))[T.lainnya]"]
bukan_kondisi_baik = result_5.params["C(kondisi_max, Treatment(reference='BAIK'))[T.SEDANG]"]


# In[68]:


bukan_tahun_2019


# In[69]:


bukan_jenis_aspal


# In[70]:


bukan_kondisi_baik


# In[71]:


# Creating prediction column using predictors from result_5

reg_model_data_log['prediction'] = result_5.params['Intercept'] + reg_model_data_log['tahun'].apply(lambda x: 0 if x == 2019 else bukan_tahun_2019) + reg_model_data_log['jenis_max'].apply(lambda x: 0 if x == 'aspal' else bukan_jenis_aspal) + reg_model_data_log['kondisi_max'].apply(lambda x: 0 if x == 'BAIK' else bukan_kondisi_baik) + reg_model_data_log['log_kendaraan_per_kapita']*result_5.params['log_kendaraan_per_kapita'] + reg_model_data_log['log_jumlah_penduduk']*result_5.params['log_jumlah_penduduk']


# In[72]:


reg_model_data_log.head()


# In[73]:


# Plotting prediction against observation

plt.scatter(reg_model_data_log['prediction'], reg_model_data_log['log_total_pajak'], color = "k", marker=".")
x_domain = np.linspace(np.min(reg_model_data_log['prediction']), np.max(reg_model_data_log['prediction']), 10000)
y_domain = np.linspace(np.min(reg_model_data_log['log_total_pajak']), np.max(reg_model_data_log['log_total_pajak']), 10000)
plt.ylabel('observation')
plt.xlabel('prediction')
plt.title("Observation and prediction regression line (log-transformed)")
plt.plot(x_domain, y_domain, label="Fitted line", color = "b")
plt.show()


# From this plot we could gather even though the prediction and observation don't exactly lie on a straight line (45 degree), there is not too much difference between them. Therefore, we could safely use this model as prediction tool in prediction total_pajak.

# In[74]:


#Visualize the residual plot
plt.scatter(result_5.fittedvalues, result_5.resid, marker=".", c = "k")

# Plot the horizontal line in 0 as the fitted line
plt.axhline([0])


# There is not exactly a visible pattern from the variances.

# In[75]:


#Plot the distribution of the errors
plt.hist(result_5.resid, color='blue', alpha=0.4)
plt.xlabel("residual")
plt.ylabel("count")

plt.show()


# Model's residuals show a bell-shaped shape.

# In[76]:


reg_model_data.head()


# In[77]:


# Let us see what the predicition looks like in original scale, namely the exponent

reg_model_data['prediction'] = np.exp(reg_model_data_log['prediction'])


# In[78]:


reg_model_data.head()


# In[79]:


# Plotting prediction against observation (original value)

plt.scatter(reg_model_data['prediction'], reg_model_data['total_pajak'], color = "k", marker=".")
x_domain = np.linspace(np.min(reg_model_data['prediction']), np.max(reg_model_data['prediction']), 10000)
y_domain = np.linspace(np.min(reg_model_data['total_pajak']), np.max(reg_model_data['total_pajak']), 10000)
plt.ylabel('observation')
plt.xlabel('prediction')
plt.title("Observation and prediction regression line (original value)")
plt.plot(x_domain, y_domain, label="Fitted line", color = "b")
plt.show()


# Looks quite nice, not so far from 45 degree line.

# In[ ]:





# In[ ]:




