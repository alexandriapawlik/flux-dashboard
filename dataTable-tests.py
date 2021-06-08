from src import DataTable

# create external file with .tst extension, exclude header
dt = DataTable.TestFile('06082021.tst')
dt2 = DataTable.TestFile('06092021.tst')

print(dt.filename)
print(dt2.filename)