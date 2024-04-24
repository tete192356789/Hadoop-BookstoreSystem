import sys
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName('BookSys_spark_job').enableHiveSupport().getOrCreate()

df = spark.sql("select * from default.customers")

clean_df = df.withColumn("customer_name", trim(col("customer_firstname"))) \
                    .withColumn("customer_since",to_date(col("customer_since"),"yyyy-MM-dd").cast("string")) \
                    .withColumn("loyalty_card_number",regexp_replace("loyalty_card_number",'\"', '')) \
                    .withColumn("birthdate",to_date(col("birthdate"),"yyyy-MM-dd").cast("string")) \
                    .withColumn("gender", when(df['gender'] == "M",'MALE')
                                .when(df['gender'] =='F','FEMALE')
                                .otherwise('NA'))

final_cust_df = clean_df.selectExpr("customer_id as cust_id", \
                                        "customer_name as cust_nm", \
                                        "customer_email as cust_email", \
                                        "customer_since as cust_strt_dt", \
                                        "loyalty_card_number as cust_member_card_no", \
                                        "birthdate as cust_birth_dt", \
                                        "birth_year as cust_birth_yr",\
                                        "gender as cust_gender")

selected_df = clean_df.select(col('customer_id').alias('cust_id'),
                              col('customer_name').alias('cust_nm'),
                              col('customer_email').alias('cust_email'),
                              col('customer_since').alias('cust_strt_dt'),
                              col('loyalty_card_number').alias('cust_member_card_no'),
                              col('birthdate').alias('cust_birth_dt'),
                              col('birth_year').alias('cust_birth_yr'),
                              col('gender').alias('cust_gender'),
                              )

selected_df.write.mode('overwrite').save('/tmp/default/customers_clean/')
spark.stop()