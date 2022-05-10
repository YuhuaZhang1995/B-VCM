library(stringr)
library(ggplot2)
B_mat=c("01_09")
alpha=c("05_05")
alp=c(1,2,5,10,20,50,100)

l2_norm=c()
for (k in alpha){
	for (j in B_mat){
		for (i in c(1:20)){
			filename1=paste0("K_2_10000_alpha_",k,"_theta_5_5_B_",j,".",i,".cs.txt")
			filename2=paste0("../data_10000_same_alpha/data_K_2_10000_direct_alpha_",k,"_theta_5_5_B_",j,"_pi_5_5.",i,".txt")
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
				l2_norm=rbind(l2_norm,c(i,m,tmp))
			}
		}
	}
}

l2_norm=as.data.frame(l2_norm)
colnames(l2_norm)=c("batch","cutoff","l2_norm")
l2_norm$upper=NA
l2_norm$lower=NA
llk_333=c()
for (j in alp){
	tmp=mean(l2_norm[which(l2_norm$cutoff==j),]$l2_norm)
	tmp2=sd(l2_norm[which(l2_norm$cutoff==j),]$l2_norm)
	llk_333=rbind(llk_333,c(21,j,tmp,tmp+tmp2,tmp-tmp2))
	l2_norm[which(l2_norm$cutoff==j),]$upper=tmp+tmp2
	l2_norm[which(l2_norm$cutoff==j),]$lower=tmp-tmp2
}
llk_333=as.data.frame(llk_333)
colnames(llk_333)=c("batch","cutoff","l2_norm","upper","lower")
p1=ggplot(data=l2_norm,aes(x=log(cutoff),y=l2_norm,group=batch))+
geom_line(color="grey")+
#ggtitle(expression(paste("10,000 interactions, ",alpha[1],"=",alpha[2],"=0.5", "a=0.9")))+
geom_line(data=llk_333)+geom_point(data=llk_333)+geom_ribbon(aes(ymin=lower, ymax=upper), linetype=2, alpha=0.04)+
ylab("L2 norm")+xlab("Log of degree cutoff")+ylim(c(-0.005,0.125))+
theme(axis.text=element_text(size=20),text = element_text(size=20))


jpeg("Spaghetti_plot_10000_same_alpha.jpeg")
print(p1)
dev.off()

