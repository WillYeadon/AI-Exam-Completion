import pandas as pd
import pingouin as pg

totals_data = pd.read_excel('../marking-results.xlsx', sheet_name='Totals')
totals_data_long = totals_data.reset_index().melt(id_vars=['index'], var_name='Rater', value_name='Rating')

# Calculate the ICC
icc = pg.intraclass_corr(data=totals_data_long, targets='index', raters='Rater', ratings='Rating').round(3)
print(icc)