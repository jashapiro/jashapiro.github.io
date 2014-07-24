---
layout: Rmd
title: First steps with R
pretitle: Biol B215
parent: index.html
tags: [R, tutorial, RStudio, BiolB215]
nav: teaching
---



Once you have successfully installed `R`, it is time to start using it. As you read through this page, I strongly encourage you to type along in your own R window, and check that you are getting the same results as shown here. But don't stop there. Try new things, play around. You won't break it, and you might learn something.

The first thing to try is using `R` like a calculator. Enter a simple mathematical expression, and `R` will give you the answer. It obeys the standard order of operations, so things should act mostly as you would expect:

```r
2+2
```

```
## [1] 4
```

```r
10*3-4/0.5
```

```
## [1] 22
```

```r
10*(3-4)/0.5
```

```
## [1] -20
```

You can also perform many of the simple mathematical functions you might expect. I'll leave it as an exercise to figure out what each of the following is doing:

```r
2.2^3
```

```
## [1] 10.65
```

```r
sqrt(2)
```

```
## [1] 1.414
```

```r
abs(10-40)
```

```
## [1] 30
```

```r
sin(1) # trig functions use radians, not degrees
```

```
## [1] 0.8415
```
Notice that `R` does not try to evaluate anything on the line after the &#8220;`#`" character. The &#8220;`#`" denotes the start of a "comment", which is very handy for putting notes right in with your code. We will discuss another way of documenting your code later, which will allow you to produce html documents like this one quickly and easily. 

## Variables

