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
Recall that we can estimate the population size $N$ from the number of individuals caught in the first round $M$, the number caught in the second round $C$, and the number of the second round that had already been captured $R$ using the equation $N=\frac{MC}{R}$. If we did a version of our experiment capturing and marking 50 individuals in our first trapping, then 150 in the second trapping, of which 3 were marked, we would calculate the number of individuals as follows:

{% highlight r %}
M <- 50
C <- 150
R <- 3
est_N <- M * C / R
est_N
{% endhighlight %}



{% highlight text %}
## [1] 2500
{% endhighlight %}
So our estimate would be that there are 2500 lizards in the population.

That works, but if we were doing this many times, we could easily make a mistake with the formula at some point, and we would like to avoid that if possible. The best way to do that is to write a new function in `R` to perform the calculation. 

### Functions in R
Functions are one of the real strengths of `R` (and really any programming language), since they allow you to run the same analysis repeatedly with different sets of input data, without having to copy and paste large chunks of code, avoiding copying errors, and without cluttering up your workspace with all of the intermediate results. We have already been using a number of different functions, such as `mean()` or `sd()`, or even the `qplot()` functions for plotting. Now it is time to define our own.


To define a function, you first type the name you want the function to have as a variable, and then use and arrow to assign to it the results of the `function()` command.  The `function()` command (itself a function) takes as its arguments the names of the arguments that your *new* function will take. The commands that make up the function are then put in curly braces, `{}`,  immediately following the `function()` statement, and can use the argument names you just defined as variables within the function. The last line of the series of statements inside the curly braces will be the output of the function.

To be more explicit, here is an example of a function that calculates the estimated population size. 


{% highlight r %}
recapturePopSize <- function(first, second, recaught){
  first * second / recaught
}

recapturePopSize(first = 50, second = 150, recaught = 3)
{% endhighlight %}



{% highlight text %}
## [1] 2500
{% endhighlight %}

Note that just as with the built-in functions, if we give the arguments in the correct order, we don't actually have to name them when we use the function: `recapturePopSize(50, 150, 3)` would have worked as well as the more explicit version above.

## Simulating the experiment
Now let's see how well our estimate of the population size from a capture-recapture experiment actually works. Let's assume that the true population size is exactly 2000 lizards. On the first trip we capture and mark 50. When we rerelease them, then the total population will consist of 50 marked individuals and 1950 unmarked lizards, which we will represent as a vector of strings: 50 with the value of `"marked"` and the remaining 1950 `"unmarked"`. On our second trip we will capture 150 individuals, just as in the example above. We will simulate this capture using the `sample()` function, which picks elements from a list randomly without replacement (unless you tell it differently). We will sample 150 individuals from the "population" vector, then count the number of those that are `"marked"`.


{% highlight r %}
# create the population vector with marked & unmarked 
marked_pop <- rep(c("marked", "unmarked"), c(50, 1950))
# sample from that population
trapped <- sample(marked_pop, 150)
n_marked <- sum(trapped == "marked")
n_marked
{% endhighlight %}



{% highlight text %}
## [1] 4
{% endhighlight %}



{% highlight r %}
recapturePopSize(50, 150, n_marked)
{% endhighlight %}



{% highlight text %}
## [1] 1875
{% endhighlight %}

Doing this one time doesn't tell us much about the distribution of our estimate, so we can write a function to do the simulation, with arguments that specify the total population size and the number of individuals captured in the first and second trappings. Notice that the actual code here is essentially identical to the code above, and we can include as many lines as we ant inside the curly braces of the function definition.


{% highlight r %}
simRecapture <- function(popsize, first, second){
  population <- rep(c("marked", "unmarked"), c(first, popsize - first))
  trapped <- sample(population, second)
  sum(trapped == "marked")
}

simRecapture(2000, 50, 150)
{% endhighlight %}



{% highlight text %}
## [1] 2
{% endhighlight %}

Now we can use a function called `replicate()` to call this function many times with the same arguments. Each time it runs it will choose a different random sample from the population, so we will get different results. Let's run it  10 times for now, then calculate the estimated population sizes for each sample using our `recapturePopSize()` function. Notice that this function works just as we might have hoped when we give it a vector rather than a single value, even though we didn't do anything special when we wrote it. 


{% highlight r %}
first_capture <- 50
second_capture <- 150
sim_recaptures <- replicate(10, simRecapture(2000, first_capture, second_capture))
sim_recaptures
{% endhighlight %}



{% highlight text %}
##  [1] 3 4 5 2 7 2 3 6 3 3
{% endhighlight %}



{% highlight r %}
recapturePopSize(first_capture, second_capture, sim_recaptures)
{% endhighlight %}



{% highlight text %}
##  [1] 2500.000 1875.000 1500.000 3750.000 1071.429 3750.000 2500.000
##  [8] 1250.000 2500.000 2500.000
{% endhighlight %}


