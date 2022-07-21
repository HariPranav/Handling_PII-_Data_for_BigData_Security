import time
import awswrangler as wr
import qgrid
import pandas as pd
import numpy as np

# Ec2-> jupyter -> source DB -> query -> S3 -> AWS



df = wr.athena.read_sql_query("select * from tablename", database="ocv_test")
df

df = wr.athena.read_sql_query("select * from table_name", database="database_name")

# testing 
df['y/n'] = ""
#df['choice'] = []


#df = df.drop(columns='0')
#df

# rearrange the "y/n" column to come in the begining

df["y/n"] = df['_name'] == ''

#df.head()

# make the last "y/n" column editable
col_opts = { 'editable': False,
           'toolTip':"Not editable"}
col_defs = { 'y/n': { 'editable': True,
                  'toolTip':"editable"} }
df3=qgrid.show_grid(df, column_options=col_opts, column_definitions=col_defs,grid_options={'forceFitColumns': False, 'defaultColumnWidth': 200})
df3
#type(df3)


# Print the latest edited dataframe

df4=df3.get_changed_df()

#Push the New data frame with the Edited Column to AWS:

bucket = 'input_bucketname'

path1 = f"s3://{bucket}/file1.csv"

#Write the csv file to the S3 bucket

wr.s3.to_csv(df4, path1, index=False)
