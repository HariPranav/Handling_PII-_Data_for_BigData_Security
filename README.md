# Handling_PII_Data_for_BigData_Security

![image](https://user-images.githubusercontent.com/28874545/180237331-9b139366-fb17-441f-8b1a-dde7b16c9e5a.png)

Data engineering often requires multiple data sources to realize the end goal of dashboard creation as per the business use case.
During this process of data ingestion, we often encounter customer data with which they can be traced back to the individual.
This data is also known as **Personal Identification Data** and if this data is compromised, then it can lead to identity theft, falsification of account and fraud. Some examples of PII data are :

1. Name

2. Address

3. Phone Number

4. Date of Birth

5. Passport Number .... etc

There are multiple laws across the world which give guidelines on how the data must be encrypted and stored in the **Cloud**. And there are Standard Operating Procedures (SOP) in place which highlight how this data must be handled. In this blog post we will be discussing how to handle PII data on the cloud.

1. We will be hosting a jupyter notebook in an EC2 instance
2. Then connect the notebook to the Source SQL server and the AWS Cloud
3. Write queries in the notebook to check the data quality **DQ CHECKS**
4. Based on the results from Step 3 we will use a Jupyter Notebook widget called **QGRID** which gives us editable pandas data frame
5. Push the data frame to AWS along with the encrypted fields

6. Create a new Ec2 instance and Install Jupyter notebook

Follow the link below to create an EC2 instance on AWS and install Jupyter notebook

[Ec2 instance Creation](https://dataschool.com/data-modeling-101/running-jupyter-notebook-on-an-ec2-server/)

2. Connect the jupyter notebook to AWS and Source DB

We need to install the AWS Cli on the EC2 instance in order to interact with the services like Athena, Glue and S3 which are required for Big Data Engineering Platforms. Click on the link below to install the AWS Cli.

[AWS CLI installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Once the CLI is installed, we need to install the Qgrid, awswrangler, pandas, numpy Libraries. Hence open the command line and install the packages as shown below:

    $ pip install qgrid

    $ pip install awswrangler

    $ pip install pandas

    $ pip install numpy

Here the **AWSWRANGLER** package relies on the **AWS CLI** to be installed to access the resources.

3. Queries to check the data quality

There are multiple queries that can be run to check the dataquality before sending it to the cloud for analysis.

a. For Phone Numbers :

    Check the length of the number based on the Geographic Location

b. For Pan Card:

    Pan card first 5 characters must be alphabets followed by numbers

c. Name:

    Should not be null, Should not contain numerical values, and should not have special characters

d. Email ID:

    Should not be null and except @ symbol there should be no special character in-between

The image below describes how this query can be written

![image](https://user-images.githubusercontent.com/28874545/180230052-c22c3e96-273c-42a3-88dc-29dd8f963fbd.png)

Next we need to mask the data so that it cannot be identified back to the individual, this can be done on the source system using an SQL **stuff and update** command as shown below:

The STUFF() function deletes a part of a string and then inserts another part into the string, starting at a specified position.

Syntax :

STUFF(string, start, length, new_string)

Usage:

    update table set column_name=STUFF(column_name,2,20,'XXXXXXXXXXXXXXX')

We can also use encryption in AWS Athena and use the SHA256 algorithm to encrypt the data once its in the cloud as shown below

    Select sha256(to_utf8(cast(name as varchar))) as encrypted_name from table_name

4,5. Qgrid widget to get the data as an editable data frame

    // Read the data USING the **wr** library and store the data into a dataframe

    df = wr.athena.read_sql_query("select * from table_name", database="database_name")

    //Add a new column called y/n to the dataframe

    df=df[["y/n","cust_details"]]

    //Make all columns to false by default

    df["y/n"] = df['name'] == ''

    //Make all the other columns non editable

    col_opts = { 'editable': False,'toolTip':"Not editable"}

    //Make only the 'y/n' column as editable

    col_defs = { 'y/n': { 'editable': True,'toolTip':"editable"} }

    //print df to check if the dataframe is editable

    df

    //Make the Grid Editable to allow the user to access the data.

    df3=qgrid.show_grid(df, column_options=col_opts, column_definitions=col_defs,grid_options={'forceFitColumns': False, 'defaultColumnWidth': 200})

    // Print the latest edited dataframe

    df4=df3.get_changed_df()

    //Push the New data frame with the Edited Column to AWS:

    bucket = 'input_bucketname'

    path1 = f"s3://{bucket}/file1.csv"

    //Write the csv file to the S3 bucket

    wr.s3.to_csv(df4, path1, index=False)

When the run the above Code and print **df**

![image](https://user-images.githubusercontent.com/28874545/180228025-9dff1334-c062-4dcb-9678-52a3cb85725f.png)

When we run the code to print **df4**

![image](https://user-images.githubusercontent.com/28874545/180228481-31af1ba3-579c-497c-b32f-7017b957cb9e.png)
