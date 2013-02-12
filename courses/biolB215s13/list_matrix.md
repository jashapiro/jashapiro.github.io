---
layout: Rmd
title: Matrices, Arrays and Lists
pretitle: Biol B215
parent: index.html
tags: [R, tutorial, RStudio, BiolB215]
---





## Introduction
Up to now, we have been dealing mostly with vectors, simple one dimensional lists of R objects that are all the same type (numbers, booleans, strings). But what if you want to arrange things in more than one dimension, or include objects of more than one type? That is where **matrices**, **arrays** and **lists** come in. Matrices and arrays allow you to have multidimensional arrangements of objects that are all the same type, and lists allow one dimensional (mostly) arrangements of objects of different types. (If you want to have a two dimensional table where each column can be a different type of object (*i.e.* a spreadsheet), then you would probably want to use a **data frame**, wich I cover on [its own page](dataframes.html)

## Matrices
A matrix is a two or more dimensional version of a vector. You construct them by calling `matrix()`, which takes up at least two arguments: a vector of values, the number of rows (`nrow`) and/or the number of columns(`ncol`) of the matrix. If you only give the rows or columns, `R` will guess the other dimension by dividing the length of the vector by the dimension you specified. By default, it will fill the matrix with the vector you give it column by column, but you can tell it to fill by row by adding the argument, `byrow = TRUE`. For example:


{% highlight r %}
my_vector <- c(1, 2, 3, 4, 10, 20, 30, 40)
tall_matrix <- matrix(my_vector, ncol = 2)
tall_matrix
{% endhighlight %}



{% highlight text %}
##      [,1] [,2]
## [1,]    1   10
## [2,]    2   20
## [3,]    3   30
## [4,]    4   40
{% endhighlight %}



{% highlight r %}
wide_matrix <- matrix(my_vector, nrow = 2, byrow = TRUE)
wide_matrix
{% endhighlight %}



{% highlight text %}
##      [,1] [,2] [,3] [,4]
## [1,]    1    2    3    4
## [2,]   10   20   30   40
{% endhighlight %}


You can also name the rows and columns by giving a list of the names in the `dimnames` argument, with the first element being a vector of row names and the second the column names as a list (see below about lists):


{% highlight r %}
my_table <- matrix(c(1, 4, 9 ,36), nrow = 2,
                   dimnames = list( c("a", "b"), c("z", "y") ) )
my_table
{% endhighlight %}



{% highlight text %}
##   z  y
## a 1  9
## b 4 36
{% endhighlight %}


If you want to select a specific element from the matrix, you can do that just like you would with a vector, using square brackets, only this time you have to specify which row(s) and column(s) you want, separated by a comma. If you leave either blank, you will get the whole row/column, as you might have guessed based on the row and column names that you saw when you didn't specify them explicitly. You can refer to the elements either by their index numbers or by the row/column names, if those exist.


{% highlight r %}
tall_matrix[3, 1]
{% endhighlight %}



{% highlight text %}
## [1] 3
{% endhighlight %}



{% highlight r %}
wide_matrix[ , 2:3]
{% endhighlight %}



{% highlight text %}
##      [,1] [,2]
## [1,]    2    3
## [2,]   20   30
{% endhighlight %}



{% highlight r %}
my_table['a', ]
{% endhighlight %}



{% highlight text %}
## z y 
## 1 9
{% endhighlight %}



{% highlight r %}
my_table[1, 2]
{% endhighlight %}



{% highlight text %}
## [1] 9
{% endhighlight %}


See what happens if you try to select from a matrix using only a single number in the brackets, i.e. `my_table[3]`. What is going on? What does the `3` refer to in this case?
{: .question}

One other way of building matrixes is to combine vectors using `rbind()` and `cbind()`, which join vectors into a matrix by rows or by columns, respectively:
 

{% highlight r %}
a <- 1:10
b <- 1:5 
c <- 101:110
cbind(a, c)
{% endhighlight %}



{% highlight text %}
##        a   c
##  [1,]  1 101
##  [2,]  2 102
##  [3,]  3 103
##  [4,]  4 104
##  [5,]  5 105
##  [6,]  6 106
##  [7,]  7 107
##  [8,]  8 108
##  [9,]  9 109
## [10,] 10 110
{% endhighlight %}



{% highlight r %}
rbind(a, b, c)
{% endhighlight %}



{% highlight text %}
##   [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
## a    1    2    3    4    5    6    7    8    9    10
## b    1    2    3    4    5    1    2    3    4     5
## c  101  102  103  104  105  106  107  108  109   110
{% endhighlight %}


Notice how `R` automatically named one of the dimensions, using the names of the vectors that you gave to the bind command. You should also have notice how the vector `b` was recycled automatically to be the same length as the other vectors (or the longest vector, if there were many lengths of vectors).

### Arrays
If you want to store things in more than two dimensions, you can do that as well, using arrays, which are constructed with `array()`. Rather than specifying the the number of rows or columns with `ncol` or `nrow`, you give it a vector of the array dimensions using the `dim` argument.  Otherwise these are mostly analagous to matrices, extended to an arbitrary  number of dimensions. I'm not going to go into detail here, as they don't come up all that often for basic analyses, but feel free to explore on your own...

## Lists
You have already seen lists, as with the list of dimension names in the last section, so just a couple of quick notes here. You can use lists to put together vectors that might be different lengths, or of different types. Unlike with the bind commands, vectors of different length won't be expanded when putting together a list. Lists don't actually have to contain just vectors, but they can contain any `R` object, whether it be a matrix, data frame (coming next) or another list. Yes, you can have lists of lists. Some examples:


{% highlight r %}
a_list <- list(a, b, c("apple", "banana"))
a_list
{% endhighlight %}



{% highlight text %}
## [[1]]
##  [1]  1  2  3  4  5  6  7  8  9 10
## 
## [[2]]
## [1] 1 2 3 4 5
## 
## [[3]]
## [1] "apple"  "banana"
{% endhighlight %}



{% highlight r %}
b_list <- list(a, my_table)
b_list
{% endhighlight %}



{% highlight text %}
## [[1]]
##  [1]  1  2  3  4  5  6  7  8  9 10
## 
## [[2]]
##   z  y
## a 1  9
## b 4 36
{% endhighlight %}



{% highlight r %}
lol <- list(a_list, b_list)
lol
{% endhighlight %}



{% highlight text %}
## [[1]]
## [[1]][[1]]
##  [1]  1  2  3  4  5  6  7  8  9 10
## 
## [[1]][[2]]
## [1] 1 2 3 4 5
## 
## [[1]][[3]]
## [1] "apple"  "banana"
## 
## 
## [[2]]
## [[2]][[1]]
##  [1]  1  2  3  4  5  6  7  8  9 10
## 
## [[2]][[2]]
##   z  y
## a 1  9
## b 4 36
{% endhighlight %}


Notice how each element of the list is indicated by double square brackets. This is just like addressing the elements of a vector, but for lists. If you have a list of lists, you can't use the notation you would for the matrix (with a comma), but rather you specify the outer list with the first brackets, then the list you want inside with a second. You can keep drilling down like this, even into the elements of a vector (though then you are back to using single brackets):


{% highlight r %}
lol[[1]]
{% endhighlight %}



{% highlight text %}
## [[1]]
##  [1]  1  2  3  4  5  6  7  8  9 10
## 
## [[2]]
## [1] 1 2 3 4 5
## 
## [[3]]
## [1] "apple"  "banana"
{% endhighlight %}



{% highlight r %}
lol[[1]][[3]]
{% endhighlight %}



{% highlight text %}
## [1] "apple"  "banana"
{% endhighlight %}



{% highlight r %}
lol[[1]][[3]][2]
{% endhighlight %}



{% highlight text %}
## [1] "banana"
{% endhighlight %}


Lists can also name their elements by specifying the name as if it were an argument name when calling `list()`, and this is how many functions actually return their results. If a list has named elements, you can access them with a `$`, in addition to the double square bracket notation.


{% highlight r %}
food <- list(fruit = c("apple", "banana"),
             veg = c("asparagus", "brussels sprout", "carrot"))
food
{% endhighlight %}



{% highlight text %}
## $fruit
## [1] "apple"  "banana"
## 
## $veg
## [1] "asparagus"       "brussels sprout" "carrot"
{% endhighlight %}



{% highlight r %}
food$fruit
{% endhighlight %}



{% highlight text %}
## [1] "apple"  "banana"
{% endhighlight %}



{% highlight r %}
food[[2]]
{% endhighlight %}



{% highlight text %}
## [1] "asparagus"       "brussels sprout" "carrot"
{% endhighlight %}


As these lists get complicated, you might start to find the `str()` function handy. This takes any variable in your workspace and tells you the structure of the data in it, with a little hint of the contents. For example:

{% highlight r %}
str(lol)
{% endhighlight %}



{% highlight text %}
## List of 2
##  $ :List of 3
##   ..$ : int [1:10] 1 2 3 4 5 6 7 8 9 10
##   ..$ : int [1:5] 1 2 3 4 5
##   ..$ : chr [1:2] "apple" "banana"
##  $ :List of 2
##   ..$ : int [1:10] 1 2 3 4 5 6 7 8 9 10
##   ..$ : num [1:2, 1:2] 1 4 9 36
##   .. ..- attr(*, "dimnames")=List of 2
##   .. .. ..$ : chr [1:2] "a" "b"
##   .. .. ..$ : chr [1:2] "z" "y"
{% endhighlight %}


To translate: the `lol` variable contains a list of two objects. The lines with &#8220;`$`" in the first column then indicate what each of those objects contains. The first object is a list of 3 objects, which repectively contain (indicated by the &#8220;`..$`" lines) a vector of 10 integers, a vector of 5 integers, and a vector of 2 strings/character objects (indicated by `chr`). The second object in the top level list (`lol`) is also a list (with two objects in it), which contains a vector of 10 integers, and a 2x2 matrix of numeric objects (indicated by `num`). That matrix also has an "attribute": the list of named dimensions that was stored in `dimnames`.

Obviously, these kinds of objects can get a bit complicated, so in general it is best to try to keep things as simple as possible. If you find yourself wanting to store lots of complicated data together, you are probably at the point where you want to start using object-oriented programming, which is beyond the scope of this class. But you will run into commands that return complicated lists/objects like this (most of the statistical test commands do). Most of the time you can ignore what is going on under the hood in those cases, but at times you may want to pull out just one part of the test results, in which case being able to figure out how the data is stored can be useful. 



