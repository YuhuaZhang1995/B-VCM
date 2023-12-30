library(ggplot2)

file=read.table(file="truth.txt",header=T)
deg=as.data.frame(table(c(file$node1,file$node2)))
deg2=as.data.frame(table(deg$Freq))
deg2$Var1=as.numeric(deg2$Var1)
p1=ggplot(data=deg2,aes(x=log(Var1),y=log(Freq)))+geom_point()+
ylab("Log Transformed Frequency")+xlab("Log Transformed Degree")

jpeg("deg_plot.jpeg")
print(p1)
dev.off()
