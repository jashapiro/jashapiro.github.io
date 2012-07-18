#haplotype plots

library(ggplot2)
library(plyr)
library(rjson)

load("set120_60_reduced_segments.RData")

chromosome <- factor(set120_60_reduced_segments$membership[, "chrom_key"], levels=1:6, 
                     ordered = T, labels = c("I", "II", "III", "IV", "V","X"))
start <- set120_60_reduced_segments$membership[, "starts"]
stop <- set120_60_reduced_segments$membership[, "stops"]
strains <- colnames(set120_60_reduced_segments$membership)[4:100]
strains[strains == "PX174"] <- "RC301"

haplotypes <- data.frame(chromosome, start, stop)

haps_all <- matrix(as.character(set120_60_reduced_segments$membership[, 4:100]), ncol=97)
colnames(haps_all) <- strains


haps_noSingle <- t(apply(haps_all, 1, function(hrow){hrow[table(hrow)[hrow] == 1 ] <- NA; return(hrow)}))
colnames(haps_noSingle) <- strains
      
haps <- haps_noSingle
## rename haplotypes for some consistency

# rank by similarity to LSJ1
# similarity <- sort(colSums((haps== haps[, "LSJ1"])), dec = T)
# sorted_strains <- names(similarity)

#rank by total haplotype sharing
similarity <- laply(strains, function(S){sum( (haplotypes$stop - haplotypes$start) * (haps == haps[,S]), na.rm = T )})
sorted_strains <- strains[order(similarity, decreasing = T)]

# replace numbers with strain names 
for (strain in sorted_strains){
  haps[haps == haps[,strain] & !(haps %in% sorted_strains)] <- strain
}

strain_alpha = .9 + (1:97 %% 2) * .1

haplotypes <- cbind(haplotypes, haps)

colorscheme = hsv(h = 0:96/97 * .85, v = c(.8,1,1), s = c(1,1, .6))


# Melt for plotting with ggplot
haplotype_melt <- melt(haplotypes, 
                   id.vars=c("chromosome", "start", "stop"),
                   variable_name = "haplotype" )
haplotype_melt$value <- factor(haplotype_melt$value, levels = sorted_strains, ordered = T)

haplotype_objects <- dlply(haplotype_melt, .(chromosome, start, stop, value), .fun=function(D){
                        if (! is.na(D$value[1])){
                         sprintf("{\"chr\":\"%s\", \"coords\":[%i,%i], \"base_strain\":\"%s\", \"strains\":[%s]}",
                         c(as.character(D$chromosome[1])), D$start[1], D$stop[1], as.character(D$value[1]),
                         paste0("\"", D$variable, "\"", collapse=", "))
                         }else {NA}})

haplotype_json <- paste0(haplotype_objects[!is.na(haplotype_objects)], collapse=",\n")
cat(file="haplotypes.json", "{\"haplotypes\": [\n", haplotype_json, "\n]}\n")