It turns out that making the population vector every time is pretty slow, so if we were to do a lot of simulations, this would be pretty slow to calculate. Luckily, we can take advantage of a function built into `R` that can do the same kind of sampling much more quickly. The second capture is very much like the binomial sampling that we have seen before, in that we are sampling individuals of two kinds (marked and unmarked) from a population where we know what the frequency of each kind, but unlike with a binomial distribution, we are capturing individuals *without* replacement. This makes it into something called  hypergeometric sampling, which has the following probability function for the number of marked individuals recaptured, with all variables the same as those we defined earlier:

$$\Pr(R) = \frac{\binom{M}{R}\binom{N-M}{C-R}}{\binom{N}{C}}$$

To draw randomly from this distribution in `R`, we use the `rhyper()` function (`r` for random, `hyper` for hypergeometric). This takes four arguments:  
`nn` - the number of times we want to draw from the distribution (the number of trials or simulations)  
`m` - the number of marked individuals ($M$ in the equation above)  
`n` - the number of unmarked individuals ($N-M$ in the equation above)  
`k` - the number of individuals to choose for each sample ($C$ above)  

To create a set of 10 samples with this function which is equivalent to the functions above, we would do the following:

{% highlight r %}
sim_recaptured <- rhyper(nn = 10, m = 50, n = 1950, k = 100)
sim_recaptured
{% endhighlight %}



{% highlight text %}
##  [1] 3 4 5 2 3 3 4 1 2 3
{% endhighlight %}

We can wrap the simulation and estimation into a single function to do the simulation and estimation in one step, then return a data frame with each row representing all of the parameters for each simulation and its results.


{% highlight r %}
simEstimate<- function(popsize, first, second, reps = 1){
  recaught <- rhyper(nn = reps, m = first, n = popsize - first, k = second)
  pop_est <- recapturePopSize(first, second, recaught)
  
  data.frame(popsize, first, second, recaught, pop_est)
}
simEstimate(2000, 50, 150, reps = 5)
{% endhighlight %}



{% highlight text %}
##   popsize first second recaught pop_est
## 1    2000    50    150        6    1250
## 2    2000    50    150        4    1875
## 3    2000    50    150        1    7500
## 4    2000    50    150        3    2500
## 5    2000    50    150        3    2500
{% endhighlight %}

### A Better Estimate
It turns out that this simple estimate of the population size is somewhat biased. This is perhaps easiest to see if you think about the case when you don't capture any marked individuals (you may have some of those in the data you simulated). Then $R = 0$, and the population is estimated to be of infinite size, which is almost certainly an overestimate of the actual population size. A somewhat better estimator is the **Schnabel** method: 

$$\hat{N} = \frac{(M+1)(C+1)}{R+1} - 1 $$

Notice that in this method, the denominator can never be zero, so we will never get an infinite population size.

{: .question}
Write a function to estimate the number of individuals in the population using the Schnabel method.  
**a.**  Using as the true population size the number of lizards you estimated were in the box, simulate 1000 experiments where you capture 100 individuals in the first trapping and 100 in the second. Be sure to store the data from these (and the following) simulations, as you will need to use them for later problems as well. Generate a histogram of the estimated population sizes that you calculated with the Schnabel method.  
**b.**  How do your results change if you captured 130 individuals in the first trapping? What about if you caught 130 in the second (and 70 in the first)? It may be helpful to combine all of your results into a single data frame, and use `ggplot2`/`qlot()` to make a faceted plot of the histograms together.  


### Quantifying Error in each design
For each simulated experimental design, we would like to calculate some estimate of the overall error of our estimates, compared to the true population size. One measure we can use is the Mean Squared Error, the average of the squared difference between an estimate and the true value: 

$$\mathrm{MSE} = \frac{\sum\limits_{i=1}^n(\hat{N}_i - N)^2}{n}$$

where $\hat{N}_i$ is the popilation size estimate from the $i^\mathrm{th}$ simulation, $N$ is the population size you simulated, and $n$ is the number of simulations. (This should look somewhat familiar... what statistical quantity we have discussed in the past is this analagous to?) If we can minimize this MSE by adjusting our sampling scheme, then we will have a pretty good sense that we are getting good estimates of the total number of lizards in the population.


## Completing the Experimental Design
Using your results from the above simulations, and any more simulations you might want to do (recording all of your results!), try to come up with a plan for the sampling scheme that you think the class should use. What should we do to get the most accurate and precise results? You should test a number of different sampling schemes, and you may want to check that your "best" sampling scheme works for different true population sizes. All of the simulations described here assumed the true population size was 2000 lizards. What if it was something different?

<div class="panel panel-primary">
<div class="panel-heading" markdown="1">
## Writing Assignment
</div>
<div class="panel-body" markdown="1">
Write up your calculations and simulations in an Rmarkdown document that describes what you did to determine the best sampling scheme for the lizard capture. Include plots that illustrate your results. You will present these results to a classmate at the next lab period, then the class will decide as a whole what the lizard sampling scheme we will use should be. 
</div>
</div>

## Next
Once we have a sampling scheme, we will try to get the best estimate of the number of lizards in the population *and our uncertainty about that number*.

**[Error and likelihood](capture_recapture3.html)**
