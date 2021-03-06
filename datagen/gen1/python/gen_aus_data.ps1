# Recreate the python virtual environment and reinstall libs on Windows.
# Chris Joakim, Microsoft, November 2021

echo 'generating customers ...'
python main.py gen_customers 1000

echo 'generating products ...'
python main.py gen_products 1000

echo 'generating online txns using customers and products, redirecting to file ...'
python main.py gen_aus_online_txn 2021-02-25 2022-02-25 100 > data\online_txn.json

echo 'generating flybuy txns using customers and products, redirecting to file ...'
python main.py gen_aus_flybuy_txn 2021-02-25 2022-02-25 100 > data\flybuy_txn.json

echo 'done'
