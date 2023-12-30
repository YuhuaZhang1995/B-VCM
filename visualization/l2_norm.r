library(ggplot2)

alp=c(1,2,5,10,20,50)
l2_norm=c()
filename1=paste0("cluster.txt")
filename2=paste0("truth.txt")
file=read.table(file=filename1,header=F,sep="\n")
truth=read.table(file=filename2,header=T)
truth=data.frame(node=c(truth$node1,truth$node2),cs_t=c(truth$c1,truth$c2))
truth_deg=as.data.frame(table(truth$node))
truth=truth[!duplicated(truth$node),]
truth=truth[order(truth$node),]
truth=merge(truth,truth_deg,by.x="node",by.y="Var1")
cs=file[,1]
cs=cs/1000
norms=truth
# Misclassfication regarding greater than 0.5 rule
#cs=ifelse(cs>0.5,1,0)
norms$aver_cs=cs
for  (m in alp){
	deg_cut=m
	norms=norms[which(norms$Freq>=deg_cut),]
	tmp1=0.5-abs(sqrt(sum((norms$aver_cs-norms$cs_t)^2)/length(norms$node))-0.5)
	tmp2=0.5-abs(sqrt(sum((norms$aver_cs-(1-norms$cs_t))^2)/length(norms$node))-0.5)
	tmp=min(tmp1,tmp2)
	l2_norm=rbind(l2_norm,c(m,tmp))
}

l2_norm=as.data.frame(l2_norm)
colnames(l2_norm)=c("cutoff","l2_norm")
p1=ggplot(data=l2_norm,aes(x=log(cutoff),y=l2_norm))+
geom_line()+ylab("L2 norm")+xlab("Log of degree cutoff")+
theme(axis.text=element_text(size=20),text = element_text(size=20))

jpeg("figure2.jpeg")
print(p1)
dev.off()


