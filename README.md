# Predicting Sectoral Growth in Turkey from Macroeconomic Indicators

**Team members**: Ahmet Yasin Aytar, Halil Ibrahim Ergül, Yasser Zouzou

## Introduction
Considering the complicated outlook that Turkey’s economy goes through these years, there has been a significant increase in the general public's interest in the stock market. It became tremendously prevelant for an average person to get involved in the stock market. For instance, according to observations of a newspaper (Habertürk), the number of young people who buy and sell shares in the stock market increased by 340%, exceeding 357 thousand. Therefore, informed decisions about buying, selling, or holding onto stocks is essential in bringing profits. What is more, making informed and solid predictions of stock value can also be important for businesses, as the value of their stocks can impact the company's access to capital and its policy of stocks. Overall, predicting stock value is important for both individual investors and businesses as it can impact decision-making and financial outcomes. These reasons motivated us to use of machine learning models for the purpose of this task.

The problem this project is dealing with falls mostly under the domain of Stock Market Prediction with some important divergences. For one thing, our objective is not to predict stock price per se, rather; being informed through the literature, we treat the market capitalization of companies (calculated by their stock prices) as their success/growth rate and we aim at predicting sectoral growth that different Turkish companies takes part in. Second, the task that this project focuses is not a prevalent field in the literature which generally focuses on stock prices of major indexes instead of looking at how sectors would behave differently with market values of stocks that are influenced through macroeconomic variables.

Our aim is to predict the sectoral growth (which we measure by the market value of stocks for companies belonging to a certain sector) of different industries using the macroeconomic indicators in Turkey. Hence, this project differs from conventional stock prediction tasks as our research focuses on the question of to what extent macroeconomic factors might possibly help in predicting sectoral growth.

## Data and Methods
The micro economic indicator datasets used in this study were manually collected mainly from the Turkish Statistical Institute (TUIK) and the Turkish Central Bank (TCMB). A summary of the datasets is provided below:

* **Total imports and exports (TUIK):** Total value of imports and exports in Turkish Lira (TL) and US Dollar (USD).

* **Export and import unit value indices (TUIK):** Computed using the base year as 2010 (2010=100).
Labor force statistics (TUIK): Unemployment rates by age groups (%).

* **Consumer price index (TUIK):** Consumer price index (CPI) measures the change in the price of a market basket. CPI changes represent inflation changes. ([Ref](https://www.bls.gov/cpi/))

* **Gross domestic product (TUIK):** Gross domestic product (GDP) is defined as “the total monetary or market value of all the finished goods and services produced within a country’s borders in a specific time period.”  ([Ref](https://www.investopedia.com/terms/g/gdp.asp))

* **Industrial Production Index (TUIK):** The industrial production index measures the changes in the output of different industries. The 2015 based (2015=100) industrial production index was used. ([Ref](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Industrial_production_(volume)_index_overview#:~:text=The%20industrial%20production%20index%20(abbreviated,price%2Dadjusted%20output%20of%20industry.)))


* **Consumer Credits (TCMB):** Measured in thousands TRY
Current account deficit (TCMB): The difference between the export and import values measured in million USD.

* **Money supply (TCMB):** “The money supply is the total amount of money—cash, coins, and balances in bank accounts—in circulation.” ([Ref](https://www.federalreserve.gov/faqs/money_12845.htm#:~:text=The%20money%20supply%20is%20the,hold%20as%20short%2Dterm%20investments))
Interest rates (TCMB)

Real effective interest rate (TCMB): “Real effective exchange rate is the nominal effective exchange rate (a measure of the value of a currency against a weighted average of several foreign currencies) divided by a price deflator or index of costs.” ([Ref](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/PX.REX.REER#:~:text=Real%20effective%20exchange%20rate%20is,deflator%20or%20index%20of%20costs.&text=International%20Monetary%20Fund%2C%20International%20Financial%20Statistics))

* **Retail sales (TCMB):** Retail sales reflect the spending in various retail categories. ([Ref](https://www.investopedia.com/terms/core-retail-sales.asp#:~:text=The%20term%20core%20retail%20sales,sales%20and%20core%20retail%20sales))

* **Gold and oil prices**

| ![companies_per_sector](https://github.com/YZouzou/CS512-project/blob/main/figures/companies_per_sector.png) | 
|:--:| 
| *Fig. 1. Number of companies in each sector* |

The market capitalization value was used as a proxy for sectoral growth in this study. Market capitalization is the total value of a company’s outstanding shares (Ref). The reason behind using market capitalization instead of directly using stock prices is that stocks are often subjected to splits which change the number and prices of shares, without altering the total market value. Thus, market capitalization is a more consistent value than stock prices. Market capitalization data was collected from Istanbul Borsa’s official website. The dataset includes monthly market capitalization values of 215 companies from 2009 until the end of 2019. We chose to exclude the years after 2019 to avoid the drastic market changes that occurred post-2019 due to the pandemic. These companies belong to 28 different sectors as shown in Fig. 1. Time series of these companies based on their sectors are shown in Fig. 2 for the first 15 sectors by company count.

| ![sector_timeseries](https://github.com/YZouzou/CS512-project/blob/main/figures/sector_timeseries.png) | 
|:--:| 
| *Fig. 2. 6-Months change (%) in market values of companies in different sectors* |






