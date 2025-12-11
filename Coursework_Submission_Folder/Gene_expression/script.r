#Install, then call libraries is needed
#install.packages("dplyr")
#install.packages("ggplot2")
library(dplyr)
library(ggplot2)


#Read in the 2 output tsv files as dataframes.
A_vs_B <- read.table(file="GIT/LIFE4138_2526_Coursework/Coursework/GeneExpression/Datasets/set_4/A_vs_B.deseq2.results.tsv",sep="\t",header=TRUE)
A_vs_F <- read.table(file="GIT/LIFE4138_2526_Coursework/Coursework/GeneExpression/Datasets/set_4/A_vs_F.deseq2.results.tsv",sep="\t",header=TRUE)


#Remove any rows that contain NA values.
A_vs_B <- A_vs_B[complete.cases(A_vs_B), ]
A_vs_F <- A_vs_F[complete.cases(A_vs_F), ]


#Created filtered data frames, dividing the data first by whether the differences are significant, then by whether the genes identified are up or down regulated. 
A_vs_B_Sig <- A_vs_B %>% filter(padj<0.05)
A_vs_F_Sig <- A_vs_F %>% filter(padj<0.05)
A_vs_BUp <- A_vs_B_Sig %>% filter(log2FoldChange>0)
A_vs_BDown <- A_vs_B_Sig %>% filter(log2FoldChange<0)
A_vs_FUp <- A_vs_F_Sig %>% filter(log2FoldChange>0)
A_vs_FDown <- A_vs_F_Sig %>% filter(log2FoldChange<0)


#Print out a summary of the dataset, including total number of genes differentially expressed in the datasets, and how many of these are up and downregulated.
print(paste0("There are ",nrow(A_vs_B_Sig)," genes with significantly different expression (p < 0.05) in the A VS B dataset. There are ",nrow(A_vs_F_Sig)," genes with significantly different expression in the A VS F dataset. In the A vs B dataset ",nrow(A_vs_BUp)," of these genes are upregulated, whilst ",nrow(A_vs_BDown)," are downregulated. In the A vs F dataset ",nrow(A_vs_FUp)," of these genes are upregulated, whilst ",nrow(A_vs_FDown)," are downregulated."))


#generate volcano plots from each of the datasets, based on the log fold differences in expression
A_vs_Bvol <- ggplot(data=A_vs_B, aes(x=log2FoldChange, y=-log10(padj))) + geom_point() + labs(x="Log2 Fold Change",y="-Log10 adjusted P value",title="Volcano plot showing both the adjusted p value and log2 change in expression for the A vs B dataset") +
theme(plot.title = element_text(hjust = 0.5)) 
A_vs_Fvol <- ggplot(data=A_vs_F, aes(x=log2FoldChange, y=-log10(padj))) + geom_point() + labs(x="Log2 Fold Change",y="-Log10 adjusted P value",title="Volcano plot showing both the adjusted p value and log2 change in expression for the A vs F dataset") +
theme(plot.title = element_text(hjust = 0.5)) 


#Commands to print out both volcano plots if needed.
plot(A_vs_Bvol)
plot(A_vs_Fvol)
View(A_vs_B)
View(A_vs_F)


#Assign whether each value is significant based on adjusted p values, then plot log2 of the base mean against the log2 fold change.
A_vs_B$threshold <- as.factor(A_vs_B$padj < 0.05)
A_vs_F$threshold <- as.factor(A_vs_F$padj < 0.05)
A_vs_BMAplot <- ggplot(data=A_vs_B,aes(x=log2(baseMean), y=log2FoldChange, colour=threshold)) + geom_point() + labs(x="Log2 Base Mean",y="Log2 Fold Change",title="MA plot showing both log2 base mean and log2 fold change within the A vs B dataset. Coloured based on significance (p < 0.05).") +
theme(plot.title = element_text(hjust = 0.5)) 
A_vs_FMAplot <- ggplot(data=A_vs_F,aes(x=log2(baseMean), y=log2FoldChange, colour=threshold)) + geom_point() + labs(x="Log2 Base Mean",y="Log2 Fold Change",title="MA plot showing both log2 base mean and log2 fold change within the A vs F dataset. Coloured based on significance (p < 0.05).") + 
theme(plot.title = element_text(hjust = 0.5)) 
plot(A_vs_BMAplot)
plot(A_vs_FMAplot)


