---
layout: Rmd
title: Plotting with R
pretitle: Biol B215
parent: index.html
tags: [R, tutorial, RStudio, BiolB215]
nav: teaching
---



## Introduction
One of the most important parts of data analysis is to visualize your data with plots and charts. To paraphrase Yogi Berra: You can see a lot by looking. `R` has lots of powerful tools for creating plots, and you can customize and polish your plots to easily generate graphics worthy of the best scientific paper. There are a number of libraries for making specialized plots and sets of plots, some of which we will explore later in the semester. But for now we will just work on plotting with the built-in graphics. You will see how to make histograms, bar charts, box plots, and scatter plots, and how to customize those plots.

You make plots the same way you do anything else in `R`: you type a command or a series of commands into the console, telling `R` what data to use and how you want the plot to look. At first, this seems much more cumbersome than selecting your data in something like Excel and clicking a plot button, but it has several advantages. They tend to be more customizable, while having much better defaults than Excel. These plots are made for science, not for splashy corporate graphics (not that there is anything wrong with that). The biggest advantage is that once you have a plot that you are satisfied with, creating a similar plot with different data becomes just a matter of copying and pasting the command, replacing only the parts that refer to the data itself.

## Data
The first thing to do is to generate a bit of data for us to plot. We will do this by using the random number generators built into `R`, and some data sets that come with `R`.

First, let's create some random data. The most common distribution in statistics is the normal distribution, so we'll start by having `R` generate random data from that distribution, using the function `rnorm()`.  By default, it uses a mean value of 0 and standard deviation 1, generating as many samples as you ask for in the first argument, `n`. We'll generate three sets of data: one with 20 samples with the default mean and variance, 50 samples with a mean of 5 (and the default standard deviation of 1), and 1000 samples with with a mean of 100 and a standard deviation of 20. 


{% highlight r %}
small_norm <- rnorm(n = 20)
med_norm <- rnorm(50, mean = 5)
large_norm <- rnorm(1000, mean = 100, sd = 20) 
{% endhighlight %}

The other data set we will use is a set of measurements of irises (the flower). This data set dates back to the early 20th century, and a paper by R.A. Fisher, who originally developed much of the basic statistics that we use now. But he was fundamentally a biologist, and was also responsible for founding the fields of population genetics and quantitative genetics. Much of his work in statistics was developed to deal with biological data. In any case, the data in the iris data set were originally collected by Edgar Anderson, but made famous by one of Fisher's publications. They are measurements of flower sepals and petals, with 50 measurements of each of 3 species. (If you want a bit more information, try `?iris`.) The commands below will load the iris data set into your workspace as a data frame and then show a quick summary of structure of that data frame (names of the columns, type of data in each, and a few values).


{% highlight r %}
data(iris)
str(iris) 
{% endhighlight %}



{% highlight text %}
## 'data.frame':	150 obs. of  5 variables:
##  $ Sepal.Length: num  5.1 4.9 4.7 4.6 5 5.4 4.6 5 4.4 4.9 ...
##  $ Sepal.Width : num  3.5 3 3.2 3.1 3.6 3.9 3.4 3.4 2.9 3.1 ...
##  $ Petal.Length: num  1.4 1.4 1.3 1.5 1.4 1.7 1.4 1.5 1.4 1.5 ...
##  $ Petal.Width : num  0.2 0.2 0.2 0.2 0.2 0.4 0.3 0.2 0.2 0.1 ...
##  $ Species     : Factor w/ 3 levels "setosa","versicolor",..: 1 1 1 1 1 1 1 1 1 1 ...
{% endhighlight %}

Take some time to look at the raw data (type the name of each variable and look at the output). You will see that `Sepal.Length`, `Sepal.Width`,  `Petal.Length`, and `Petal.Width` are all `numeric`,  data, while `Species` is a `factor`.

