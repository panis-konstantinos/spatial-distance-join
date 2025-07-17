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


## Resources Distribution Scenarios
We tested four different resource allocation configurations for each value of the parameter 𝜀 and recorded the execution time of Query A. In all tests, the parameter cell_factor was set to 4. The four different scenarios correspond to the following cases:

* Use of a single machine with all cores (scenarios 1.*)
  
* Distribution of the computational load across all available resources (scenarios 2.*)

* Maximum use of all available resources with small executors (scenarios 3.*)

* Fewer executors with higher computational power per executor (scenarios 4.*)

We can observe that the best overall performance in terms of execution time is achieved when the number of executors is set to 4 ( scenarios 4.* ). Specifically, in this case, the execution times in seconds for 𝜀 values of 0.003, 0.006, and 0.012 are 153.18, 169.92, and 186.55 respectively. These times are relatively close to those in the scenario where 8 executors are used in total (160.65, 165.50, and 210.31 respectively). However, it appears that in the first case (4 executors), better scalability is achieved, as the execution time for 𝜀 = 0.012 is significantly lower than in the second case (8 executors). This indicates that our algorithmic approach performs better with fewer resources but with greater computational power per executor. This is further confirmed by the fact that when all available resources are used (16 executors) with lower computational power per executor, execution time increases dramatically, even exceeding that of scenarios 1.*, where a single executor is used.

| Scenario | Description              | Master | DeployMode | DriverMem. | Exec.Mem. | Exec.Cores | #Execs | 𝜀     | Exec.Time (s) |
|----------|--------------------------|--------|------------|------------|-----------|------------|--------|-------|----------------|
| 1.1      | SingleExecutor           | yarn   | client     | 1g         | 1g        | 4          | 1      | 0.003 | 162.25         |
| 1.2      | SingleExecutor           | yarn   | client     | 1g         | 1g        | 4          | 1      | 0.006 | 181.69         |
| 1.3      | SingleExecutor           | yarn   | client     | 1g         | 1g        | 4          | 1      | 0.012 | 253.62         |
| 2.1      | MultiExec. (Moderate)    | yarn   | client     | 1g         | 2g        | 2          | 8      | 0.003 | 160.65         |
| 2.2      | MultiExec. (Moderate)    | yarn   | client     | 1g         | 2g        | 2          | 8      | 0.006 | 165.50         |
| 2.3      | MultiExec. (Moderate)    | yarn   | client     | 1g         | 2g        | 2          | 8      | 0.012 | 210.31         |
| 3.1      | MaxParallel (SmallExecs) | yarn   | client     | 2g         | 1500m     | 1          | 16     | 0.003 | 175.75         |
| 3.2      | MaxParallel (SmallExecs) | yarn   | client     | 2g         | 1500m     | 1          | 16     | 0.006 | 180.94         |
| 3.3      | MaxParallel (SmallExecs) | yarn   | client     | 2g         | 1500m     | 1          | 16     | 0.012 | 268.20         |
| 4.1      | FewerExec. (MoreCores)   | yarn   | client     | 1g         | 3g        | 4          | 4      | 0.003 | 153.18         |
| 4.2      | FewerExec. (MoreCores)   | yarn   | client     | 1g         | 3g        | 4          | 4      | 0.006 | 169.92         |
| 4.3      | FewerExec. (MoreCores)   | yarn   | client     | 1g         | 3g        | 4          | 4      | 0.012 | 186.55         |

**NOTE**: Visualisation of the above experiment results is available in [experiment_results](resources_scens_plot.png)