#Plot histograms for both datasets, demonstrating the distribution of adjusted p values. Number of bins set to 50.
A_vs_Bhist <- ggplot(A_vs_B,aes(x=padj)) + geom_histogram(binwidth=.02) + labs(x="Adjusted p value",y="Frequency",title="Histogram showing frequency of adjusted p values from the A vs B dataset") +
theme(plot.title = element_text(hjust = 0.5)) 
A_vs_Fhist <- ggplot(A_vs_F,aes(x=padj)) + geom_histogram(binwidth=.02) + labs(x="Adjusted p value",y="Frequency",title="Histogram showing frequency of adjusted p values from the A vs F dataset") +
theme(plot.title = element_text(hjust = 0.5)) 
plot(A_vs_Bhist)
plot(A_vs_Fhist)


#Combine the two primary datasets together, including an identifier of their original dataset.
Combdf <- bind_rows(A_vs_B=A_vs_B, A_vs_F=A_vs_F,.id="dataset") 
View(Combdf)


#Heatmap to show all p values for genes between the two data sets.
Combdf %>% ggplot(aes(x= dataset, y = gene_id, fill=padj)) + geom_tile() + labs(x="Dataset",y="Gene",title="Heatmap, showing comparison between the two datasets. Tiles coloured based on adjusted p values") +
theme(plot.title = element_text(hjust = 0.5)) 
Combdf %>% ggplot(aes(x= dataset, y = gene_id, fill=log2FoldChange)) + geom_tile() + labs(x="Dataset",y="Gene",title="Heatmap, showing comparison between the two datasets. Tiles coloured based on log2 Fold change") +
theme(plot.title = element_text(hjust = 0.5)) 


#Combine the previous significant gene data frames, 
Combsigdf <- bind_rows(A_vs_B_Sig=A_vs_B_Sig, A_vs_F_Sig=A_vs_F_Sig,.id="dataset")
View(Combsigdf)
Combsigdf %>% ggplot(aes(x= dataset, y = gene_id, fill=padj)) + geom_tile()  + geom_tile() + labs(x="Datasets",y="Gene",title="Heatmap, showing comparison between the significantly different genes from the two datasets. Tiles coloured based on adjusted p values") +
theme(plot.title = element_text(hjust = 0.5)) 
Combsigdf %>% ggplot(aes(x= dataset, y = gene_id, fill=log2FoldChange)) + geom_tile()  + geom_tile() + labs(x="Datasets",y="Gene",title="Heatmap, showing comparison between the significantly different genes from the two datasets. Tiles coloured based on log2 Fold change") +
theme(plot.title = element_text(hjust = 0.5)) 

#Create a heatmap from the combined significant data frames, only utilizing the first 50 gene ids.
Combsigdfhead <- Combsigdf[order(apply(Combdf, 1, max))[1:50],]
Combsigdfhead <- Combsigdfhead[complete.cases(Combsigdfhead), ]
View(Combsigdfhead)
Combsigdfhead %>% ggplot(aes(x= dataset, y = gene_id, fill=padj)) + geom_tile()  + geom_tile() + labs(x="Datasets",y="Gene",title="Heatmap, showing comparison between the two datasets. Tiles coloured based on adjusted p values") +
theme(plot.title = element_text(hjust = 0.5)) 
Combsigdfhead %>% ggplot(aes(x= dataset, y = gene_id, fill=log2FoldChange)) + geom_tile()  + geom_tile() + labs(x="Datasets",y="Gene",title="Heatmap, showing comparison between the two datasets. Tiles coloured based on log2 Fold change") +
theme(plot.title = element_text(hjust = 0.5)) 


#Print a table of genes which demonstrate most significantly different expression from baseline
A_vs_B_Most_Sig <- A_vs_B %>% filter(padj<0.001)
A_vs_B_Most_Sig_Fin <- data.frame(A_vs_B_Most_Sig$gene_id, A_vs_B_Most_Sig$log2FoldChange,A_vs_B_Most_Sig$pvalue,A_vs_B_Most_Sig$padj)
A_vs_F_Most_Sig <- A_vs_F %>% filter(padj<0.001)
A_vs_F_Most_Sig_Fin <- data.frame(A_vs_F_Most_Sig$gene_id, A_vs_F_Most_Sig$log2FoldChange,A_vs_F_Most_Sig$pvalue,A_vs_F_Most_Sig$padj)
View(A_vs_B_Most_Sig_Fin)
View(A_vs_F_Most_Sig_Fin)

#Export these data frames as .csv files
write.csv(A_vs_B_Most_Sig_Fin,"~/GIT/LIFE4138_2526_Coursework/Coursework_Submission_Folder/Gene_expression/AvsB_Most_Sig_Genes.csv",row.names=FALSE)
write.csv(A_vs_F_Most_Sig_Fin,"~/GIT/LIFE4138_2526_Coursework/Coursework_Submission_Folder/Gene_expression/AvsF_Most_Sig_Genes.csv",row.names=FALSE)