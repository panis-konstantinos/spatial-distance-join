# Overview
A distributed Spark application for analyzing spatial proximity between data points of two large datasets using Apache Spark and Hadoop. Given two CSV files (denoted as R and S) containing data poins (id, longitude, latitude), the app computes:

* The number of point pairs (r in R, s in S) within a given distance ε

* All points in R that have at least k neighbors from S within distance ε

To address these queries, algorithms were designed and implemented using point grid partitioning techniques, aiming to reduce computational cost and avoid exhaustive pairwise comparisons. The implementation was based on the Spark DataFrame API and executed on real large-scale datasets. Through experimental evaluation, the performance of the algorithms was recorded for different parameter values (ε, k), highlighting the advantages of parallel processing and spatial proximity-based optimization. The results confirm the effectiveness of the approach in terms of both execution time and scalability.