You can also store the results of any calculation (or really anything at all) in a variable of your choosing. Then any time you want that value back you can just type the variable name, either by itself or as part of a later calculation. There are two ways to do this: with an equals sign (`=`), which will *assign* the value on the right to the variable name on the left. The other way is with an arrow (`<-`), which will store a value into the variable that it is pointing to. The arrow tends to be more common, mostly for historical reasons (you couldn't use the &#8220;`=`" symbol in early versions of `R`), but you should feel free to use either. 


```r
x <- 3
x
```

```
## [1] 3
```

```r
y = 10^0.5
y
```

```
## [1] 3.162
```

You can assign new values to existing variables, but when you do, whatever old value that was there is lost. 


```r
y <- exp(3) 
# exp() calculates powers of the mathematical constant e
y
```

```
## [1] 20.09
```


One little trick with the arrow, as shown below, is that you can actually make it point either direction, but it usually a good idea to always put the variable on the left and the new value on the right (with a left-pointing arrow). Consistency is good.


```r
x + y -> z # works, but not a great idea
z
```

```
## [1] 23.09
```

```r
z - x
```

```
## [1] 20.09
```


## Vectors
You may have noticed that when `R` returns a value, it prepends it with &#8220;`[1]`". This is because, in it's way of working, `R` is never actually working just one number, but rather it is always working with a string of numbers: a **vector**. It is just that all the vectors we have dealt with so far have length 1. To construct a vector that is longer than length 1, you use the `c()` function:

```r
X <- c(1, 2, 3, 4, 5, 6, 7, 8)
X
```

```
## [1] 1 2 3 4 5 6 7 8
```

Now we can start to explore some of the strange and wonderful things that `R` does that are quite different from most calculators or programming languages. The first is what happens when you perform mathematical functions on a vector. Most of the time, `R` automatically applies the function to each element of the vector, returning a new vector with the results:

```r
X + 10
```

```
## [1] 11 12 13 14 15 16 17 18
```

```r
sqrt(X)
```

```
## [1] 1.000 1.414 1.732 2.000 2.236 2.449 2.646 2.828
```

```r
X^2
```

```
## [1]  1  4  9 16 25 36 49 64
```

```r
X + X^2
```

```
## [1]  2  6 12 20 30 42 56 72
```

```r
X * (X + 1)
```

```
## [1]  2  6 12 20 30 42 56 72
```

Notice how when I told `R` to add or multiply two vectors, it performed the operation element by element. (This might not be what you expected for the multiplication if you were thinking of vectors like you would in linear algebra.) In fact, when I told it to add a single value to the vector, what `R` actually did was to repeat that value to a vector equal in length to the longer one, and then perform the pairwise addition. This means that you can do some fun and often useful things like adding different numbers to each element of the list depending on position. Say you want to make every other element negative. You can just make a vector of length 2: `c(1, -1)` and multiply it by your starting vector. `R` will automatically repeat the shorter vector as many times as necessary to make it the same length as the longer one. This is known as vector "recycling". If it can't do that an integer number of times, it will give you a warning (but it will still perform the operation, usually).


```r
X * c(1, -1)
```

```
## [1]  1 -2  3 -4  5 -6  7 -8
```

```r
X + c(0, 10, 100)
```

```
## Warning: longer object length is not a multiple of shorter object length
```

```
## [1]   1  12 103   4  15 106   7  18
```

Working always with vectors this way may seem odd at first, but it makes a lot of sense for in statistics, when you often have to perform the same mathematical function on a whole lot of data. In other languages you would have to write a loop of some kind, and that is a lot more to type and keep track of. This "vectorization" also allows `R` to perform a certain amount of optimization behind the scenes to speed up these types of calculations quite substantially. 

### The colon operator
There is another way of generating vectors that can be quite handy, so it is worth mentioning. That is the colon operator, `:`. This simply generates a vector of numbers where each is 1 more than the previous starting with the number on the left, ending with the number on the right (or as close as possible without going over, *Price Is Right* rules). Or if the number on the left is larger than the one on the right, it will produce a vector of descending numbers. While you can use this with non-integer starting points, I generally don't recommend it, as you are likely to be get confused about what the exact sequence returned will be.


```r
1:10
```

```
##  [1]  1  2  3  4  5  6  7  8  9 10
```

```r
8:-4
```

```
##  [1]  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4
```

```r
2.3:23
```

```
##  [1]  2.3  3.3  4.3  5.3  6.3  7.3  8.3  9.3 10.3 11.3 12.3 13.3 14.3 15.3
## [15] 16.3 17.3 18.3 19.3 20.3 21.3 22.3
```

One very important note with the colon operator is that it comes first in the order of operations, before addition, multiplication, etc. Forget this at your peril.

```r
x <- 3
1:x
```

```
## [1] 1 2 3
```

```r
1:x+10
```

```
## [1] 11 12 13
```

```r
1:(x+10)
```

```
##  [1]  1  2  3  4  5  6  7  8  9 10 11 12 13
```

```r
1:x/3
```

```
## [1] 0.3333 0.6667 1.0000
```

```r
1:(x/3)
```

```
## [1] 1
```

{: .problem}
Create a vector of the numbers from 1 to 9 and store it in a variable called `digits`. Use `R`'s vector recycling to divide every even number by 2, then multiply every multiple of 3 by 3. (6, being both even and a multiple of 3 should become 9). Store the result in a new variable.


### Selecting from vectors
Sometimes you want only a single element from a vector, or a few elements of the vector. To get that, you can use the square brackets operator, `[]`, with the index positions of the element or elements you want. So if I want the fifth element of a vector I can get it with something like: `X[5]`. You are not limited to choosing only one element, or even to choosing each element only once: simply provide another vector with the element positions you wish to select. 

```r
X[5]
```

```
## [1] 5
```

```r
X[2:4]
```

```
## [1] 2 3 4
```

```r
X[c(1,1,3,7,1,2)]
```

```
## [1] 1 1 3 7 1 2
```
You can also select a subset by choosing the elements you don't want by making those index numbers negative. This will return every element but those:

```r
X[-3]
```

```
## [1] 1 2 4 5 6 7 8
```

```r
X[c(-4,-8)]
```

```
## [1] 1 2 3 5 6 7
```
What you can *not* do is mix positive and negative index numbers. I'm not even sure what that would mean, and `R` will complain.

You may have noticed that `R` counts its index positions starting with `1`. This is different from many programming languages, which start with `0`. If you haven't done much programming before that won't be a big deal, but for people coming from another language it can be pretty confusing. (Note that the previous syntax for excluding elements wouldn't work if you numbered from `0`, as you would not be able to exclude the first element...)

You can also use the vector indexing to replace an element or elements of a vector, even replacing multiple elements at once:

```r
X
```

```
## [1] 1 2 3 4 5 6 7 8
```

```r
X[3] <- 23
X
```

```
## [1]  1  2 23  4  5  6  7  8
```

```r
X[c(2,4,6)] <- 0
X
```

```
## [1]  1  0 23  0  5  0  7  8
```

```r
X[c(1,3,6)] <- c(-10, -20, -30)
X
```

```
## [1] -10   0 -20   0   5 -30   7   8
```

### Functions on vectors
There are a number of functions that require vectors as input, rather than simply being applied to each element in turn. These are things like: `length()`, which tells you how many elements are in the vector; `sum()` and `mean()`, which perform some variant of aggregation; as well as functions like `diff()`,  which returns a vector of the differences between each pair of numbers in the input vector. It is important to keep track of what input a function requires and what its output will be, but most of the time things will work generally as you expect them to.


```r
Y <- c(1, 2, 2, 5, 6, 2, 3, 4, 
       4, 5, 6, 7, 2, 3, 5)
length(Y)
```

```
## [1] 15
```

```r
sum(Y)
```

```
## [1] 57
```

```r
mean(Y)
```

```
## [1] 3.8
```

```r
median(X)
```

```
## [1] 0
```

```r
diff(Y)
```

```
##  [1]  1  0  3  1 -4  1  1  0  1  1  1 -5  1  2
```


## Basic Data Types

### Numeric and Integer
So far, we have dealt almost entirely with numbers, but there are a few different data types in `R` and it is important to understand them. As we have already seen, the first is numbers. Most of the time, you don't need to worry about whether the numbers are floating point numbers (decimal) or integers, as `R` will perform the appropriate conversions. If you want to do the conversion manually, you can use functions such as `round()`, `ceiling()`, and `floor()`, or `as.integer()`, which you will note acts like `floor()` in the way it performs rounding.

```r
a <- 1:10/2
a
```

```
##  [1] 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0
```

```r
round(a)
```

```
##  [1] 0 1 2 2 2 3 4 4 4 5
```

```r
ceiling(a)
```

```
##  [1] 1 1 2 2 3 3 4 4 5 5
```

```r
floor(a)
```

```
##  [1] 0 1 1 2 2 3 3 4 4 5
```

```r
as.integer(a)
```

```
##  [1] 0 1 1 2 2 3 3 4 4 5
```

### Booleans
Even simpler than integers are booleans, which can be only `TRUE` or `FALSE` (note the all caps). These appear often, usually as the result of some kind of test. For example, below, I show tests for all the numbers less than or greater than others, and one way to test for even numbers. This is to use the modulo operator, `%%`, which give you the remainder after division (by 2 in this case), which will be `0` for even numbers. So I then compare the result to `0` using the double equals operator (`==`), which returns `TRUE` if the values on both sides are equal. (Don't confuse it with the single `=` used for variable  assignment.)

```r
b <- FALSE
b
```

```
## [1] FALSE
```

```r
Z <- 1:10
Z < 4 # less than
```

```
##  [1]  TRUE  TRUE  TRUE FALSE FALSE FALSE FALSE FALSE FALSE FALSE
```

```r
Z >= 2 # greater than or equal to
```

```
##  [1] FALSE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE
```

```r
even <- (Z %% 2) == 0 
even
```

```
##  [1] FALSE  TRUE FALSE  TRUE FALSE  TRUE FALSE  TRUE FALSE  TRUE
```

If you have a vector of booleans like this, you can also use that as a way of selecting part of a vector. If you want to know how many elements of a boolean vector are true, the easiest thing is usually just to sum up the vector, which will convert all of the `TRUE` values to 1 and all of the `FALSE` values to 0, then sum them just like any other number).


```r
Z[even]
```

```
## [1]  2  4  6  8 10
```

```r
sum(even)
```

```
## [1] 5
```
There are a few operators that are be used specifically on boolean data. These perform logical operations like "*AND*", "*OR*" and "*NOT*". The "*NOT*" operator is the exclamation point (`!`). It takes any `TRUE` value and turns it `FALSE`, and vice versa. "*AND*", performed by the ampersand (`&`), compares two values (or a pair of vectors, element by element), returning `TRUE` only if both values are `TRUE`, otherwise it is `FALSE`.  "*OR*", performed by the pipe (`|`) returns `TRUE` if either of the two values is `TRUE`, it is `FALSE` only if both are `FALSE`.

```r
odd <- !even
odd
```

```
##  [1]  TRUE FALSE  TRUE FALSE  TRUE FALSE  TRUE FALSE  TRUE FALSE
```

```r
threes <- Z%%3 == 0
odd & threes #elements that are odd AND divisible by 3
```

```
##  [1] FALSE FALSE  TRUE FALSE FALSE FALSE FALSE FALSE  TRUE FALSE
```

```r
even | threes #elements that are even OR divisible by 3
```

```
##  [1] FALSE  TRUE  TRUE  TRUE FALSE  TRUE FALSE  TRUE  TRUE  TRUE
```

{: .problem}
Calculate the sum of the integers from 1 to 1000 with every number divisible by 7 excluded. There are many ways to do this; show at least two methods.



### Characters and strings
If you want to store text (usually referred to as *strings* in programming contexts), `R` does so in a `character()` data type. Enclose the string of text in quotes to distinguish it from variables (single or double quotes will work). Note that these too are stored as vectors. 


```r
name <- 'Jane Doe'
name
```

```
## [1] "Jane Doe"
```

```r
pets <- c("dog", "cat", "fish", "hedgehog")
pets
```

```
## [1] "dog"      "cat"      "fish"     "hedgehog"
```

### Factors
The last data type we will talk about now is the factor. This is a way of storing categorical data efficiently, while keeping the names of the categories as levels. They look something like character data, but they act quite a bit differently at many times. We will talk a lot more about them as we get into dealing with data more extensively. For now, just note how they appear as contrasted with character vectors. Note also that they can be converted to integers easily, which the character vector can't.

```r
colors <- c("blue", "blue", "green", "red", "yellow", 
            "blue", "blue", "blue", "yellow", "yellow")
colors
```

```
##  [1] "blue"   "blue"   "green"  "red"    "yellow" "blue"   "blue"  
##  [8] "blue"   "yellow" "yellow"
```

```r
f_colors <- factor(colors)
f_colors
```

```
##  [1] blue   blue   green  red    yellow blue   blue   blue   yellow yellow
## Levels: blue green red yellow
```

```r
levels(f_colors)
```

```
## [1] "blue"   "green"  "red"    "yellow"
```

```r
as.integer(f_colors)
```

```
##  [1] 1 1 2 3 4 1 1 1 4 4
```

```r
as.integer(colors)
```

```
## Warning: NAs introduced by coercion
```

```
##  [1] NA NA NA NA NA NA NA NA NA NA
```

### Missing Data
When I tried to convert a character vector to an integer, `R` returned the value &#8220;`NA`". This stands for "Not Available", and is the chief way that missing data is stored in `R`. `NA` will always return `NA` in any comparison, as it is usually preferrable to keep missing values missing. You can test specifically for `NA` values using `is.na()`, and some functions that don't work with `NA`s have options to remove them before performing their calculations

```r
x <- c(1, 2, 3, 4, 5, NA)
is.na(x)
```

```
## [1] FALSE FALSE FALSE FALSE FALSE  TRUE
```

```r
mean(x)
```

```
## [1] NA
```

```r
mean(x, na.rm=TRUE) 
```

```
## [1] 3
```

There are a couple of other "missing" data types, for when you divide by `0` and silly things like that: these are &#8220;`Inf`", &#8220;`-Inf`" and &#8220;`NaN`" (not a number). They are *not* the same as `NA`, though they will often behave similarly, or cause other functions to return `NA` or `NaN`. But since they are not `NA`, `is.na()` will return `FALSE`. 

```r
a <- -3:3
10/a
```

```
## [1]  -3.333  -5.000 -10.000     Inf  10.000   5.000   3.333
```

```r
is.na(10/a)
```

```
## [1] FALSE FALSE FALSE FALSE FALSE FALSE FALSE
```

```r
-10/a
```

```
## [1]   3.333   5.000  10.000    -Inf -10.000  -5.000  -3.333
```

```r
sum(-10/a)
```

```
## [1] -Inf
```

```r
sqrt(a)
```

```
## Warning: NaNs produced
```

```
## [1]   NaN   NaN   NaN 0.000 1.000 1.414 1.732
```

```r
mean(sqrt(a))
```

```
## Warning: NaNs produced
```

```
## [1] NaN
```

## A Bit on Functions
I am not going to go into great depth on how functions in R work, but I want to introduce a bit of terminology that will keep coming up. A function in `R` has two basic parts: the function name and its arguments. The name of the function is the first part, followed immediately by parenthesis. Inside the parenthesis are the arguments, separated by commas. For example, in the `rnorm()` function, which generates normally distributed random numbers, the arguments are: `n`, the number of random numbers you want to generate; `mean`, the mean of the normal distribution they are chosen from; and `sd`, the standard deviation of that distribution. So if you wanted 12 random numbers drawn from a normal distribution with mean 3 and standard deviation 5, you would call the function like this:

```r
rnorm(n = 12, mean = 3, sd = 5)
```

```
##  [1] 13.4208  2.5156  7.7434  9.2317 -1.7623  1.3535 -1.1736  0.9838
##  [9]  1.3417 11.4267  1.7634  7.2616
```
You can actually take a shortcut and not give the argument names explicitly, as long as you give them in the order expected:

```r
rnorm(12, 3, 5)
```

```
##  [1]  4.8821  5.5417  9.4314  4.6396  0.9508 -1.4439  8.6898  1.3341
##  [9]  6.7149 -7.1035  1.0822  2.1698
```
Some arguments have default values, which you can see if you look at the help page for the function you are interested in. For `rnorm()` the default `mean` is `0` and the default `sd` is `1`. If we want to use those, we can shorten our call further and leave those off completely:

```r
rnorm(12) # equivalent to rnorm(12, 0, 1)
```

```
##  [1]  0.7259  0.4766  0.4064 -0.3915  0.4961 -0.1355  0.3385  0.1135
##  [9]  1.8779  0.1659  0.2975 -0.7052
```
If you want to leave some arguments as their default but change others, you can skip the ones you don't want to change, but then you **must** name any arguments that are out of order. If I want 5 random numbers with mean 0 but standard deviation of 0.2 (rather than default of 1), I could do the following:

```r
rnorm(5, sd = 0.2)
```

```
## [1] -0.3275 -0.1969  0.1977  0.2353 -0.1618
```

If any of this is confusing for now, don't worry. There was a lot to take in. Everything will become more clear the more you practice. And there will be plenty of chances to practice.

## Next
Now that you know something about the basic data types, we will start to move on to learning about how to read in data, organize it, and create beautiful plots.
