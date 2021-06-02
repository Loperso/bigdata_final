from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import types
from pyspark.sql import functions as f
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, to_date, from_unixtime, date_format
from pyspark.sql.types import DoubleType, StringType, DateType
import requests
import time

def process(row):
        datos = {'time': row['TIMESTAMP'],'min': row['MIN'], 'max': row['MAX'], 'avg': row['AVG']}
        requests.post('http://172.31.50.178:8080/', data=datos)



spark = SparkSession.builder.appName('window-processing').getOrCreate()

sqlContext = SQLContext(sparkContext=spark.sparkContext, sparkSession=spark)


#Lee el csv
df = sqlContext.read.csv("/home/ubuntu/bigdata/SPY_TICK_TRADE.csv", header=True, inferSchema=True)

df = df.select('TIME', 'PRICE')
df_2 = df.withColumn('TIMESTAMP', df['TIME'].cast(StringType()))
df_3 = df_2.withColumn('DATE', from_unixtime('TIMESTAMP', 'dd-MM-yyyy-HH-mm-ss'))
df_4 = df_3.withColumn('DAY', f.split('DATE', '-')[0]).withColumn('MONTH', f.split('DATE', '-')[1]).withColumn('YEAR', f.split(f.split('Date', '-')[2], ' ')[0])

w_day = Window.partitionBy('DAY', 'MONTH', 'YEAR').orderBy('DATE')

df_5 = df_4.withColumn('TEST', f.row_number().over(w_day)).withColumn('MIN', f.min('PRICE').over(w_day)).withColumn('MAX', f.max('PRICE').over(w_day)).withColumn('AVG', f.avg('PRICE').over(w_day)).where(f.col("TEST")==1)

df_6 = df_5.sort('TIMESTAMP')

df_final = df_6.select('TIMESTAMP', 'MIN', 'MAX', 'AVG')

print(30*'*')
print('HEY')

for row in df_final.rdd.collect():
        if row['MIN'] != row['MAX']:
                time.sleep(5)
                print(30*'*')
                print(row)
                process(row)
