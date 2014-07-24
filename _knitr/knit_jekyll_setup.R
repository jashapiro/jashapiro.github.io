require(knitr)

hook_plot_md_align <- function(x, options){
  if (options$fig.show == 'asis' ||
      options$fig.num == 1L || 
      options$fig.cur == options$fig.num){
    ## alignment class at end of list of figures: will apply to their paragraph
    if(options$fig.align %in% c('center', 'left', 'right', 'wide', 'sidebar')){
      if (options$fig.align %in% c('left', 'right')){
        div_class <- paste("{: .pull-", options$fig.align, "}", sep="")
      } else{
        div_class <- paste("{: .", options$fig.align, "}", sep="")
      }
      
      paste(sub("\\s+$", "", hook_plot_md(x, options)),
            "\n", div_class, "\n", 
            sep = ""
      )
    } else {
      hook_plot_md(x, options)
    }
  } else {
    hook_plot_md(x, options)
  }
}
knit_hooks$set(plot = hook_plot_md_align)