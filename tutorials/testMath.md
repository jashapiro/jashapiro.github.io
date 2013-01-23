---
layout: Rmd
title: Math tests
tags: [R, tutorial, RStudio]
---




This is an R Markdown document. Markdown is a simple formatting syntax for authoring web pages (click the **MD** toolbar button for help on Markdown).

When you click the **Knit HTML** button a web page will be generated that includes both content as well as the output of any embedded R code chunks within the document. You can embed an R code chunk like this:


{% highlight r %}
summary(cars)
{% endhighlight %}



{% highlight text %}
##      speed           dist    
##  Min.   : 4.0   Min.   :  2  
##  1st Qu.:12.0   1st Qu.: 26  
##  Median :15.0   Median : 36  
##  Mean   :15.4   Mean   : 43  
##  3rd Qu.:19.0   3rd Qu.: 56  
##  Max.   :25.0   Max.   :120
{% endhighlight %}


You can also embed plots, for example:


{% highlight r %}
plot(cars)
{% endhighlight %}

![plot of chunk unnamed-chunk-2](plots/test_math-unnamed-chunk-2.png)
{: .align-right}

Embedding math should work now, either on its own:
$$\sum_i^{10}{i}$$

Or inline with text like this: $\frac{10}{x}$. One thing I am curious about is if I can do superscripts like this 10^3 or not.
