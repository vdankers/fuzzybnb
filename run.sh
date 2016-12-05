python preprocessing.py listings.csv result.csv prices.csv
python trim_csv.py result.csv 1000 result_trim.csv
python trim_csv.py prices.csv 1000 prices_trim.csv
Rscript learn.R
