#!/usr/bin/env python
# coding: utf-8

# In[2]:


# load data
import pandas as pd
import numpy as np

# visualization
import matplotlib.pyplot as plt
import seaborn as sns

# modelling
import statsmodels.formula.api as smf


# In[3]:


pd.set_option('display.max_columns', None)


# In[4]:


data_pajak = pd.read_csv('bapenda-od_15833_jml_pajak_denda_kndrn_brmtr__jenis_pajak_kndrn_brmtr_p_data.csv')
data_bea = pd.read_csv('bapenda-od_15828_jml_bea_balik_nama_kndrn__jenis_bea_balik_nama_kndrn_b_data.csv')
data_jenis_fungsi = pd.read_csv('bapenda-od_15829_jml_kndrn__jenis_kndrn_fungsi_kndrn_cabang_pelayanan_data.csv')
data_jumlah = pd.read_csv('bapenda-od_15830_jumlah_kendaraan_bermotor_berdasarkan_cabang_pelayanan_data.csv')
data_belum_daftar_ulang = pd.read_csv('bapenda-od_15831_jml_kndrn_belum_daftar_ulang__jenis_kndrn_fungsi_kndrn_data.csv')
data_tidak_daftar_ulang = pd.read_csv('bapenda-od_15832_jml_kndrn_tidak_daftar_ulang__jenis_kndrn_fungsi_kndrn_data.csv')
data_kanal = pd.read_csv('bapenda-od_15834_jml_pembayaran_pajak_kndrn_brmtr_melalui_e_samsat__ban_data.csv')
data_panjang_jalan_by_jenis = pd.read_csv('disbmpr-od_15059_panjang_ruas_jalan_berdasarkan_jenis_permukaan_data.csv')
data_panjang_jalan_by_wewenang = pd.read_csv('disbmpr-od_18478_panjang_jalan__tingkat_kewenangan_peman_data.csv')
data_panjang_jalan_by_kondisi = pd.read_csv('disbmpr-od_15060_panjang_ruas_jalan_berdasarkan_kondisi_jalan_data.csv')
data_panjang_jalan_by_kabkota = pd.read_csv('disbmpr-od_15061_panjang_ruas_jalan_berdasarkan_kabupatenkota_data.csv')


# In[5]:


pdrb_2010_2011 = pd.read_excel('PDRB per Kapita Atas Dasar Harga Konstan Menurut Kabupaten_Kota _2010_2011.xlsx')
pdrb_2012_2014 = pd.read_excel('PDRB per Kapita Atas Dasar Harga Konstan Menurut Kabupaten_Kota _2012_2014.xlsx')
pdrb_2015_2017 = pd.read_excel('PDRB per Kapita Atas Dasar Harga Konstan Menurut Kabupaten_Kota _2015_2017.xlsx')
pdrb_2018_2020 = pd.read_excel('PDRB per Kapita Atas Dasar Harga Konstan Menurut Kabupaten_Kota _2018_2020.xlsx')


# In[6]:


penduduk_2012_2014 = pd.read_excel('Jumlah Penduduk Menurut Kabupaten_Kota_2012_2014.xlsx')
penduduk_2015_2017 = pd.read_excel('Jumlah Penduduk Menurut Kabupaten_Kota_2015_2017.xlsx')
penduduk_2018_2020 = pd.read_excel('Jumlah Penduduk Menurut Kabupaten_Kota_2018_2020.xlsx')


# In[7]:


data_pajak.isnull().sum()


# In[8]:


data_bea.isnull().sum()


# In[9]:


data_jenis_fungsi.isnull().sum()


# In[10]:


data_belum_daftar_ulang.isnull().sum()


# In[11]:


data_tidak_daftar_ulang.isnull().sum()


# In[12]:


data_kanal.isnull().sum()


# In[13]:


data_panjang_jalan_by_jenis.isnull().sum()


# In[14]:


data_panjang_jalan_by_wewenang.isnull().sum()


# In[15]:


data_panjang_jalan_by_kondisi.isnull().sum()


# In[16]:


data_panjang_jalan_by_kabkota.isnull().sum()


# In[17]:


data_pajak.head()


# In[18]:


data_pajak.isnull().sum()


# In[19]:


