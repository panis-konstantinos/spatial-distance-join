## Experiments Methodology
In order to assess the algorithm's efficiency we measured its execution time for different parameter values and available resources distribution. The experiments were categorized into the following scenario types:

* **Algorithm Parameters Scenarios**: Examined different values for input parameters ε, k and cell_factor
* **Resources Distribution Scenarios**: Run the application with different utilization of availablle resources

  
## Algorithm Parameters Scenarios
In order to properly configure the value of the parameter cell_factor, we tested different values in combination with a range of values for the distance threshold parameter 𝜀. Regarding question B, we tested the same combinations while keeping the threshold value constant for the number of pairs k equal to 200. For these specific tests, the Spark program was submitted with the values:
master=yarn, deploy=client, driver-memory=1g, executor-memory=2g, executor-cores=2, and num-executors=8