## `ggplot2`
For these exercises, we will mostly focus on the built-in graphics in `R`, but there are a number of packages which present alternative ways of creating plots, and one of the most common is [ggplot2](http://ggplot2.org), written by Hadley Wickham. If you have not already installed it, you can do so with `install.packages("ggplot2")`. For many of the plot types here I will show you how to construct them with either built-in graphics or ggplot2. Sometimes one is easier, and sometimes the other... but in my opinion, the ggplot2 version almost always looks better.


## Simple plots
The most basic plotting command in `R` is `plot()`. Lets see what happens when we try it with our random data. *Remember that since we are using randomly generated data, your plots will not look exactly like mine.*


{% highlight r %}
plot(small_norm)
{% endhighlight %}

<img src="plots/basic_graphics-small_plot.png" title="plot of chunk small_plot" alt="plot of chunk small_plot" width="360" />
{: .text-center}

So what did that do? Something you almost never want to bother doing: `R` plotted the data values in `small_norm` on the y-axis, with just the position of each value in the vector along the x-axis. Since the order doesn't mean anything, this is probably not the kind of plot we really wanted to produce. But for now, let's stick with it, just to illustrate some of the things you can do to customize plots.

### Labels
If we were just exploring the data in `R`, we might be satisfied with the default label, which `R` takes from the name of the variable. But for any kind of publication (including homework!) you should change the axis labels to inform your readers about what the data represent. We do this with the `xlab` or `ylab` arguments, placing our label in quotes. We can also title the plot using `main`. (Some plots will have a default title. To get rid of it, you can use `main = ""` ).


{% highlight r %}
plot(small_norm, 
     ylab = "My random variable",
     main = "A Bad Plot")
{% endhighlight %}

<img src="plots/basic_graphics-badplot.png" title="plot of chunk badplot" alt="plot of chunk badplot" width="360" />
{: .text-center}

We can also change what is being plotted (points, lines, etc.)using `type`, change the color of the points using `col`, and their shape with `pch` (which stands for "point character") and many other options. For a more extensive list, I recommend looking at the reference card available at: <http://cran.r-project.org/doc/contrib/Short-refcard.pdf>, and in particular the "Graphical parameters"" section. I'll use a few different options through this worksheet; see if you can figure out what is doing what by trying different settings yourself.


{% highlight r %}
plot(small_norm, 
     ylab = "My random variable", 
     type = "l")
{% endhighlight %}

<img src="plots/basic_graphics-unnamed-chunk-1.png" title="plot of chunk unnamed-chunk-1" alt="plot of chunk unnamed-chunk-1" width="360" />
{: .text-center}

`R` has a number of ways to define the color you want, but often the easiest is to just use one of the predefined colors, like `"blue"`, `"red"`, `"green"`, or `"lemonchiffon3"`. Yeah, the color names get strange. For a complete list of the colors, you can use the `colors()` command, or you could look at the following color chart: <http://research.stowers-institute.org/efg/R/Color/Chart/ColorChart.pdf> to see what they all look like. Note that color names have to be given  as strings with quotes around them (unless you store the color names in your own variable).


{% highlight r %}
plot(med_norm, 
     ylab = "Another random variable",
     col = "firebrick", pch = 18)
{% endhighlight %}

<img src="plots/basic_graphics-colored_plot.png" title="plot of chunk colored_plot" alt="plot of chunk colored_plot" width="360" />
{: .text-center}

To see the possible point types (there are 20 of them), you can make a quick plot using a command like the one below. 


{% highlight r %}
plot(1:20, 
     ylab = "pch value", 
     pch = 1:20,
     col = c("red", "blue"),
     cex = 2) 
{% endhighlight %}

<img src="plots/basic_graphics-point_types.png" title="plot of chunk point_types" alt="plot of chunk point_types" width="360" />
{: .text-center}

Notice how I can give the `pch` and `col` arguments vectors, so each point gets a different shape and the colors alternate (because `R` is recycling the vector). You can do the same thing for any other option that affects the appearance of data points, which can be useful for visually separating different subsets of data, or highlighting individual points. 

{: .question}
Create a plot of the `med_norm` vector where all the points greater than or equal to 5 are blue and all the points less than 5 are green. You will need to create a vector of color names to do this; the easiest way is to start with a vector of all one color that the same length as the `med_norm` vector, using the `rep()` function, then replace the values that need to change in the next step.  


## Histograms
Since the previous plots were not particularly useful, lets try to do a bit better. We'll start with a basic histogram, which you already saw in your homework assignment.


{% highlight r %}
hist(med_norm)
{% endhighlight %}

<img src="plots/basic_graphics-basic_hist.png" title="plot of chunk basic_hist" alt="plot of chunk basic_hist" width="360" />
{: .text-center}

We can adjust the number of divisions in the histogram with `breaks`. When making a histogram, this is probably your most important decision. If you have too many or too few breakpoints, your histogram will not be very informative. There are no hard and fast rules; it depends what you are trying to show with the plot, as well as how much data you have. (Note that `R` will not necessarily give the exact number of breakpoints that you ask for, it does some optimization internally. If you want, you can use `breaks` to specify the exact breakpoints with a vector instead of a single number. This can be useful for precise plots, and also for histograms with unequal bin widths.)


{% highlight r %}
hist(small_norm, 
     breaks = 20, 
     col = "blue",
     main = "Too many breakpoints")
{% endhighlight %}

<img src="plots/basic_graphics-hist_breaks1.png" title="plot of chunk hist_breaks" alt="plot of chunk hist_breaks" width="360" />
{: .text-center}


{% highlight r %}
hist(large_norm, 
     breaks = 20, 
     col = "blue",
     main = "Better with more data")
{% endhighlight %}

<img src="plots/basic_graphics-hist_breaks2.png" title="plot of chunk hist_breaks" alt="plot of chunk hist_breaks" width="360" />
{: .text-center}

### `ggplot2` Histograms
The basic plotting function in in `ggplot2` is `qplot()`, which can actually make a large number of different kinds of plots, depending on what options you give it. (Saying this is the *basic* plotting function is a bit misleading as it is actually a layer on top of lower level functions, but it is the easiest one to use, at least at first.) 

To make a histogram, we will first load the `ggplot2` package (you only need to do this once per session) and then call `qplot()` with a single vector of numbers. Unlike `plot()`, `qplot()` will actually do something reasonable here, and make a histogram rather than just a series of points.


{% highlight r %}
library(ggplot2)
{% endhighlight %}



{% highlight text %}
## Loading required package: methods
{% endhighlight %}



{% highlight r %}
qplot(med_norm)
{% endhighlight %}



{% highlight text %}
## stat_bin: binwidth defaulted to range/30. Use 'binwidth = x' to adjust this.
{% endhighlight %}

<img src="plots/basic_graphics-gghist.png" title="plot of chunk gghist" alt="plot of chunk gghist" width="360" />
{: .text-center}

We got a warning because we did not tell `qplot` about the histogram bins we wanted. Rather than specifying `breaks` as we did with `hist()`, we tell `qplot()` the actual size of the bins we want to use by givint it a `binwidth` argument. Other arguments for axis labels and title are the same is in `hist()`, though we have to use `fill` for the bar colors and enclose the name of color we want in `I()`. (That part is a bit strange, but there are some good reasons for it. Ask if you are curious.)


{% highlight r %}
qplot(med_norm,
      binwidth = 0.5,
      main = "YA Histogram",
      xlab = "x",
      fill = I("blue"))
{% endhighlight %}

<img src="plots/basic_graphics-gghist2.png" title="plot of chunk gghist2" alt="plot of chunk gghist2" width="360" />
{: .text-center}

### Facetting with ggplot2
One of the very nice features of `ggplot2` is the ability to work with data frames that contain multiple related data sets, or to split data sets by a particular variable and plot each subset separately, in different colors, or otherwise distinguish the subsets. We can play around with this using the `iris` data set. To start, lets make a histogram of just the sepal widths of the flowers in the data set (notice how we use the `data` argument to specify that our x variable comes from a particular data frame):


{% highlight r %}
qplot(x = Sepal.Width,
      data = iris,
      binwidth = 0.2,
      xlab = "Sepal Width (cm)")
{% endhighlight %}

<img src="plots/basic_graphics-sepalhist.png" title="plot of chunk sepalhist" alt="plot of chunk sepalhist" width="360" />
{: .text-center}

If we specify the fill color as a variable (`Species` in this case), ggplot will  make a kind of staked histograms, with each bar colored by the number of each species in each grouping.


{% highlight r %}
qplot(x = Sepal.Width,
      data = iris,
      binwidth = 0.2,
      fill = Species,
      xlab = "Sepal Width (cm)")
{% endhighlight %}

<img src="plots/basic_graphics-sepalcolor.png" title="plot of chunk sepalcolor" alt="plot of chunk sepalcolor" width="504" />
{: .text-center}

While pretty it can be a bit hard to see what each species histogram would look like on its own. In this case, the *setosa* histogram is easy to interpret, but the ones stacked on top of it are a bit rough. It might be better to separate each set of data onto distinct sets of axes. When we do this, we do want all of our plots to still have the same binwidths and to be nicely aligned. This is called facetting, and can be done with the `facets` argument. To use this, you specify what you want to split the data up by, with vertical splits (rows) first, then a `~` (tilde) followed by horizontal splits (columns). In this case I want to the plots vertically so the data are stacked one on top of the other by Species, but I don't want to split by anything on the other axis, so I just use a period (`.`) to specify no splitting on the other axis. So facetting variable is `Species ~ .` as shown below.



{% highlight r %}
qplot(x = Sepal.Width,
      data = iris,
      binwidth = 0.2,
      facets = Species ~ .,
      xlab = "Sepal Width (cm)")
{% endhighlight %}

<img src="plots/basic_graphics-sepalfacet.png" title="plot of chunk sepalfacet" alt="plot of chunk sepalfacet" width="504" />
{: .text-center}



## Adding to plots
Often you might want to add extra points or lines to a plot, and `R` does allow you do to this in a few different ways. With the base graphics (we'll explore another system later), you can add points, lines, line segments, and rectangles to a plot you have made with commands `points()`, `abline()`, `segments()`, and `rect()`, respectively. For now, we will just use `abline()` to annotate our histogram a bit. Feel free to explore the other commands as well.

To add lines showing the locations of the mean and standard deviations, we can first calculated those, then add them to the plot with `abline()`. The `a` and `b` in `abline()` refer to the equation $y = a + bx$, so you can use it to plot a line at any location with a y-intercept of `a` and a slope of `b`. So if you want a diagonal line that goes through the origin with a slope of 1, you would use the command `abline(a = 0,b = 1)` or simply `abline(0, 1)`. One thing you can't do with that equation is to plot a vertical line, but that can be done by leaving out `a` and `b` and instead giving an x-intercept value or values as the argument `v`, which is what I have done below.


{% highlight r %}
large_mean <- mean(large_norm)
large_sd <- sd(large_norm)
hist(large_norm, 
     breaks = 10)
abline(v = large_mean,
       col = "purple",
       lwd = 2) #lwd controls the line width
abline(v = c(large_mean + large_sd, large_mean - large_sd),
       col = "purple",
       lwd = 2,
       lty = 2) #lty controls the line type, here dashed
{% endhighlight %}

<img src="plots/basic_graphics-annotated_hist.png" title="plot of chunk annotated_hist" alt="plot of chunk annotated_hist" width="360" />
{: .text-center}

For `ggplot2`, you add elements to a plot by literally adding things to the `qplot()` function using a `+` sign. To add a vertical line, you add the `geom_vline()` function and specify the `xintercept` argument. As you will see, `ggplot2` tends to be a bit more verbose than the basic graphics. You have to type out things like `color` and `linetype`, but this can make it a bit easier to see what is really going on.


{% highlight r %}
qplot(large_norm, 
      binwidth = 10,
      xlab = "x") +
  geom_vline(xintercept = large_mean,
             color = "purple") +
  geom_vline(xintercept = c(large_mean + large_sd, large_mean - large_sd),
             color = "purple",
             linetype = 2 )
{% endhighlight %}

<img src="plots/basic_graphics-ggannotated_hist.png" title="plot of chunk ggannotated_hist" alt="plot of chunk ggannotated_hist" width="360" />
{: .text-center}

{: .question}
Create a histogram of the `large_norm` data with about 100 breakpoints. Is this a good number? Play around with different numbers of breakpoints until you find one that you think is a good representation of the data. Then add vertical lines indicating the median and interquartile range of the data. You will want to use the `quantile()` function to find those quantities.

## Box Plots
Another way we can represent a distribution is with a box plot, which we can make using the function `boxplot()`, of all things. For one variable, the call is simple:


{% highlight r %}
boxplot(iris$Petal.Length, ylab = "Petal Length (cm)")
{% endhighlight %}

<img src="plots/basic_graphics-box.png" title="plot of chunk box" alt="plot of chunk box" width="360" />
{: .text-center}

The real utility of box plots though, is to compare distributions in a single plot. To include more than one variable, we need to enclose the variables in a `list`, which is a data structure we have not yet talked about. It is similar to a vector, but can contain elements of different types, including vectors. We could save the list to a variable name of its own, but for now we will just call `list()` within the `boxplot()` function. If To customise the labels for each box, you  use `names`, as in the `barplot()` example.


{% highlight r %}
boxplot(list(iris$Petal.Length, iris$Petal.Width, iris$Sepal.Length, iris$Sepal.Width), 
        names = c("Petal Length", "Petal Width", 
                  "Sepal Length", "Sepal Width"),
        ylab = "centimeters")
{% endhighlight %}

<img src="plots/basic_graphics-boxplot.png" title="plot of chunk boxplot" alt="plot of chunk boxplot" width="504" />
{: .text-center}

Another thing we might want to do is to take the iris data and separate out the different species. To do that with base graphics, we have to introduce R formulas. A formula is a way of representing a relationship you want to explore. Take the classic linear relationship: $y = a + bx$. Since in statistical analysis we generally don't know $a$ and $b$ before we start, the R formula expression just leaves them out, and we would represent the relationship between a response variable `y` and an explanatory variable `x` with the formula `y ~ x`. What that is saying is that `y` may depend on `x`, and that is the relationship I want to explore. In the context of the box plot, I want to see if the distributions are different for different species, so I will use the formula `Petal.Length ~ Species`. This is put in as the first argument. In order to save me from having to type `iris$` a bunch of times to show that I am referring to the `iris` data frame (i.e. `iris$Petal.Length ~ iris$Species`), I can tell the boxplot command that all of my varibles are coming from `iris` with the argument `data = iris` as shown below. 


{% highlight r %}
boxplot(Petal.Length ~ Species, 
        data = iris,
        col = c("orange", "purple", "blue"),
        ylab = "Sepal Length (cm)")
{% endhighlight %}

<img src="plots/basic_graphics-box_formula.png" title="plot of chunk box_formula" alt="plot of chunk box_formula" width="360" />
{: .text-center}

You should be able to see pretty clearly why plotting all of the species together as we did earlier was a bad idea...

### ggplot2 boxplots
`ggplot2` doesn't use the formula notation for boxplots. Instead you just specify the x and y axis as you might have otherwise expected, then use `geom="boxplot"`:


{% highlight r %}
qplot(x = Species,
      y = Petal.Length,
      data = iris,
      geom = "boxplot",
      fill = Species,
      ylab = "Sepal Length (cm)"
      )
{% endhighlight %}

<img src="plots/basic_graphics-ggboxplot.png" title="plot of chunk ggboxplot" alt="plot of chunk ggboxplot" width="432" />
{: .text-center}

{: .question}
Make a boxplot that shows the distribution of the product of petal width and petal length for each individual iris in the data set, split by species. Add a solid horizontal line to your plot that shows the mean of this product across all three the species. Also add a dotted horizontal line that shows the product of mean width and mean length, calculated separately. Are these the same? Why or why not?

## Scatterplots
Finally, lets make some scatterplots. In many ways, these are the easiest to do. Use `plot()`, giving both `x` and `y` values. (Unfortunately, the `data = iris` trick won't work here.)

{% highlight r %}
plot(x = iris$Sepal.Width, y = iris$Sepal.Length)
{% endhighlight %}

<img src="plots/basic_graphics-scatter.png" title="plot of chunk scatter" alt="plot of chunk scatter" width="360" />
{: .text-center}

If you want to add color or shapes to indicate the different species, things get a bit annoying, as we have to assign a color to every single point. Since the data are ordered by species, we can do this quickly with `rep()`, but if they were not, things would get a bit more complicated. If we wanted to do different shapes by species, we would have to make a vector of the shapes as well, which starts to get tedious. We also have to make a legend manually, which I am not even going to try here. 

{% highlight r %}
species_colors <- rep(c("orange", "purple", "blue"), each = 50)
plot(x = iris$Sepal.Width, y = iris$Sepal.Length,
     col = species_colors)
{% endhighlight %}

<img src="plots/basic_graphics-colorscatter.png" title="plot of chunk colorscatter" alt="plot of chunk colorscatter" width="360" />
{: .text-center}

### ggplot2 scatterplots
With `ggplot2`, making these kinds of plots is much simpler, as long as we are willing to let `ggplot2` choose the colors and shapes (it tends to do a good job, but we could override it with another set of commands that we won't worry about now).


{% highlight r %}
qplot(x = Sepal.Width, y = Sepal.Length,
      data = iris,
      color = Species,
      shape = Species)
{% endhighlight %}

<img src="plots/basic_graphics-ggcolorscatter.png" title="plot of chunk ggcolorscatter" alt="plot of chunk ggcolorscatter" width="432" />
{: .text-center}

One little problem with this data that you can see is that there are multiple points that overlap, so you can't see all of the points. This is known as overplotting, and one way to get around it is to add a bit of random error ("jitter") to our data, moving all the points just a little bit from their true position. This is easy to do in `ggplot2` without affecting the original data. (This would be much more annoying to do using basic `R` plotting commands.)

{% highlight r %}
qplot(x = Sepal.Width, y = Sepal.Length,
      data = iris,
      color = Species,
      shape = Species,
      position = "jitter")
{% endhighlight %}

<img src="plots/basic_graphics-ggcolorscatter2.png" title="plot of chunk ggcolorscatter2" alt="plot of chunk ggcolorscatter2" width="432" />
{: .text-center}

<div class="panel panel-primary">
<div class="panel-heading" markdown="1">
## Writing Assignment
</div>
<div class="panel-body" markdown="1">
Using the iris data, or any other multidimensional data set that you might find and want to use, create a plot that illustrates something you find interesting about that data. Your plot should take advantage of at least one feature of plotting in `R` that was not discussed on this page, either from base graphics or `ggplot2`. (Some suggestions: density plots, transparency, varible point sizes, continuous color scales, fit lines, or smoothing curves). You may find the examples available at [ggplot2.org](http://ggplot2.org) to be helpful, especially the example chapter from the [ggplot2 book](http://ggplot2.org/book/): "Getting started with qplot" \[[PDF](http://ggplot2.org/book/qplot.pdf)\].

Your lab assignment for this week is to write a tutorial explaining how to make your plot and what it means. You should start by describing your data set and how to load it into R. Then describe the steps you took to make the plot. You may want start with a simple plot, then show your additions step by step as the plots (and plotting commands) become more complex. Finally, describe the conclusions about your data that you are able to discern from your plot. Assume that the reader has a basic knowledge of R, but has never seen `ggplot2` before. Basically, that they are where you were before today... 
</div>
</div>


### Extra: Bar charts
I don't use a lot of bar charts, for a few reasons, but it does come up at times, so I am throwing the instructions for making a bar plot down here at the bottom. To make a bar chart in R, you can use the function `barplot()`. In the simplest case, you have a vector of numbers and a vector of labels. For example, if I were plotting the number of points scored by each team in the NFL Conference Championships this year, I would have the following vectors:


{% highlight r %}
teams <- c("49ers", "Falcons", "Patriots", "Ravens")
points <- c(28, 24, 13, 28 )
team_colors <- c("gold", "red", "blue", "purple")
{% endhighlight %}

The first argument of `barplot()` is the height of the bar, and `names.arg` (or just `names`) specifies the labels for each bar. Just like before, we can set the color for each bar with `col` and include nice labels for the axes.
 

{% highlight r %}
barplot(points, names = teams, 
        col = team_colors, 
        ylab = "Points Scored", 
        xlab = "Team")
{% endhighlight %}

<img src="plots/basic_graphics-barplot.png" title="plot of chunk barplot" alt="plot of chunk barplot" width="360" />
{: .text-center}
One thing you might have noticed is that the y-axis in this plot does not extend to cover all of the data. `R` has a tendency to do this in its attempts to find "pretty" (their word, not mine) places to put the axis ticks, but you might disagree with its decision about how long a given axis should be. Luckily, you can control this using `xlim` and `ylim`, each of which takes a vector of length 2 with the minimum and maximum values for the axis.


{% highlight r %}
barplot(points, names = teams, 
        col = team_colors, 
        ylim = c(0, 30),
        ylab = "Points Scored", 
        xlab = "Team")
{% endhighlight %}

<img src="plots/basic_graphics-barplot_unpretty.png" title="plot of chunk barplot_unpretty" alt="plot of chunk barplot_unpretty" width="360" />
{: .text-center}

As the data get more complicated, you might want to start grouping bars (for example to put the teams that actually played each other close together, with larger spaces between matchup pairs), but we will leave that for another time. 

### `ggplot2` bar charts
Bar charts can be done in `ggplot2` by adding the argument `geom = "bar"` to a `qplot()` function that has `x` and `y` values. If you want to avoid getting a warning from `ggplot2`, you also have to add an argument of `stat = "identity"`, and you have to wrap the fill colors up in that `I()` function again.  It isn't the prettiest thing in the world, but it does work.


{% highlight r %}
qplot(x = teams, y = points, 
      geom = "bar", 
      stat = "identity", 
      fill = I(team_colors))
{% endhighlight %}

<img src="plots/basic_graphics-ggbarplot.png" title="plot of chunk ggbarplot" alt="plot of chunk ggbarplot" width="360" />
{: .text-center}
If you don't use the `I()` function, `ggplot2` will try to intepret the vector you give to `fill` as a factor, and it will assign its own colors (and generate a legend), which can actually be handy:


{% highlight r %}
league <- c("NFC", "NFC", "AFC", "AFC")
qplot(x = teams, y = points, 
      geom="bar", 
      stat = "identity", 
      fill = league)
{% endhighlight %}

<img src="plots/basic_graphics-ggbarplot2.png" title="plot of chunk ggbarplot2" alt="plot of chunk ggbarplot2" width="432" />
{: .text-center}