data_pajak_edit = data_pajak[['kode_kabupaten_kota', 'jenis_pkb', 'jumlah_pendapatan', 'tahun']].groupby(['kode_kabupaten_kota', 'jenis_pkb', 'tahun'], as_index=False).sum().sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_pajak_edit.head()


# In[20]:


data_pajak_use=data_pajak_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='jenis_pkb',values=['jumlah_pendapatan'])
data_pajak_use


# In[21]:


data_pajak_use.columns = data_pajak_use.columns.droplevel()
data_pajak_use


# In[22]:


data_pajak_use=data_pajak_use.rename_axis(None,axis=1)
data_pajak_use


# In[23]:


data_pajak_use=data_pajak_use.reset_index()
data_pajak_use


# In[24]:


data_bea.head()


# In[25]:


data_bea['jenis_bbnkb'].unique()


# In[26]:


data_bea_edit = data_bea[['kode_kabupaten_kota', 'jenis_bbnkb', 'jumlah_pendapatan', 'tahun']].groupby(['kode_kabupaten_kota', 'jenis_bbnkb', 'tahun'], as_index=False).sum().sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_bea_use=data_bea_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='jenis_bbnkb',values=['jumlah_pendapatan'])
data_bea_use.columns = data_bea_use.columns.droplevel()
data_bea_use=data_bea_use.rename_axis(None,axis=1)
data_bea_use=data_bea_use.reset_index()
data_bea_use


# In[27]:


data_jenis_fungsi.head()


# In[28]:


data_jenis_fungsi['fungsi_kendaraan'].unique()


# In[29]:


data_jenis_fungsi['fungsi_kendaraan'] = data_jenis_fungsi['fungsi_kendaraan'].replace(' PRIBADI', 'PRIBADI', regex=True)
data_jenis_fungsi['fungsi_kendaraan'] = data_jenis_fungsi['fungsi_kendaraan'].replace(' DINAS', 'DINAS', regex=True)
data_jenis_fungsi['fungsi_kendaraan'] = data_jenis_fungsi['fungsi_kendaraan'].replace(' UMUM', 'UMUM', regex=True)


# In[30]:


data_jenis_fungsi['fungsi_kendaraan'].unique()


# In[31]:


data_jenis_fungsi_edit = data_jenis_fungsi[['kode_kabupaten_kota', 'fungsi_kendaraan', 'jumlah_kendaraan', 'tahun']].groupby(['kode_kabupaten_kota', 'fungsi_kendaraan', 'tahun'], as_index=False).sum().sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_jenis_fungsi_use = data_jenis_fungsi_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='fungsi_kendaraan',values=['jumlah_kendaraan'])
data_jenis_fungsi_use.columns = data_jenis_fungsi_use.columns.droplevel()
data_jenis_fungsi_use=data_jenis_fungsi_use.rename_axis(None,axis=1)
data_jenis_fungsi_use=data_jenis_fungsi_use.reset_index()
data_jenis_fungsi_use


# In[32]:


data_jenis_fungsi_use.rename(columns={'DINAS':'fungsi_dinas',
                                     'PRIBADI':'fungsi_pribadi',
                                     'UMUM':'fungsi_umum'}, inplace=True)
data_jenis_fungsi_use


# In[33]:


data_belum_daftar_ulang.head()


# In[34]:


data_belum_daftar_ulang['fungsi_kendaraan'].unique()


# In[35]:


data_belum_daftar_ulang['fungsi_kendaraan'] = data_belum_daftar_ulang['fungsi_kendaraan'].replace('  PRIBADI', 'PRIBADI', regex=True)
data_belum_daftar_ulang['fungsi_kendaraan'] = data_belum_daftar_ulang['fungsi_kendaraan'].replace('   DINAS', 'DINAS', regex=True)
data_belum_daftar_ulang['fungsi_kendaraan'] = data_belum_daftar_ulang['fungsi_kendaraan'].replace('   UMUM', 'UMUM', regex=True)


# In[36]:


data_belum_daftar_ulang['fungsi_kendaraan'].unique()


# In[37]:


