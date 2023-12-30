library(reshape2)
library(ggplot2)
library(stringr)
library(dplyr)

test=read.table(file="result1.txt",header=F,sep="\n")
truth=read.table(file="data1.txt",header=T)
K=4
node_index=unique(c(truth$node1,truth$node2))
node_index=node_index[order(node_index)]
node_index=data.frame(node_index=node_index,index=c(1:length(node_index)))
len_node=(dim(test)[1]-K)/K
nodelist=unique(c(truth$node1,truth$node2))
test2=c()
for (k in 1:K){
	tmp=test[((k-1)*len_node+1):(k*len_node),1]
	test2=cbind(test2,as.numeric(tmp)/1000)
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

nodeindex=unique(c(truth$node1,truth$node2))
nodeindex=nodeindex[order(nodeindex)]
nodeindex=data.frame(node=nodeindex,index=c(1:length(nodeindex)))
truth=merge(truth,nodeindex,by.x="node1",by.y="node")
truth=merge(truth,nodeindex,by.x="node2",by.y="node")



test_2=read.table(file="result2.txt",header=F,sep="\n")
truth_2=read.table(file="data2.txt",header=T)
K=4
len_node=(dim(test_2)[1]-K)/K
nodelist=unique(c(truth_2$node1,truth_2$node2))
test2=c()
for (k in 1:K){
	tmp=test_2[((k-1)*len_node+1):(k*len_node),1]
	test2=cbind(test2,as.numeric(tmp)/1000)
}
		
Bmat=test_2[(dim(test_2)[1]-K+1):dim(test_2)[1],]
Bmat=unlist(strsplit(as.character(Bmat)," "))	
Bmat=str_replace(Bmat,"\\[","")
Bmat=str_replace(Bmat,"\\[","")
Bmat=str_replace(Bmat,"\\]","")
Bmat=str_replace(Bmat,"\\]","")
Bmat=Bmat[which(Bmat!="")]
Bmat=matrix(as.numeric(Bmat),ncol=4,byrow=TRUE)

nodeindex=unique(c(truth_2$node1,truth_2$node2))
nodeindex=nodeindex[order(nodeindex)]
nodeindex=data.frame(node=nodeindex,index=c(1:length(nodeindex)))
truth_2=merge(truth_2,nodeindex,by.x="node1",by.y="node")
truth_2=merge(truth_2,nodeindex,by.x="node2",by.y="node")

#calculate the observed adj matrix
count=matrix(0,nrow(nodeindex),nrow(nodeindex))
for (i in 1:nrow(truth_2)){
	tmp=truth_2[i,]
	count[tmp$index.x,tmp$index.y]=1
}

#Generate the plot
melted_t1 <- melt(count)
melted_sample=melted_t1
truth1=data.frame(inf_cs=c(truth$inf_cs1,truth$inf_cs2),node=c(truth$node1,truth$node2))
truth1=truth1[!duplicated(truth1$node),]
truth1=merge(nodeindex,truth1,by.x="node",by.y="node")
truth1=truth1[,c("index","inf_cs")]
melted_sample=merge(melted_sample,truth1,by.x="Var1",by.y="index")
melted_sample=merge(melted_sample,truth1,by.x="Var2",by.y="index")
melted_sample_part1 <- melted_sample[sample(which(melted_sample$inf_cs.x==1)),]
nodelist=c(melted_sample_part1$Var1[1:25],melted_sample_part1$Var2[1:25])
melted_sample_part1 <- melted_sample[sample(which(melted_sample$inf_cs.x==2)),]
nodelist=c(nodelist,melted_sample_part1$Var1[1:25],melted_sample_part1$Var2[1:25])
melted_sample_part1 <- melted_sample[sample(which(melted_sample$inf_cs.x==3)),]
nodelist=c(nodelist,melted_sample_part1$Var1[1:25],melted_sample_part1$Var2[1:25])
melted_sample_part1 <- melted_sample[sample(which(melted_sample$inf_cs.x==4)),]
nodelist=c(nodelist,melted_sample_part1$Var1[1:25],melted_sample_part1$Var2[1:25])
melted_sample=melted_t1[which(melted_t1$Var1%in%nodelist&melted_t1$Var2%in%nodelist),]
melted_sample=merge(melted_sample,truth1,by.x="Var1",by.y="index")
melted_sample=merge(melted_sample,truth1,by.x="Var2",by.y="index")
	
melted_sample$Var1=factor(melted_sample$Var1, levels=unique(melted_sample$Var1[order(melted_sample$inf_cs.x)]))
melted_sample$Var2=factor(melted_sample$Var2, levels=unique(melted_sample$Var2[order(melted_sample$inf_cs.y)]))
tmp=melted_sample[!duplicated(melted_sample[,c("Var1","inf_cs.x")]),c("Var1","inf_cs.x")]
tmp=tmp %>% arrange(factor(Var1, levels = levels(melted_sample$Var1)))
tmp2=melted_sample[!duplicated(melted_sample[,c("Var2","inf_cs.y")]),c("Var2","inf_cs.y")]
tmp2=tmp2 %>% arrange(factor(Var2, levels = levels(melted_sample$Var2)))

p1=ggplot(data = melted_sample, aes(x=Var1, y=Var2, fill=value)) + 
geom_tile(color="white")+
scale_fill_gradient(low = "white", high = "red",limits=c(0,1)) +
theme(axis.text.y = element_text(angle = 90))+
theme(legend.position = "none")+
theme(axis.text.x=element_blank())+
theme(axis.text.y=element_blank())+
theme(panel.border = element_rect(colour = "black", fill=NA, size=1))+
xlab("")+ylab("")
jpeg("figure5b.jpeg",width=720,height=720)
print(p1)
dev.off()
