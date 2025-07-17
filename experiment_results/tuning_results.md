## Experiments Methodology
In order to assess the algorithm's efficiency we measured its execution time for different parameter values and available resources distribution. The experiments were categorized into the following scenario types:

* **Algorithm Parameters Scenarios**: Examined different values for input parameters ε, k and cell_factor
* **Resources Distribution Scenarios**: Run the application with different utilization of availablle resources

  
## Algorithm Parameters Scenarios
In order to properly configure the value of the parameter cell_factor, we tested different values in combination with a range of values for the distance threshold parameter 𝜀. Regarding question B, we tested the same combinations while keeping the threshold value constant for the number of pairs k equal to 200. For these specific tests, the Spark program was submitted with the values:
master=yarn, deploy=client, driver-memory=1g, executor-memory=2g, executor-cores=2, and num-executors=8. 

As shown in Table 1, as the value of the cell_factor parameter increases, the points are distributed into grids of smaller dimensions, increasing the number of candidate pairs that result from the spatial data join. In fact, we observe that the number of candidate pairs reaches up to around one billion for 𝜀 = 0.012 and cell_factor = 10. Regarding execution time, as shown in Figure 1, we observe that for 𝜀 = 0.003 and 0.006, the minimum execution time occurs at cell_factor = 4. However, for 𝜀 = 0.012, the minimum is observed at cell_factor = 2. We also note that execution time increases as the distance parameter 𝜀 increases, due to the increase in candidate pairs. Similar results are obtained for the execution time of query B. Notably, despite the larger number of candidate pairs generated at cell_factor = 4, the execution time is minimized at this point in most of the tests. This is due to the fact that in order to benefit from the parallel processing provided by the Spark environment, it is necessary to have a significant volume of data to process, so that all available resources can be utilized effectively. For this reason, we selected 4 as the best value for the cell_factor parameter.
