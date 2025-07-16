# Overview
A distributed Spark application for analyzing spatial proximity between data points of two large datasets using Apache Spark (PySpark) for the computations and Hadoop File System for file storage. Given two CSV files (denoted as R and S) containing data poins (id, longitude, latitude), the app computes:

* The number of point pairs (r in R, s in S) within a given distance ε

* All points in R that have at least k neighbors from S within distance ε

To address these queries, algorithms were designed and implemented using point grid partitioning techniques, aiming to reduce computational cost and avoid exhaustive pairwise comparisons. The implementation was based on the Spark DataFrame API and executed on real large-scale datasets. Through experimental evaluation, the performance of the algorithms was recorded for different parameter values (ε, k), highlighting the advantages of parallel processing and spatial proximity-based optimization. The results confirm the effectiveness of the approach in terms of both execution time and scalability.

# Development & Test Environment
The project was originally developed and tested on a 4-node cluster. Each node ran:

* **OS**: Ubuntu 16.04.3 LTS

* **Resources**: 4 CPU cores, 6 GB RAM, 10 GB disk

* **Software**: Apache Spark v3.5.1, Apache Hadoop v3.2.1

This setup was used to evaluate performance and scalability of the algorithms on real distributed infrastructure.The project was originally tested and developed on a 4-node cluster setup. Each node run on Ubuntu 16.04.3 LTS, had 6144ΜΒ RAM, 4 cores, 10GB hard disk and Apache Spark (version 3.5.1) and Apache Hadoop (version 3.2.1) installed.

# Methodology
The algorithm was implemented in the Python programming language using the Spark API for Python, PySpark, with a focus on leveraging Spark’s parallel processing capabilities. Key goals included execution performance and scalability. Data processing was implemented using Spark DataFrames, in order to optimize both physical and logical execution plans (through the Catalyst Optimizer) and improve in-memory storage efficiency.
The algorithm consists of two main parts. The first part involves partitioning the points into groups by dividing the space into grid cells and assigning each point to a cell. At this stage, it is important to replicate points into neighboring cells that are within a distance less than or equal to the threshold ε, in order to ensure that no candidate pair (r, s) is missed. The second part concerns the join of the two datasets, R and S, to form candidate pairs and compute the distance between them. After the distance is calculated, filtering based on ε and k thresholds is straightforward.
