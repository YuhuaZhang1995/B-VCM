
### B-VCM ###
K=4
file1=read.table(file="HL1.txt",header=F,sep="\n")
file2=read.table(file="HL2.txt",header=F,sep="\n")

truth1=read.table(file="data1.txt",header=T)
nodelist1=sort(unique(c(truth1$node1,truth1$node2)))
truth2=read.table(file="data2.txt",header=T)
nodelist2=sort(unique(c(truth2$node1,truth2$node2)))
	
cs1=c()
cs2=c()
for (k in 1:K){
	length1=nrow(file1)/K
	cs1=cbind(cs1,file1[((k-1)*length1+1):(k*length1),1]/1000)
	length2=nrow(file2)/K
	cs2=cbind(cs2,file2[((k-1)*length2+1):(k*length2),1]/1000)
}
cs1=as.data.frame(cs1)
cs2=as.data.frame(cs2)
	
index=length(intersect(nodelist1,nodelist2))
	
tmp_HD=c()
for (i in c(1:100)){
	tmp=0
	tmp1=cs1[,sample(ncol(cs1))]
	tmp2=cs2[,sample(ncol(cs2))]
	tmp1$nodelist=nodelist1
	tmp2$nodelist=nodelist2
	tmp1=tmp1[which(tmp1$nodelist%in%tmp2$nodelist),]
	tmp2=tmp2[which(tmp2$nodelist%in%tmp1$nodelist),]

	#Hellinger distance
	tmp=0
	for (k in 1:index){
		tmp_K=0
		for (j in c(1:K)){
			tmp_K=tmp_K+(sqrt(tmp1[k,j])-sqrt(tmp2[k,j]))**2
		}
		tmp=tmp+sqrt(tmp_K)/sqrt(2)
	}
	tmp_HD=c(tmp_HD,tmp/index)
}

min(tmp_HD)


