import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

import comtradeapicall
import pandas as pd
import time

subscription_key = "6ac5204effef4564b01c24d70547ee61"

years = list(range(2015, 2024))
countries_to_track = ['Malaysia', 'Other Asia, nes', 'Rep. of Korea', 'China', 'Viet Nam', 'Thailand']
results = []

for year in years:
    print(f"Pulling {year}...")
    
    df = comtradeapicall.getFinalData(
        subscription_key,
        typeCode='C',
        freqCode='A',
        clCode='HS',
        period=str(year),
        reporterCode='842',
        cmdCode='8542',
        flowCode='M',
        partnerCode=None,
        partner2Code=None,
        customsCode=None,
        motCode=None,
        format_output='JSON',
        includeDesc=True
    )
    
    if df is None or len(df) == 0:
        print(f"  No data for {year}, skipping")
        continue
    
    slim = df[['partnerCode', 'partnerDesc', 'primaryValue']]
    slim = slim[slim['partnerCode'] != 0]
    
    total = slim['primaryValue'].sum()
    slim['share'] = slim['primaryValue'] / total
    
    hhi = ((slim['share'] * 100) ** 2).sum()
    
    row = {'year': year, 'hhi': hhi}
    
    for country in countries_to_track:
        match = slim[slim['partnerDesc'] == country]
        row[country] = match['share'].values[0] * 100 if len(match) > 0 else 0
    
    results.append(row)
    time.sleep(1)

results_df = pd.DataFrame(results)
print("\n--- Full Trend ---")
print(results_df)

results_df.to_csv('semiconductor_hhi_trend_expanded.csv', index=False)
print("\nSaved to semiconductor_hhi_trend_expanded.csv")