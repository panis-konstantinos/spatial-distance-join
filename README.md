# Overview
A distributed Spark application for analyzing spatial proximity between data points of two large datasets using Apache Spark and Hadoop. Given two CSV files (denoted as R and S) containing point data (id, longitude, latitude), the app computes:

* The number of point pairs (r in R, s in S) within a given distance ε

* All points in R that have at least k neighbors from S within distance ε

Designed to scale across a Hadoop cluster using PySpark for parallel processing.
