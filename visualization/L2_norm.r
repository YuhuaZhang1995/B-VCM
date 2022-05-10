library(stringr)
library(ggplot2)

alp=c(1,2,5,10,20,50)
l2_plot=c()
for (i in alp){
	truth=read.table(file=paste0("../../clustering_v1/data_2500_same_alpha/data_K_2_2500_direct_alpha_05_05_theta_5_5_B_01_09_pi_5_5.",i,".txt"),header=T)
	truth_deg=as.data.frame(table(c(truth$node1,truth$node2)))
	filename=paste0("results_K_2_2500_alpha_05_theta_5_B_01_09.phi.",i,".txt")
	phi=read.table(file=filename,header=F,sep="\n")

	tmp<-unlist(strsplit(as.character(phi[,1]),","))
	tmp=str_replace(tmp,"\\]","")
	tmp=str_replace(tmp,"\\[","")
	tmp=data.frame(matrix(as.numeric(tmp),ncol=2,byrow = T))
	phi=tmp
	phi$c=ifelse(as.numeric(as.character(phi$X1))%%2==0,0,1)
	phi=merge(phi,truth_deg,by.x="X1",by.y="Var1",all.x=TRUE)

	#l2_plot=c()
	for (m in alp){
		tmp=min(sqrt(sum((phi[which(phi$Freq>=m),]$X2-1+phi[which(phi$Freq>=m),]$c)^2)/nrow(phi[which(phi$Freq>=m),])),sqrt(sum((phi[which(phi$Freq>=m),]$X2-phi[which(phi$Freq>=m),]$c)^2)/nrow(phi[which(phi$Freq>=m),])))
		l2_plot=rbind(l2_plot,c(i,m,tmp))
	}
}

l2_norm=as.data.frame(l2_plot)
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
geom_line(data=llk_333)+geom_point(data=llk_333)+geom_ribbon(aes(ymin=lower, ymax=upper), linetype=2, alpha=0.04)+
ylab("L2 norm")+xlab("Log of degree cutoff")+
ylim(c(-0.005,0.35))+
theme(axis.text=element_text(size=20),text = element_text(size=20))


jpeg("Spaghetti_plot_2500_VI.jpeg")
print(p1)
dev.off()

