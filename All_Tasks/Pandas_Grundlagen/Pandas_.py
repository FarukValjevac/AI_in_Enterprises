import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

dow_jones_index = pd.read_csv("dow_jones_index.csv")
# columns_with_nan_values = dow_jones_index.columns[dow_jones_index.isna().any()].tolist()
# # Remove all non values, they will influence negatively the boxplot
# for i in range(len(columns_with_nan_values)):
#     dow_jones_index_no_none = dow_jones_index[dow_jones_index[columns_with_nan_values[i]].notna()]
#     i += 1
#
# dow_jones_index_numeric = dow_jones_index_no_none.select_dtypes(include=np.number)
# all_numeric_columns = list(dow_jones_index_numeric.columns)
#
#
# fig, axs = plt.subplots(int(len(all_numeric_columns)/4), int(len(all_numeric_columns)/2), figsize=(10, 7))
# axs = axs.ravel()
# # Plot all the boxplots where columns has numeric values
# for i in range(len(all_numeric_columns)):
#     axs[i].boxplot(dow_jones_index_numeric[all_numeric_columns[i]])
#     axs[i].set_title(all_numeric_columns[i])
# fig.suptitle('Boxplots for all columns with numeric values')
# plt.show()

# regex = '(\d+)'
#
dow_jones_index['date'] = pd.to_datetime(dow_jones_index['date'])
dow_jones_index = dow_jones_index.sort_values('date').reset_index(drop=True)
cisco = dow_jones_index.loc[dow_jones_index['stock'] == "CSCO"]
# cisco.to_csv(path_or_buf="./pandas.csv", header=True, decimal='.', sep=',', index=False)
# print()
#
pd.set_option('mode.chained_assignment', None)
cisco['close'] = cisco['close'].replace({'\$':''}, regex=True)
cisco['close'] = cisco['close'].astype(float)

cisco['high'] = cisco['high'].replace({'\$':''}, regex=True)
cisco['high'] = cisco['high'].astype(float)
cisco['low'] = cisco['low'].replace({'\$':''}, regex=True)
cisco['low'] = cisco['low'].astype(float)

cisco['newcol'] = cisco['high'] - cisco['low']

print(cisco)

# plt.plot(cisco['date'], cisco['close'])
# plt.xlabel('Date')
# plt.ylabel('$').set_rotation(0)
# plt.show()

