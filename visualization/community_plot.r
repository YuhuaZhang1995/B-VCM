# Generate the community plot

library(reshape2)
library(ggplot2)
library(stringr)

possibleError=tryCatch({
	test=read.table(file="cluster.txt",header=F,sep="\n")
	truth=read.table(file="truth.txt",header=T)
}, error=function(e) e)
if (inherits(possibleError,"error")) next

node_index=unique(c(truth$node1,truth$node2))
node_index=node_index[order(node_index)]
node_index=data.frame(node_index=node_index,index=c(1:length(node_index)))
len_node=dim(test)[1]/K
nodelist=unique(c(truth$node1,truth$node2))
test2=c()
for (k in 1:K){
	tmp=test[((k-1)*len_node+1):(k*len_node),1]
	test2=cbind(test2,tmp)
}
	
# generate the binary allocation matrix by the maximal number of the nodes hit into one of the communities
node_k=list()
for (k in 1:K){
	maxlist=apply(test2,1,max)
	nodelist_1=node_index[which(test2[,k]==maxlist),1]
	node_k[[k]]=nodelist_1
}

truth$inf_cs1=NA
truth$inf_cs2=NA
for (i in 1:dim(truth)[1]){
	for (k in 1:K){
		if (truth[i,1]%in%node_k[[k]]){truth[i,]$inf_cs1=k}
		if (truth[i,2]%in%node_k[[k]]){truth[i,]$inf_cs2=k}
	}
}

count=matrix(0,K,K)
for (k in 1:K){
	tmp=truth[which(truth$inf_cs1==k),]
	for (i in 1:dim(tmp)[1]){
		for (kk in 1:K){
			if ((!is.na(tmp[i,]$inf_cs2))&(tmp[i,]$inf_cs2==kk)) {count[k,kk]=count[k,kk]+1}
		}
	}
}

count2=count/rowSums(count)
countplot=melt(count2)
countplot_ss=melt(count)
#countplot$ss=countplot_ss$value
countplot$ss=round(countplot$value,digits=2)
plotname=paste0("comm.jpeg")
jpeg(plotname)
p1=ggplot(data = countplot, aes(x=as.integer(Var1), y=as.integer(Var2), fill=value)) + 
geom_tile(color = "white")+
scale_fill_gradient2(low = "white", high = "red",limit = c(0,1),name="Inter/Intra\n connection")+
geom_tile()+xlab("K")+ylab("K")+
geom_text(aes(Var2, Var1, label = ss), color = "black", size = 6)+
scale_y_continuous(breaks=c(1,2,3,4,5,6,7,8,9,10))+
scale_x_continuous(breaks=c(1,2,3,4,5,6,7,8,9,10))+
theme(axis.text=element_text(size=20),text = element_text(size=20))+
theme(legend.position="none")
print(p1)
dev.off()
