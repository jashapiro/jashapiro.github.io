---
layout: Rmd
title: "Recapture: Calculations & Simulations"
pretitle: Biol B215
parent: index.html
tags: [R, tutorial, RStudio, BiolB215]
nav: teaching
---

[back to Introduction](capture_recapture.html)



## Calculating Population Size
Recall that we can estimate the population size $N$ from the number of individuals caught in the first round $M$, the number caught in the second round $C$, and the number of the second round that had already been captured $R$ using the equation $N=\frac{MC}{R}$. If we did a version of our experiment capturing and marking 100 individuals in our first trapping, then 240 in the second trapping, of which 3 were marked, we would calculate the number of individuals as follows:

```r
M <- 100
C <- 240
R <- 3
est_N <- M * C / R
est_N
```

```
## [1] 8000
```
That works, but if we were doing this many times, we could easily make a mistake with the formula at some point, and we would like to avoid that if possible. The best way to do that is to write a new function in `R` to perform the calculation. 

### Functions in R
Functions are one of the real strengths of `R` (and really any programming language), since they allow you to run the same analysis repeatedly with different sets of input data, without having to copy and paste large chunks of code, avoiding copying errors, and without cluttering up your workspace with all of the intermediate results. To define a function, you use the `function()` command, which takes as its arguments the names of the arguments that your new function will take. The commands that make up the function are then put in curly braces, `{}`, and can use the arguments you just defined as variables within the function. The last line of your function should usually be a `return()` statement. Whatever you put in that statement will be the output of the function.

To be more explicit, here is an example of a function that calculates the estimated population size. 


```r
recapturePopSize <- function(first, second, recaught){
  N_est <- first * second / recaught
  return(N_est)
}

recapturePopSize(first = 100, second = 240, recaught = 3)
```

```
## [1] 8000
```

Note that just as with the built-in functions, if we give the arguments in the correct order, we don't actually have to name them when we use the function: `recapturePopSize(100, 240, 3)` would have worked as well as the more explicit version above.

## Simulating the experiment
Now let's see how well our estimate of the population size from a capture-recapture experiment actually works. Let's assume that the true population size is exactly 3000 lizards. On the first trip we capture and mark 100. When we rerelease them, then the total population will consist of 50 marked individuals and 2900 unmarked lizards, which we will represent as a vector of strings: 100 with the value of `"marked"` and the remaining 2900 `"unmarked"`. On our second trip we will capture 240 individuals, just as in the example above. We will simulate this capture using the `sample()` function, which picks elements from a list randomly without replacement (unless you tell it differently). We will sample 240 individuals from the population vector, then count the number of those that are `"marked"`.


```r
# create the population vector with marked & unmarked 
marked_pop <- rep(c("marked", "unmarked"), c(100, 2900))
# sample from that population
trapped <- sample(marked_pop, 240)
n_marked <- sum(trapped == "marked")
n_marked
```

```
## [1] 7
```

```r
recapturePopSize(100, 240, n_marked)
```

```
## [1] 3429
```

Doing this one time doesn't tell us much about the distribution of our estimate, so we can write a function to do the simulation, with arguments that specify the total population size and the number of individuals captured in the first and second trappings. 

```r
simRecapture <- function(popsize, first, second){
  population <- rep(c("marked", "unmarked"), c(first, popsize - first))
  trapped <- sample(population, second)
  return ( sum(trapped == "marked") )
}

simRecapture(3000, 100, 240)
```

```
## [1] 7
```
Then we can use a function called `replicate()` to call this function many times with the same arguments. Each time it runs it will choose a different random sample from the population, so we will get different results. Let's run it  10 times for now, then calculate the estimated population sizes for each sample using our `recapturePopSize()` function. Notice that this function works just as we might have hoped when we give it a vector rather than a single value, even though we didn't do anything special when we wrote it. 

```r
sim_recaptures <- replicate(10, simRecapture(3000, 100, 240))
sim_recaptures
```

```
##  [1]  7 10  6  3 11  6  7  4  6  4
```

```r
recapturePopSize(100, 240, sim_recaptures)
```

```
##  [1] 3429 2400 4000 8000 2182 4000 3429 6000 4000 6000
```


