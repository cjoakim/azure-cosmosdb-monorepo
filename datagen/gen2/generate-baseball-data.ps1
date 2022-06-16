
# Generate the Baseball mongoexport files based on the
# Sean LahmanBaseball Databank files.
# Chris Joakim, Microsoft, May 2022

echo 'deleting output files ...'
rm data/*.json

python main.py create_baseball_base_mongoexport_files

python main.py create_baseball_large_document_count_data 5000
#python main.py create_baseball_large_document_count_data 1500000

# baseball_fantasy_teams.json 50000 docs = 1809371637
# >>> 1809371637.0 / (1024 * 1024 * 1024)
# 1.685108651407063 GB
# >>> (50.0 / 1.685) * 50000
# 1483679.525222552
# Therefore, 1.5 million docs will be just over 50GB

python main.py create_baseball_large_document_size_data 10
#python main.py create_baseball_large_document_size_data 1000

echo 'done'
