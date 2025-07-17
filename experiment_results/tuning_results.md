## Experiments Methodology
In order to assess the algorithm's efficiency we measured its execution time for different parameter values and available resources distribution. The experiments were categorized into the following scenario types:

* **Algorithm Parameters Scenarios**: Examined different values for input parameters ε, k and cell_factor
* **Resources Distribution Scenarios**: Run the application with different utilization of availablle resources

  
## Algorithm Parameters Scenarios
In order to properly configure the value of the parameter cell_factor, we tested different values in combination with a range of values for the distance threshold parameter 𝜀. Regarding question B, we tested the same combinations while keeping the threshold value constant for the number of pairs k equal to 200. For these specific tests, the Spark program was submitted with the values:
master=yarn, deploy=client, driver-memory=1g, executor-memory=2g, executor-cores=2, and num-executors=8. 

As shown in the table below as the value of the cell_factor parameter increases, the points are distributed into grids of smaller dimensions, increasing the number of candidate pairs that result from the spatial data join. In fact, we observe that the number of candidate pairs reaches up to around one billion for 𝜀 = 0.012 and cell_factor = 10. Regarding execution time we observe that for 𝜀 = 0.003 and 0.006, the minimum execution time occurs at cell_factor = 4. However, for 𝜀 = 0.012, the minimum is observed at cell_factor = 2. We also note that execution time increases as the distance parameter 𝜀 increases, due to the increase in candidate pairs. Similar results are obtained for the execution time of query B. Notably, despite the larger number of candidate pairs generated at cell_factor = 4, the execution time is minimized at this point in most of the tests. This is due to the fact that in order to benefit from the parallel processing provided by the Spark environment, it is necessary to have a significant volume of data to process, so that all available resources can be utilized effectively. For this reason, we selected 4 as the best value for the cell_factor parameter.

| Scenario | 𝜀     | cell_factor | CellsX | CellsY | CandidatePairs   | Exec.TimeA (s) | 𝑘   | Exec.TimeB (s) |
|----------|-------|-------------|--------|--------|------------------|----------------|------|----------------|
| 1.1      | 0.003 | 1           | 20066  | 10570  | 7,639,136        | 180.36         | 200  | 359.10         |
| 1.2      | 0.006 | 1           | 10033  | 5285   | 30,068,955       | 188.03         | 200  | 276.58         |
| 1.3      | 0.012 | 1           | 5016   | 2642   | 112,256,461      | 211.39         | 200  | 230.84         |
| 2.1      | 0.003 | 2           | 10033  | 5285   | 13,473,677       | 170.51         | 200  | 204.34         |
| 2.2      | 0.006 | 2           | 5016   | 2642   | 52,205,437       | 171.52         | 200  | 172.99         |
| 2.3      | 0.012 | 2           | 2508   | 1321   | 186,076,833      | 201.36         | 200  | 215.57         |
| 3.1      | 0.003 | 4           | 5016   | 2642   | 29,952,843       | 164.82         | 200  | 171.14         |
| 3.2      | 0.006 | 4           | 2508   | 1321   | 109,089,164      | 166.22         | 200  | 185.60         |
| 3.3      | 0.012 | 4           | 1254   | 660    | 373,249,850      | 210.99         | 200  | 232.39         |
| 4.1      | 0.003 | 8           | 2508   | 1321   | 77,124,365       | 169.85         | 200  | 161.10         |
| 4.2      | 0.006 | 8           | 1254   | 660    | 266,129,256      | 219.47         | 200  | 214.34         |
| 4.3      | 0.012 | 8           | 627    | 330    | 844,544,080      | 274.52         | 200  | 272.72         |
| 5.1      | 0.003 | 10          | 2006   | 1057   | 107,520,867      | 209.31         | 200  | 174.75         |
| 5.2      | 0.006 | 10          | 1003   | 528    | 361,872,569      | 191.27         | 200  | 200.14         |
| 5.3      | 0.012 | 10          | 501    | 264    | 1,145,967,946    | 268.65         | 200  | 304.27         |

**NOTE**: Visualisation of the above experiment results is available in [experiment_results](calculation_scens_plot.png)
