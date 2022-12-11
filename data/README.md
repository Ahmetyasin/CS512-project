# Data Directory

## File descriptions
Please add the description of any file/directory you add here.

### yahoo_finance dir:
Contains the files:
* **merged_yahoo_data.csv**: Merged dataset downloaded from [Yahoo Finance](https://finance.yahoo.com/).
* **data_summary.csv**: Summary of the merged dataset for each company. All columns are self explanatory except `na_in_close`, which is the number of NaN values in the "close" column, as an indicator of missing data.

### TUIK dir:

* **export_import**: Total imports and exports
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=Dis-Ticaret-104)

* **export/import_unit_value_index**: Export/Import unit value index
    * Base year 2010
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=Dis-Ticaret-104)

* **unemployment1**: Unemployment rate by age groups ("Labour Force Statistics (1988-2013)" in TUIK site)
    * [Link to source](https://biruni.tuik.gov.tr/isgucuapp/isgucu.zul?dil=2)

* **unemployment2**: Unemployment rate by age groups ("Labour Force Statistics (2014 and after)" in TUIK site)
    * [Link to source](https://biruni.tuik.gov.tr/medas/?kn=72&locale=en)

* **consumer_price_index**: Consumer Price Index
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=Inflation-v-Price-106)

* **gdp_production**: Gross domestic product by production approach ("Quarterly Gross Domestic Product" in TUIK site)
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=National-Accounts-113)
    
* **gdp_expenditure**: Gross domestic product by expenditure approach ("Quarterly Gross Domestic Product" in TUIK site)
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=National-Accounts-113)
    
* **gdp_income**: Gross Domestic Product By Income Approach ("Quarterly Gross Domestic Product" in TUIK site)
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=National-Accounts-113)

* **industrial_production_index1 (2005 - 2015)**: Industrial Production Index
    * Industrial Production Index (2015=100) (base year: 2015)
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=Industry-114)
    
* **industrial_production_index2 (2016 - 2022)**: Industrial Production Index
    * Industrial Production Index (2015=100) (base year: 2015)
    * [Link to source](https://data.tuik.gov.tr/Kategori/GetKategori?p=Industry-114)


### wiki/bist_company_symbols
Company symbols used to download data from Yahoo Finance.
* [Source of wiki_company_symbols](https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Istanbul_Stock_Exchange)
* [Source of bist_company_symbols](https://www.wikiwand.com/tr/Borsa_%C4%B0stanbul%27da_i%C5%9Flem_g%C3%B6ren_%C5%9Firketler_listesi)
