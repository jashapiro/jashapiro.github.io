---
layout: Rmd
title: knitr markdown test
---

# Knitr and markdown tests

This is a minimal example of using **knitr** with in HTML pages. I am actually
using markdown here since it is more convenient in GitHub.

First, the input file was named as `knitr-minimal.Rmd`
([source](https://github.com/yihui/knitr/blob/master/inst/examples/knitr-minimal.Rmd)),
and **knitr** will automatically determine the output filename to be
`knitr-minimal.md` (`*.Rmd --> *.md`).

I used the code below to make sure **knitr** writes correct URL's for my images.



{% highlight r %}
opts_knit$set(base.dir="..", base.url="/")
render_jekyll()
hook_plot_md_side <- function(x, options){
  if (!is.null(options$fig.sidebar)) {
    paste(sub("\\s+$", "", hook_plot_md(x, options)),
          "{: .sidefig}\n",
          sep = ""
          )
  }else{
    hook_plot_md(x, options)
  }
}
knit_hooks$set(plot = hook_plot_md_side)
{% endhighlight %}




Now we write some code chunks in this markdown file:



{% highlight r %}
## a simple calculator
1+1
{% endhighlight %}



{% highlight text %}
## [1] 2
{% endhighlight %}



{% highlight r %}
## boring random numbers
set.seed(123)
rnorm(5)
{% endhighlight %}



{% highlight text %}
## [1] -0.56048 -0.23018  1.55871  0.07051  0.12929
{% endhighlight %}




We can also produce plots:



{% highlight r %}
library(ggplot2)
{% endhighlight %}



{% highlight text %}
## Warning message: package 'ggplot2' was built under R version 2.14.2
{% endhighlight %}



{% highlight r %}
qplot(hp, mpg, data=mtcars)+geom_smooth()
{% endhighlight %}
![plot of chunk md-cars-scatter](/images/Rplot-md-cars-scatter.png){: .sidefig}



So no more hesitation on using GitHub and **knitr**! You just write a minimal
amount of code to get beautiful output on the web.
