from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, explode, floor, sequence, lit, min, max, avg
from pyspark.sql.types import StructType, StructField, IntegerType, ArrayType, LongType
import time
import os
import csv
import math

def read_submit_conf(spark):
    conf = spark.sparkContext.getConf()

    arealm_path = conf.get("spark.query.pathA")
    rails_path = conf.get("spark.query.pathR")
    output_path = conf.get("spark.query.output")
    eps = float(conf.get("spark.query.eps"))
    cell_factor = int(conf.get("spark.query.cellFactor"))
    k = conf.get("spark.query.k", "Not Set")
    deploy_mode = conf.get("spark.submit.deployMode", "Not Set")
    driver_memory = conf.get("spark.driver.memory", "Not Set")
    executor_memory = conf.get("spark.executor.memory", "Not Set")
    executor_cores = conf.get("spark.executor.cores", "Not Set")
    num_executors = conf.get("spark.executor.instances", "Not Set")

    return arealm_path, rails_path, output_path, eps, cell_factor, k,\
           deploy_mode, driver_memory, executor_memory, executor_cores, num_executors

def read_files(spark, arealm_path, rails_path):
    df_s = spark.read.csv(header=False, inferSchema=True, path=arealm_path, sep='\t') 
    df_r = spark.read.csv(header=False, inferSchema=True, path=rails_path, sep='\t') 
    return df_s, df_r

def compute_grid_cells(x_min, x_max, y_min, y_max, cell_size):
    # Compute number of grid cells based on spatial bounds and distance threshold.
    m_x = math.ceil((x_max - x_min) / cell_size) - 1
    m_y = math.ceil((y_max - y_min) / cell_size) - 1
    return m_x, m_y

def rename_columns(df_s, df_r):
    df_s2 = df_s.withColumnRenamed("_c0", "id").withColumnRenamed("_c1", "lon").withColumnRenamed("_c2", "lat")
    df_r2 = df_r.withColumnRenamed("_c0", "id").withColumnRenamed("_c1", "lon").withColumnRenamed("_c2", "lat")

    return df_s2, df_r2

def tag_cells_r(df, alias, x_min, y_min, epsilon, cell_size):
    df2 = df.withColumn("min_cell_x", floor((col("lon") - lit(x_min) - lit(epsilon)) / lit(cell_size))) \
            .withColumn("max_cell_x", floor((col("lon") - lit(x_min) + lit(epsilon)) / lit(cell_size))) \
            .withColumn("min_cell_y", floor((col("lat") - lit(y_min) - lit(epsilon)) / lit(cell_size))) \
            .withColumn("max_cell_y", floor((col("lat") - lit(y_min) + lit(epsilon)) / lit(cell_size)))

    df3 = df2.withColumn("cell_x", explode(sequence(col("min_cell_x"), col("max_cell_x")))) \
             .withColumn("cell_y", explode(sequence(col("min_cell_y"), col("max_cell_y"))))

    df_with_cells = df3.withColumn("cell_id", (col("cell_x") * 10000 + col("cell_y")).cast(LongType())) \
                       .select(col("id").alias(f"{alias}_id"), \
                               col("lon").alias(f"{alias}_lon"), \
                               col("lat").alias(f"{alias}_lat"), \
                               col("cell_id"))

    return df_with_cells

def tag_cells_s(df, alias, x_min, y_min, cell_size):
    return df.withColumn("cell_x", floor((col("lon") - lit(x_min)) / lit(cell_size))) \
            .withColumn("cell_y", floor((col("lat") - lit(y_min)) / lit(cell_size))) \
            .withColumn("cell_id", (col("cell_x") * 10000 + col("cell_y")).cast(LongType())) \
            .select(col("id").alias(f"{alias}_id"), \
                    col("lon").alias(f"{alias}_lon"), \
                    col("lat").alias(f"{alias}_lat"), \
                    col("cell_id"))

def get_cells_dist(R_tagged, S_tagged):
    r_cells = R_tagged.groupBy("cell_id").count()
    s_cells = S_tagged.groupBy("cell_id").count()
    stats_r = r_cells.agg(
        min("count"),
        max("count"),
        avg("count")
    )
    stats_s = r_cells.agg(
        min("count"),
        max("count"),
        avg("count")
    )

    stats_r.coalesce(1).write.mode("overwrite").text("/home/user/stats_r")
    stats_s.coalesce(1).write.mode("overwrite").text("/home/user/stats_s")
    r_cells.coalesce(1).write.mode("overwrite").text("/home/user/r_cells")
    s_cells.coalesce(1).write.mode("overwrite").text("/home/user/s_cells")