data_belum_daftar_ulang_edit = data_belum_daftar_ulang[['kode_kabupaten_kota', 'fungsi_kendaraan', 'jumlah_kendaraan', 'tahun']].groupby(['kode_kabupaten_kota', 'fungsi_kendaraan', 'tahun'], as_index=False).sum().sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_belum_daftar_ulang_use = data_belum_daftar_ulang_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='fungsi_kendaraan',values=['jumlah_kendaraan'])
data_belum_daftar_ulang_use.columns = data_belum_daftar_ulang_use.columns.droplevel()
data_belum_daftar_ulang_use = data_belum_daftar_ulang_use.rename_axis(None,axis=1)
data_belum_daftar_ulang_use = data_belum_daftar_ulang_use.reset_index()
data_belum_daftar_ulang_use


# In[38]:


data_belum_daftar_ulang_use.rename(columns={'DINAS':'belum_daftar_dinas',
                                     'PRIBADI':'belum_daftar_pribadi',
                                     'UMUM':'belum_daftar_umum'}, inplace=True)
data_belum_daftar_ulang_use


# In[39]:


data_tidak_daftar_ulang.head()


# In[40]:


data_tidak_daftar_ulang['fungsi_kendaraan'].unique()


# In[41]:


data_tidak_daftar_ulang_edit = data_tidak_daftar_ulang[['kode_kabupaten_kota', 'fungsi_kendaraan', 'jumlah_kendaraan', 'tahun']].groupby(['kode_kabupaten_kota', 'fungsi_kendaraan', 'tahun'], as_index=False).sum().sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_tidak_daftar_ulang_use = data_tidak_daftar_ulang_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='fungsi_kendaraan',values=['jumlah_kendaraan'])
data_tidak_daftar_ulang_use.columns = data_tidak_daftar_ulang_use.columns.droplevel()
data_tidak_daftar_ulang_use = data_tidak_daftar_ulang_use.rename_axis(None,axis=1)
data_tidak_daftar_ulang_use = data_tidak_daftar_ulang_use.reset_index()
data_tidak_daftar_ulang_use


# In[42]:


data_tidak_daftar_ulang_use.rename(columns={'DINAS':'tidak_daftar_dinas',
                                     'PRIBADI':'tidak_daftar_pribadi',
                                     'UMUM':'tidak_daftar_umum'}, inplace=True)
data_tidak_daftar_ulang_use


# In[43]:


data_kanal.head()


# In[44]:


data_kanal['nama_bank'].unique()


# In[45]:


data_kanal_edit = data_kanal[['kode_kabupaten_kota', 'nama_bank', 'jumlah_pendapatan', 'tahun']].groupby(['kode_kabupaten_kota', 'nama_bank', 'tahun'], as_index=False).sum().sort_values('tahun', ascending=True)
data_kanal_edit.head()


# In[46]:


data_kanal['tahun'].unique()


# In[47]:


data_kanal_edit = data_kanal[['kode_kabupaten_kota', 'tahun', 'nama_bank', 'jumlah_pendapatan']].groupby(['kode_kabupaten_kota', 'nama_bank', 'tahun'], as_index=False).sum().sort_values('tahun', ascending=True)
data_kanal_use = data_kanal_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='nama_bank',values=['jumlah_pendapatan'])
data_kanal_use.columns = data_kanal_use.columns.droplevel()
data_kanal_use = data_kanal_use.rename_axis(None,axis=1)
data_kanal_use = data_kanal_use.reset_index()
data_kanal_use


# In[48]:


data_kanal_use.isnull().sum()


# In[49]:


data_kanal_use = data_kanal_use.fillna(0)


# In[50]:


data_kanal_use.head()


# In[51]:


data_kanal_use.isnull().sum()


# In[52]:


data_panjang_jalan_by_jenis.head()


# In[53]:


data_panjang_jalan_by_jenis.isnull().sum()


# In[54]:


data_panjang_jalan_by_jenis.info()


# In[55]:


data_panjang_jalan_by_jenis['tahun'].unique()


# In[56]:


data_panjang_jalan_by_jenis = data_panjang_jalan_by_jenis.drop(['id'], axis=1)


# In[57]:


data_panjang_jalan_by_jenis['panjang_ruas_jalan'] = data_panjang_jalan_by_jenis['panjang_ruas_jalan'].str.replace('-', '0')


# In[58]:


