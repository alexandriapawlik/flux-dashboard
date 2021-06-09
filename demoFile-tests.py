# move to root of project directory to use
from src import DataTable

# create external file with .tst extension, exclude header
dt = DataTable.DemoFile('src/testing/06082021.tst')
dt2 = DataTable.DemoFile('src/testing/06092021.tst')

# print(dt.filename)
# print(dt2.filename)

df = dt.create_df()
df2 = dt2.create_df()

print(df)
print(df2)