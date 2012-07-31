---
layout: default
title: research
permalink: /research/index.html
---

# Research

My research focuses on the relationship between genetic variation and the path of evolution. Natural selection requires  genetic variation to act upon, but the action of selection removes that variation from the population. My work explores the interplay between these forces, using genomic data from many individuals and multiple populations in order to create an unbiased picture of genetic variation across a species.

Much of my work has involved studying natural populations of organisms that have been long been used as laboratory models: the 'fruit' fly *Drosophila melanogaster*, the nematode *Caenorhabditis elegans*, and the budding yeast *Saccharomyces cerevisiae*. Most laboratory studies in these organisms are performed using the progeny of a small number of strains (often only one). While this approach has led to many great advances in biology, understanding the variation present in the species allows us to put laboratory findings in context. At the same time, the variation  present in natural populations can be very different from the mutations that are commonly induced in the lab, making natural varaints a rich source of information that we can use to make new discoveries.


## Global selective sweeps in *C. elegans*

*Caenorhabditis elegans* is a globally distributed species of nematode that lives in decaying plant material and soil. It has been used as a model for developmental biology and genetics for over 50 years, with work on the species resulting in three Nobel prizes. Almost all of this work was done using a single strain, but there has long been interest in the natural variation and population genetics of the species.

*C. elegans* was known to have fairly low genetic diversity (a level similar to humans), and it was widely suspected that this low diversity was largely the result of the fact that *C. elegans* is a selfing hermaphrodite (with rare males), a life history that tends to result in greater power for purifying selection. Even mutations with very small negative effects will tend to be eliminated fairly quickly by natural selection, taking with them neutral variation, in a process called [background selection](http://www.ncbi.nlm.nih.gov/pubmed/8375663?dopt=Abstract "Charlesworth et al. The effect of deleterious mutations on neutral molecular variation.").

<figure class="align-pullright">
<img src="/images/two_chroms.png" alt="elegans haplotypes" title="Haplotype blocks on C. elegans Chromosomes III and V" width="400px" height="240px" />
<figcaption>Haplotypes in a global sample of <em>C. elegans</em>. Each row represents an individual and the colored bars indicated regions of the chromosome that are nearly identical across multiple individuals. On the left, chromosome III shows the expected pattern without positive selection, with many different haplotypes tend to be shared among a few individuals each. By contrast, chromosome V, on the right, shows evidence for a very recent strong selective sweep, which has spread the large red haplotype across almost all sampled strains. </figcaption>
</figure>

Together with [Erik Andersen](http://www.princeton.edu/~eca "Erik Andersen's Homepage") and Justin Gerke, I undertook a large-scale study of the global and genomic diversity of *C. elegans*, using high-throughput sequencing of restriction site associated DNA [(RADseq)](http://dx.doi.org/10.1371/journal.pone.0003376 "Baird et al. 2008") to examine over 200 wild isolates. We began by confirming the general patterns of diversity that had previously been observed using smaller data sets, but our data allowed us to see patterns that had never been appreciated before. Not only was overall diversity low, but on three of the six *C. elegans* chromosomes, large regions were completely identical across strains collected from all over the globe. These long blocks of identity are compelling evidence for positive selection. Simulations indicated that the global spread of these haplotypes occurred only in the past few hundred years.

This strong selection and rapid spread indicates that some allele (or combination of alleles) in each of these haplotypes was strongly favored in the recent past. Unfortunately, the size of the haplotypes and their high frequency in the population mean that the current data do not help us much in identifying the genes which were under selection. Complete genomic sequences for the strains will help, as will data from more strains, as the global collection of *C. elegans* continues to expand. These data, especially from strains that do not contain the common haplotypes, will also allow me to explore whether the recent sweeps are unusual within the history of *C. elegans*, potentially driven by human interactions, or if such sweeps have much more common through the history of the species than we had anticipated. 

If you are interested in exploring this in more detail, you could do worse than to read the paper we published in *Nature Genetics* on the topic: [Chromosome-scale selective sweeps shape *Caenorhabditis elegans* genomic diversity](http://dx.doi.org/10.1038/ng.1050). (You can now get a free version of the article [at PubMedCentral](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3365839)). There was also a nice [News and Views article](http://www.nature.com/ng/journal/v44/n3/full/ng.2201.html) by [Patrick Philips](http://pages.uoregon.edu/pphil/index.html) published alongside the original article (not free).

## Functional variation in *S. cerevisiae*

Another focus of my post-doctoral research has been to identify and characterize the natural patterns of functional variation in the brewers yeast *Saccharomyces cerevisiae*.  Working with Joseph Schacherer, I used an unbiased SNP discovery platform developed in our lab to examined variation in strains of yeast collected from around the world in different environments, both natural and industrial. We generated one of the most comprehensive sets of data on genomic diversity of *S. cerevisiae* strains polymorphism available.  

<figure class="align-pullleft">
<img src="/images/yeast_tree.png" alt="cerevisiae tree" title="Tree of S. cerevisiae strains" width="400px" height="291px" />
<figcaption>
A neighbor-joining tree illustrating the relationships among a global sample of <em>S. cerevisiae</em> strains, determined by genome-wide array-based genotyping. There is little geographic structure among the strains, but they are strongly clustered by environment, particularly strains derived from wineries, sake production and laboratory research. </figcaption>
</figure>

These data clearly demonstrated strong population structure in *S. cerevisiae*, most likely largely driven by strong selection of domestication for winemaking, sake production, and laboratory work. These

Through a genome-wide association study (GWAS), I identified sets of polymorphisms that are responsible for changes in global gene expression among these strains. Population genetic analysis of these polymorphisms shows that changes in trans-acting factors tend to be deleterious, especially when they affect the expression of many other genes. By contrast, cis-regulatory variants are more likely to be neutral or adaptive. 