# west-java-vehicle-tax-revenue
A project focusing on Vehicle Tax Revenue in West Java Province, Indonesia

# Background
This project tries to do answer two questions. Firs, is there any improvement in the matter of tax revenue, based on year-to-year, tax/RGDP and tax/vehicle basis? Second, what variables do drive the revenue and how should the model be?

# Objective
1. Statistical inference
2. Linear regression model
   
# Dataset
All of the data used here come from Open Data Jabar and Indonesia Statistics with details as such:
1. [Tax revenue](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fjumlah-pajak-dan-denda-kendaraan-bermotor-berdasarkan-jenis-pajak-kendaraan-bermotor-pkb-di-jawa-barat)
2. [Right transfer fee (also a kind of tax revenue)](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fjumlah-bea-balik-nama-kendaraan-berdasarkan-jenis-bea-balik-nama-kendaraan-bermotor-bbnkb-dan-cabang-pelayanan-di-jawa-barat)
3. [Number of vehicles in general](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fjumlah-kendaraan-bermotor-berdasarkan-cabang-pelayanan-di-jawa-barat)
4. [Number of vehicles based on function and category](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fjumlah-kendaraan-berdasarkan-jenis-kendaraan-fungsi-kendaraan-dan-cabang-pelayanan-di-jawa-barat)
5. [Number of unregistered vehicles](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fjumlah-kendaraan-yang-tidak-daftar-ulang-berdasarkan-jenis-kendaraan-fungsi-kendaraan-dan-cabang-pelayanan-di-jawa-barat)
6. [Number of un-reregistered vehicles](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fjumlah-kendaraan-yang-belum-daftar-ulang-berdasarkan-jenis-kendaraan-fungsi-kendaraan-dan-cabang-pelayanan-di-jawa-barat)
7. Payment channels (when I tried looking up at the data source again, sadly I could not find the link)
8. [Roads based on category](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fpanjang-ruas-jalan-berdasarkan-jenis-permukaan-di-jawa-barat)
9. [Roads based on authority](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fpanjang-jalan-berdasarkan-tingkat-kewenangan-pemerintahan-di-jawa-barat)
10. [Roads based on condition](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fpanjang-ruas-jalan-berdasarkan-kondisi-jalan-di-jawa-barat)
11. [Roads based on regions](https://medium.com/r/?url=https%3A%2F%2Fopendata.jabarprov.go.id%2Fid%2Fdataset%2Fpanjang-ruas-jalan-berdasarkan-kabupatenkota-di-jawa-barat)
12. [West Java Population](https://medium.com/r/?url=https%3A%2F%2Fjabar.bps.go.id%2Findicator%2F12%2F133%2F1%2Fjumlah-penduduk-menurut-kabupaten-kota.html)
13. [West Java Regional GDP](https://medium.com/r/?url=https%3A%2F%2Fjabar.bps.go.id%2Findicator%2F155%2F230%2F1%2Fpdrb-per-kapita-atas-dasar-harga-konstan-menurut-kabupaten-kota-.html)

# Flow
As with any other project, this is also started with some data cleaning and, subsequently, assembling. After that, it continues with doing stastical test in order to some hyphotesis. Lastly, the project goes to derive linear regression model to build a prediction tool for tax revenue.

For simplicity reason, this project is divided into three files, `stat_project_dataset`, `stat_project_inference` and `stat_project_regression_final`. The first one contains ready-to-use and after-cleaning data, the second is for statistical inference and the last is for modelling linear regression.

# Data Cleaning and Assembly
Since the data came from public administration, there is not really any empty data there. The real work is about assembling different data for certain uses since different use requires different granularities.

In short, all those data are turned into four main datasets:
1. Population
2. Vehicles
3. Tax revenue
4. RGDP

There will also be a final dataset used for linear regression model which uses variable from four above datasets.

Special note for two variables in the final dataset, namely kondisi_max and jenis_max, which came from road dataset which show value with the longest road length. So kondisi_max shows which road condition is the most widespread ("BAIK/"GOOD") and jenis_max shows the road category.

Final dataset is quite cut since there is not much overlap between original datasets. As a final result, there are only two years worth of data left (2019–2020).

# Inference
This project tries to answer if tax revenue did undergo some improvement, namely on the basis of:
1. Year-to-year: comparing tax revenue from year n to year n+1
2. Population: comparing the ratio of tax revenue/population (tax revenue per capita) from year n to year n+1
3. RGDP: comparing the ratio of tax revenue/RGDP from year n to year n+1

For these three goals, t test will be used.

# Linear Regression
For this objective, the outcome is tax revenue while the predictors are RGDP (pdrb_per_kapita), population (jumlah_penduduk), number of vehicles (kendaraan_per_kapita), road category (jenis_max) and road condition (kondisi_max).

There will five different models in total which are the result of recurring tries to find the most appopriate model based on R-squared and multicollinearity reason.
