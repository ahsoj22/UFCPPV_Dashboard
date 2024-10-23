import kaggle
import pandas as pd
from sklearn.preprocessing import StandardScaler


kaggle.api.authenticate()

kaggle.api.dataset_download_files('daverosenman/ufc-ppv-sales', path = './data', unzip = True)
kaggle.api.dataset_download_files('rajeevw/ufcdata', path = './data', unzip =True)

fight_details = pd.read_csv('./data/data.csv')
ppv_buys = pd.read_csv('./data/ufc_ppv_buys.csv')

ppv_buys['date'] = pd.to_datetime(ppv_buys[['Year', 'Month', 'Day']])
fight_details['date'] = pd.to_datetime(fight_details['date'])
merged_data = pd.merge(fight_details, ppv_buys[['date', 'PPV']], on='date', how='inner')
merged_data = merged_data.dropna(subset=['PPV'])
merged_data.fillna(merged_data.mean(numeric_only=True), inplace=True)

merged_data.to_csv('./data/merged_ufc_data.csv', index=False)