data_panjang_jalan_by_jenis['panjang_ruas_jalan'] = data_panjang_jalan_by_jenis['panjang_ruas_jalan'].str.replace(',', '.')
data_panjang_jalan_by_jenis['panjang_ruas_jalan'] = data_panjang_jalan_by_jenis['panjang_ruas_jalan'].astype(float)


# In[59]:


data_panjang_jalan_by_jenis.head()


# In[60]:


data_panjang_jalan_by_jenis_use = data_panjang_jalan_by_jenis.pivot(index=['kode_kabupaten_kota','tahun'], columns='jenis_permukaan',values=['panjang_ruas_jalan'])
data_panjang_jalan_by_jenis_use.columns = data_panjang_jalan_by_jenis_use.columns.droplevel()
data_panjang_jalan_by_jenis_use = data_panjang_jalan_by_jenis_use.rename_axis(None,axis=1)
data_panjang_jalan_by_jenis_use = data_panjang_jalan_by_jenis_use.reset_index()
data_panjang_jalan_by_jenis_use


# In[61]:


data_panjang_jalan_by_jenis_use.rename(columns={'ASPAL':'aspal',
                                               'LAINNYA':'lainnya',
                                               'TIDAK DI ASPAL':'tidak_aspal'}, inplace=True)
data_panjang_jalan_by_jenis_use


# In[62]:


data_panjang_jalan_by_jenis_use.isnull().sum()


# In[63]:


data_panjang_jalan_by_wewenang.head()


# In[64]:


data_panjang_jalan_by_wewenang.isnull().sum()


# In[65]:


data_panjang_jalan_by_wewenang['tahun'].unique()


# In[66]:


data_panjang_jalan_by_wewenang.info()


# In[67]:


data_panjang_jalan_by_wewenang_use = data_panjang_jalan_by_wewenang.pivot(index=['kode_kabupaten_kota','tahun'], columns='tingkat_kewenangan',values=['panjang_jalan'])
data_panjang_jalan_by_wewenang_use.columns = data_panjang_jalan_by_wewenang_use.columns.droplevel()
data_panjang_jalan_by_wewenang_use = data_panjang_jalan_by_wewenang_use.rename_axis(None,axis=1)
data_panjang_jalan_by_wewenang_use = data_panjang_jalan_by_wewenang_use.reset_index()
data_panjang_jalan_by_wewenang_use


# In[68]:


data_panjang_jalan_by_wewenang_use.rename(columns={'KABUPATEN/KOTA':'wewenang_kabkota',
                                                  'NEGARA':'wewenang_negara',
                                                  'PROVINSI':'wewenang_provinsi'}, inplace=True)
data_panjang_jalan_by_wewenang_use


# In[69]:


data_panjang_jalan_by_wewenang_use.isnull().sum()


# In[70]:


data_panjang_jalan_by_wewenang_use[data_panjang_jalan_by_wewenang_use['kode_kabupaten_kota']==3201]


# In[71]:


data_panjang_jalan_by_wewenang_use = data_panjang_jalan_by_wewenang_use.fillna(method='ffill')


# In[72]:


data_panjang_jalan_by_wewenang_use.head()


# In[73]:


data_panjang_jalan_by_wewenang_use.isnull().sum()


# In[74]:


data_panjang_jalan_by_kondisi.head()


# In[75]:


data_panjang_jalan_by_kondisi = data_panjang_jalan_by_kondisi.drop(['id'], axis=1)


# In[76]:


data_panjang_jalan_by_kondisi = data_panjang_jalan_by_kondisi.drop_duplicates()


# In[77]:


data_panjang_jalan_by_kondisi


# In[78]:


data_panjang_jalan_by_kondisi['panjang_ruas_jalan'] = data_panjang_jalan_by_kondisi['panjang_ruas_jalan'].str.replace(',', '.')


# In[79]:


data_panjang_jalan_by_kondisi['panjang_ruas_jalan'] = data_panjang_jalan_by_kondisi['panjang_ruas_jalan'].str.replace('-', '0')


# In[80]:


data_panjang_jalan_by_kondisi['panjang_ruas_jalan'] = data_panjang_jalan_by_kondisi['panjang_ruas_jalan'].astype(float)