It turns out that making the population vector every time is pretty slow, so if we were to do a lot of simulations, this would be pretty slow to calculate. Luckily, we can take advantage of a function built into `R` that can do the same kind of sampling much more quickly. The second capture is very much like the binomial sampling that we have seen before, in that we are sampling individuals of two kinds (marked and unmarked) from a population where we know what the frequency of each kind, but unlike with a binomial distribution, we are capturing individuals *without* replacement. This makes it into something called a hypergeometric distribution, which has the following probability function, where the variables are the same as those we defined earlier:
$$\Pr(R) = \frac{\binom{M}{R}\binom{N-M}{C-R}}{\binom{N}{C}}$$
To draw randomly from this distribution in `R`, we use the `rhyper()` function (`r` for random, `hyper` for hypergeometric). This takes four arguments:  
`nn` - the number of times we want to draw from the distribution (the number of trials or simulations)  
`m` - the number of marked individuals ($M$ in the equation above)  
`n` - the number of unmarked individuals ($N-M$ in the equation above)  
`k` - the number of individuals to choose for each sample ($C$ above)  

To create a set of 10 samples with this function which is equivalent to the functions above, we would do the following:

```r
sim_recaptured <- rhyper(nn = 10, m = 100, n = 2900, k = 240)
sim_recaptured
```

```
##  [1]  7 11  5  7  6 12 12 11  7  5
```

We can wrap the simulation and estimation into a single function to do the simulation and estimation in one step, then return a data frame with each row representing all of the parameters for each simulation and its results.


```r
simRecapture2<- function(popsize, first, second, reps = 1){
  recaught <- rhyper(nn = reps, m = first, n = popsize - first, k = second)
  pop_est <- recapturePopSize(first, second, recaught)
  return(data.frame(popsize, 
                    first, 
                    second, 
                    recaught, 
                    pop_est)
         )
}
simRecapture2(3000, 100, 240, reps = 5)
```

```
##   popsize first second recaught pop_est
## 1    3000   100    240       13    1846
## 2    3000   100    240        7    3429
## 3    3000   100    240        7    3429
## 4    3000   100    240        8    3000
## 5    3000   100    240        8    3000
```

### A Better Estimate
It turns out that this simple estimate of the population size is somewhat biased. This is perhaps easiest to see if you think about the case when you don't capture any marked individuals (you may have some of those in the data you simulated). Then $R = 0$, and the population is estimated to be of infinite size, which is never a good thing. A somewhat better estimator is the **Schnabel** method: 
$$\hat{N} = \frac{(M+1)(C+1)}{R+1} - 1 $$

{: .problem-nonum}
Write a function to estimate the number of individuals in the population using the Schnabel method.  
**a.**  Using as the true population size the number of lizards you estimated were in the box, simulate 1000 experiments where you capture 170 individuals in the first trapping and 170 in the second. Be sure to store the data from these (and the following) simulations, as you will need to use them for later problems as well. Generate a histogram of the estimated population sizes that you calculated with the Schnabel method.  
**b.**  How do your results change if you captured 200 individuals in the first trapping? What about if you caught 200 in the second (and 140 in the first)? It may be helpful to combine all of your results into a single data frame, and use `ggplot2`/`qlot()` to make all of the histograms together.  
**c.**  For each of the three experimental designs above, calculate the mean squared error of the Schnabel estimate ($\mathrm{MSE} = \frac{\sum(\hat{N}_i - N)^2}{n}$, where $\hat{N}_i$ is your estimate from the each simulation, $N$ is the population size you simulated, and $n$ is the number of simulations). Which gave the best estimate of the actual population size? Do you think it is better to put more effort into your first or second sample?  


## Completing the Experimental Design
Using your results from the above simulations, and any more simulations you might want to do (recording all of your results!), come up with a plan for the sampling scheme that you think the class should use. What should we do to get the most accurate and precise results?

{: .problem-nonum}
Write up your calculations and simulations in an Rmarkdown document that describes what you did to determine the best sampling scheme for the lizard capture. You will present this to a classmate at the next lab period, then the class will decide as a whole what the lizard sampling scheme will be.   
*Note:* You should use your solution to the previous problem(s) in your writeup, but you do not need to explicitly label those solutions. Your writeup should be a narrative that explains what you did and why, and the conclusions that you drew from your simulations.

## Next
Now that we have a sampling scheme, we will try to get the best estimate of the number of lizards in the population *and our uncertainty about that number*.

**[Error and likelihood](capture_recapture3.html)**