def queryA(R_tagged, S_tagged, eps, mode=None):
    
    if mode == None:
        # Join on cell ID (PBSM partition) and filter locally
        joined = R_tagged.join(S_tagged, on="cell_id") \
                        #.dropDuplicates(["r_id", "s_id"])
                        #.filter(col("r_id") < col("s_id"))   # Prevent duplicate unordered pairs

        # Add distance column and filter by epsilon
        result = joined.withColumn("distance", ((col("s_lon") - col("r_lon"))**2 + (col("s_lat") - col("r_lat"))**2)**0.5) \
                    .filter(col("distance") <= eps) \
                    .dropDuplicates(["r_id", "s_id"])

        cnt = result.count()

        return cnt
    else:
        return R_tagged.join(S_tagged, on="cell_id").count()

def queryB(R_tagged, S_tagged, eps, k):
    # Join on cell ID (PBSM partition) and filter locally
    joined = R_tagged.join(S_tagged, on="cell_id") \
                    #.dropDuplicates(["r_id", "s_id"])
                    #.filter(col("r_id") < col("s_id"))   # Prevent duplicate unordered pairs

    # Add distance column and filter by epsilon
    result = joined.withColumn("distance", ((col("s_lon") - col("r_lon"))**2 + (col("s_lat") - col("r_lat"))**2)**0.5) \
                    .filter(col("distance") <= eps) \
                    .dropDuplicates(["r_id", "s_id"]) \
                    .groupBy(col("r_id")) \
                    .count() \
                    .filter(col("count") > k) \
                    .cache()
                    

    cnt = result.count()

    return result, cnt

def write_result(spark, query, result, output):
    if query == "A":
        df = spark.createDataFrame([(str(result),)], ["count"])
        df.coalesce(1).write.mode("overwrite").text(output)
    else:
        # Step 2: Map each row to a string in the format "{id, count}"
        formatted_rdd = result.rdd.map(lambda row: f"{{{row['r_id']}, {row['count']}}}")

        # Step 3: Save as text file (to HDFS or local filesystem)
        formatted_rdd.coalesce(1).saveAsTextFile(output)

def write_metadata(eps, cell_factor, deploy_mode, driver_memory, executor_memory, executor_cores, num_executors, cnt, exec_time):
    conf = {
            "eps": eps,
            "cell_factor": cell_factor,
            "deploy_mode": deploy_mode,
            "driver_memory": driver_memory,
            "executor_memory": executor_memory,
            "executor_cores": executor_cores,
            "num_executors": num_executors,
            "cnt": cnt,
            "exec_time": exec_time
        }
    
    file_path = "/home/user/scenarios.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="") as f:
        field_names = list(conf.keys())
        writer = csv.DictWriter(f, field_names)
        if not file_exists:
            writer.writeheader()
        else:
            pass
        writer.writerow(conf)

def main():
    start_time = time.time()

    # Create Spark session
    spark = SparkSession.builder.appName("query").getOrCreate() # master to be removed in final script

    # Read submit configuration
    arealm_path, rails_path, output_path, eps, cell_factor, k,\
    deploy_mode, driver_memory, executor_memory, executor_cores, num_executors = read_submit_conf(spark)

    # Read files
    df_s, df_r = read_files(spark, arealm_path, rails_path)

    # Rename columns
    df_s2, df_r2 = rename_columns(df_s, df_r)

    # Define grid bounds, eps and cell size
    x_min, x_max = -124.763068, -64.564909
    y_min, y_max = 17.673976, 49.384360
    cell_size = cell_factor * eps

    # Tag cells to points
    R_tagged = tag_cells_r(df_r2, "r", x_min, y_min, eps, cell_size).repartition("cell_id").cache()
    S_tagged = tag_cells_s(df_s2, "s", x_min, y_min, cell_size).repartition("cell_id")

    # Query calculation
    if k == "Not Set":
        cnt = queryA(R_tagged, S_tagged, eps)
        end_time = time.time()
        write_result(spark, query="A", result=cnt, output=output_path)
    else:
        k = int(k)
        result, cnt = queryB(R_tagged, S_tagged, eps, k)
        end_time = time.time()
        write_result(spark, query="B", result=result, output=output_path)

    exec_time = end_time-start_time

    # Compute grid cells in axes
    m_x, m_y = compute_grid_cells(x_min, x_max, y_min, y_max, cell_size)
    candidates = queryA(R_tagged, S_tagged, eps, mode="test")
    #write_result(spark, cnt, output_path)
    #write_metadata(eps, cell_factor, deploy_mode, driver_memory, executor_memory, executor_cores, num_executors, cnt, exec_time)

    spark.stop()

    print(f"Result count: {cnt}")
    print(f"Cells on x: {m_x}")
    print(f"Cells on y: {m_y}")
    print(f"Candidate pairs: {candidates}")
    print(f"Execution time: {exec_time:.6f} seconds.")
    

if __name__=="__main__":
    main()