# In[81]:


data_panjang_jalan_by_kondisi[data_panjang_jalan_by_kondisi['kondisi_jalan']=='BAIK']['kategori_jalan'].unique()


# In[82]:


data_panjang_jalan_by_kondisi[data_panjang_jalan_by_kondisi['kondisi_jalan']=='SEDANG']['kategori_jalan'].unique()


# In[83]:


data_panjang_jalan_by_kondisi[data_panjang_jalan_by_kondisi['kondisi_jalan']=='RUSAK RINGAN']['kategori_jalan'].unique()


# In[84]:


data_panjang_jalan_by_kondisi[data_panjang_jalan_by_kondisi['kondisi_jalan']=='RUSAK BERAT']['kategori_jalan'].unique()


# In[85]:


data_panjang_jalan_by_kondisi.info()


# In[86]:


data_panjang_jalan_by_kondisi.head()


# In[164]:


data_panjang_jalan_by_kondisi_edit = data_panjang_jalan_by_kondisi[['kode_kabupaten_kota', 'tahun', 'kondisi_jalan', 'panjang_ruas_jalan']].groupby(['kode_kabupaten_kota','kondisi_jalan', 'tahun'], as_index=False).sum().sort_values('tahun', ascending=True)
data_panjang_jalan_by_kondisi_use = data_panjang_jalan_by_kondisi_edit.pivot(index=['kode_kabupaten_kota','tahun'], columns='kondisi_jalan',values=['panjang_ruas_jalan'])
data_panjang_jalan_by_kondisi_use.columns = data_panjang_jalan_by_kondisi_use.columns.droplevel()
data_panjang_jalan_by_kondisi_use = data_panjang_jalan_by_kondisi_use.rename_axis(None,axis=1)
data_panjang_jalan_by_kondisi_use = data_panjang_jalan_by_kondisi_use.reset_index()
data_panjang_jalan_by_kondisi_use


# In[88]:


data_panjang_jalan_by_kondisi_use.isnull().sum()


# In[89]:


data_pajak_use.head()


# In[90]:


data_kendaraan = data_pajak_use.merge(data_bea_use, on=['kode_kabupaten_kota', 'tahun']).merge(data_jenis_fungsi_use, on=['kode_kabupaten_kota', 'tahun'],).merge(data_belum_daftar_ulang_use, on=['kode_kabupaten_kota', 'tahun']).merge(data_tidak_daftar_ulang_use, on=['kode_kabupaten_kota', 'tahun']).merge(data_kanal_use, on=['kode_kabupaten_kota', 'tahun'])


# In[91]:


data_kendaraan.tail()


# In[92]:


data_kendaraan.isnull().sum()


# In[93]:


data_panjang_jalan_by_jenis_use.head()


# In[94]:


data_panjang_jalan_by_wewenang_use.head()


# In[95]:


data_jalan = data_panjang_jalan_by_jenis_use.merge(data_panjang_jalan_by_wewenang_use, on=['kode_kabupaten_kota', 'tahun']).merge(data_panjang_jalan_by_kondisi_use, on=['kode_kabupaten_kota', 'tahun'])


# In[96]:


data_jalan.head()


# In[97]:


data_jalan.isnull().sum()


# In[98]:


data_kendaraan['tahun'].unique()


# In[99]:


data_jalan['tahun'].unique()


# In[100]:


pdrb_2010_2011.head()


# In[101]:


pdrb_2010_2011_header = pdrb_2010_2011.iloc[0]
pdrb_2010_2011_use = pd.DataFrame(pdrb_2010_2011.values[1:], columns=pdrb_2010_2011_header)
pdrb_2010_2011_use.head()


# In[102]:


pdrb_2010_2011_use = pdrb_2010_2011_use.rename(columns=str).rename(columns={'nan':'wilayah'})


# In[103]:


pdrb_2010_2011_use = pdrb_2010_2011_use.drop(range(28,32))


# In[104]:


pdrb_2010_2011_use


# In[105]:


pdrb_2012_2014.head()


# In[106]:


