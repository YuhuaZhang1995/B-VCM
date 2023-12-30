library(ggplot2)
filename=paste0("llk.txt")
file=read.table(file=filename,header=F)
file=file[1001:2000,1]
print(mean(file))

