---
layout: Rmd
title: "Recapture: More Bayes"
pretitle: Biol B215
parent: index.html
tags: [R, tutorial, RStudio, BiolB215]
---

[back to Bayesian Confidence](capture_recapture4.html)




##  Alternative Bayesian priors
The uniform prior is simple, but does not reflect the information that you and the class put into your initial estimates of the number of lizards in the box. Ideally, we would like to incorporate that information, which we can do by adjusting the prior probability distribution that we use. How we do this is a bit subjective, however, and you will have to think about how much weight you want to put on the class guesses. There is no "correct" answer, aside from the fact that the sum of the prior probabilities for each population size you include in the distribution must equal 1.

Use the class guesses of the population size to construct a prior distribution that is not so flat as the one we have used to this point.  
**a.**  What should this prior look at? How could we smooth the class guesses into a distribution? How much uncertainty should we add?  
**b.**  Plot this new prior distribution, and the posterior that it results in. Compare this to the prior and posterior distributions from one of the uniform priors that you used before.  
**c.**  Are you happier with this new distribution? What are the benefits of this "more subjective: prior over the flat prior? What are its disadvantages? Is it really more subjective?  
{: .question}

## One more capture
After your second "capture", you marked the group of lizards you "caught" and returned them to the box. I will now give you one more chance to catch lizards. Working in groups of 3, you will choose 60 more lizards (per group). Record the numbers of lizards of each color, marked and unmarked. 

What is the the best way to integrate this new information into your estimate of the population size?  
**a.**  How many total individuals were marked when you went out to trap the third time? Assume no loss of markings.  
**b.**  Calculate population size estimates and Bayesian credible intervals using the data from the third capture, using a uniform (flat) distribution for your prior probabilities.  
**c.**  Is the uniform distribution an appropriate prior distribution to use for the data from the third trip? What might be a better choice (besides the class estimate)?  
**d.**  Use the alternative prior that you identified in the previous part to calculate a new posterior distribution for population size using the data from the third trip. Calculate an estimate of the population size and credible intervals based on this posterior distribution. How does this estimate compare to your previous calculations?   
**e.**  Plot the three posterior distributions (the two from part **b** and the one from part **d**) in a single chart. Which one provides the best information about the size of lizard population?    
{: .question}

## Further thoughts
The following additional questions are things that you might want to include in your final report. These are not required, but definitely worth at least thinking about, whether or not you include them in your final report. 

* How would you incorporate all groups' data from their third capture into your estimate of the population size? 
  * Should you just pool all group counts as one large capture? Why or why not?
  * If not, how should that data be incorporated?
  
* How can you incorporate the color data from all rounds to make a better estimate of the proportion of each color lizard in the box? 
  * Can you average any estimates you might have gotten from individual captures? Are the colors in each capture independent? (Were the number of marked individuals independent across captures?) 
  * A somewhat easier version of this question may be to estimate the proportion of a single color; then you can use what you already know about the binomial distribution to inform your  intuition and calculations.