pdrb_2012_2014_header = pdrb_2012_2014.iloc[0]
pdrb_2012_2014_use = pd.DataFrame(pdrb_2012_2014.values[1:], columns=pdrb_2012_2014_header)
pdrb_2012_2014_use = pdrb_2012_2014_use.rename(columns=str).rename(columns={'nan':'wilayah',
                                                                           '2012.0':'2012',
                                                                           '2013.0':'2013',
                                                                           '2014.0':'2014'})
pdrb_2012_2014_use = pdrb_2012_2014_use.drop(range(28,32))
pdrb_2012_2014_use


# In[107]:


pdrb_2015_2017.head()


# In[108]:


pdrb_2015_2017_header = pdrb_2015_2017.iloc[0]
pdrb_2015_2017_use = pd.DataFrame(pdrb_2015_2017.values[1:], columns=pdrb_2015_2017_header)
pdrb_2015_2017_use = pdrb_2015_2017_use.rename(columns=str).rename(columns={'nan':'wilayah',
                                                                           '2015.0':'2015',
                                                                           '2016.0':'2016',
                                                                           '2017.0':'2017'})
pdrb_2015_2017_use = pdrb_2015_2017_use.drop(range(28,32))
pdrb_2015_2017_use


# In[109]:


pdrb_2018_2020.head()


# In[110]:


pdrb_2018_2020_header = pdrb_2018_2020.iloc[0]
pdrb_2018_2020_use = pd.DataFrame(pdrb_2018_2020.values[1:], columns=pdrb_2018_2020_header)
pdrb_2018_2020_use = pdrb_2018_2020_use.rename(columns=str).rename(columns={'nan':'wilayah',
                                                                           '2018.0':'2018',
                                                                           '2019.0':'2019',
                                                                           '2020.0':'2020'})
pdrb_2018_2020_use = pdrb_2018_2020_use.drop(range(28,32))
pdrb_2018_2020_use


# In[111]:


data_pdrb = pdrb_2018_2020_use.merge(pdrb_2015_2017_use, on='wilayah').merge(pdrb_2012_2014_use, on='wilayah')


# In[112]:


data_pdrb


# In[113]:


