# Run entire R system provided all files are in the right directories
python2 preprocessing.py listings.csv result.csv prices.csv
Rscript learn.R