data_pdrb = data_pdrb[['wilayah', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']]


# In[114]:


data_pdrb = data_pdrb.iloc[1:]


# In[115]:


data_pdrb.head()


# In[116]:


daftar_kab_kota = data_pajak[['kode_kabupaten_kota', 'nama_kabupaten_kota']]
daftar_kab_kota = daftar_kab_kota.drop_duplicates()


# In[117]:


daftar_kab_kota


# In[118]:


wilayah_pdrb = data_pdrb['wilayah'].tolist()


# In[119]:


wilayah_pdrb


# In[120]:


daftar_wilayah_pdrb = []
for wilayah in wilayah_pdrb:
    if wilayah.startswith('Kota'):
        daftar_wilayah_pdrb.append(wilayah)
    else:
        kota = "Kabupaten "+str(wilayah)
        daftar_wilayah_pdrb.append(kota)


# In[121]:


daftar_wilayah_pdrb


# In[122]:


data_pdrb.head()


# In[123]:


data_pdrb['nama_kabupaten_kota'] = daftar_wilayah_pdrb


# In[124]:


data_pdrb


# In[125]:


data_pdrb = data_pdrb[['nama_kabupaten_kota', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']]


# In[126]:


data_pdrb.head()


# In[127]:


data_pdrb['nama_kabupaten_kota'] = data_pdrb['nama_kabupaten_kota'].str.upper()


# In[128]:


data_pdrb


# In[129]:


data_pdrb = data_pdrb.merge(daftar_kab_kota, on='nama_kabupaten_kota')
data_pdrb = data_pdrb[['nama_kabupaten_kota', 'kode_kabupaten_kota', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']]


# In[130]:


data_pdrb.head()


# In[131]:


data_pdrb = pd.melt(data_pdrb, id_vars=['nama_kabupaten_kota','kode_kabupaten_kota'],value_vars=['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012'],var_name='tahun',value_name='jumlah').sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_pdrb = data_pdrb.reset_index()
data_pdrb = data_pdrb.drop(['index'], axis=1)


# In[132]:


data_pdrb.head()


# In[133]:


data_kendaraan.head()


# In[134]:


data_jalan.head()


# In[135]:


penduduk_2012_2014.head()


# In[136]:


penduduk_2012_2014_header = penduduk_2012_2014.iloc[0]
penduduk_2012_2014_use = pd.DataFrame(penduduk_2012_2014.values[1:], columns=penduduk_2012_2014_header)
penduduk_2012_2014_use = penduduk_2012_2014_use.rename(columns=str).rename(columns={'nan':'wilayah',
                                                                           '2012.0':'2012',
                                                                           '2013.0':'2013',
                                                                           '2014.0':'2014'})
penduduk_2012_2014_use = penduduk_2012_2014_use.drop(range(28,32))
penduduk_2012_2014_use


# In[137]:


penduduk_2015_2017_header = penduduk_2015_2017.iloc[0]
penduduk_2015_2017_use = pd.DataFrame(penduduk_2015_2017.values[1:], columns=penduduk_2015_2017_header)
penduduk_2015_2017_use = penduduk_2015_2017_use.rename(columns=str).rename(columns={'nan':'wilayah',
                                                                           '2015.0':'2015',
                                                                           '2016.0':'2016',
                                                                           '2017.0':'2017'})
penduduk_2015_2017_use = penduduk_2015_2017_use.drop(range(28,32))
penduduk_2015_2017_use


# In[138]:


penduduk_2018_2020_header = penduduk_2018_2020.iloc[0]
penduduk_2018_2020_use = pd.DataFrame(penduduk_2018_2020.values[1:], columns=penduduk_2018_2020_header)
penduduk_2018_2020_use = penduduk_2018_2020_use.rename(columns=str).rename(columns={'nan':'wilayah',
                                                                           '2018.0':'2018',
                                                                           '2019.0':'2019',
                                                                           '2020.0':'2020'})
penduduk_2018_2020_use = penduduk_2018_2020_use.drop(range(28,32))
penduduk_2018_2020_use


# In[139]:


data_penduduk = penduduk_2012_2014_use.merge(penduduk_2015_2017_use, on='wilayah').merge(penduduk_2018_2020_use, on='wilayah')
data_penduduk.head()


# In[140]:


data_penduduk = data_penduduk[['wilayah', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']]
data_penduduk.head()


# In[141]:


data_penduduk = data_penduduk.iloc[1:]


# In[142]:


data_penduduk.head()


# In[143]:


wilayah_penduduk = data_penduduk['wilayah'].tolist()


# In[144]:


wilayah_penduduk


# In[145]:


daftar_wilayah_penduduk = []
for wilayah in wilayah_penduduk:
    if wilayah.startswith('Kota'):
        daftar_wilayah_penduduk.append(wilayah)
    else:
        kota = "Kabupaten "+str(wilayah)
        daftar_wilayah_penduduk.append(kota)


# In[146]:


daftar_wilayah_penduduk


# In[147]:


data_penduduk.head()


# In[148]:


data_penduduk['nama_kabupaten_kota'] = daftar_wilayah_penduduk


# In[149]:


data_penduduk.head()


# In[150]:


data_penduduk = data_penduduk[['nama_kabupaten_kota', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']]


# In[151]:


data_penduduk.head()


# In[152]:


data_penduduk['nama_kabupaten_kota'] = data_penduduk['nama_kabupaten_kota'].str.upper()


# In[153]:


data_penduduk.head()


# In[154]:


data_penduduk = data_penduduk.merge(daftar_kab_kota, on='nama_kabupaten_kota')
data_penduduk = data_penduduk[['nama_kabupaten_kota', 'kode_kabupaten_kota', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012']]


# In[155]:


data_penduduk.head()


# In[156]:


data_penduduk = pd.melt(data_penduduk, id_vars=['nama_kabupaten_kota','kode_kabupaten_kota'],value_vars=['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012'],var_name='tahun',value_name='jumlah').sort_values(['kode_kabupaten_kota', 'tahun'], ascending=True)
data_penduduk = data_penduduk.reset_index()
data_penduduk = data_penduduk.drop(['index'], axis=1)


# In[157]:


data_penduduk.head()


# In[158]:


data_kendaraan.head()


# In[159]:


data_jalan.head()


# In[160]:


data_pdrb.head()


# In[161]:


data_penduduk.head()


# In[ ]:





# In[ ]:





# In[ ]:




