
file_list = dir("./",pattern = "dat$")

data = NULL
for (f in file_list) {
 assign(f,read.table(f,header=TRUE))
 data <- c(data,read.table(f,header=TRUE))
}

par(mfcol=c(3,2))
k = length(data)/5
for (i in seq(1,length(data),by=2)) {
 x <- data[i]$sigma
 y <- data[i+1]$err_rms
 if (i <= k) {
  par(mfg=c(1, 1, 3, 2))
 }
 else if (i < 2*k) {
 par(mfg=c(1, 2, 3, 2))
 }
 else if (i < 3*k){
  par(mfg=c(2, 1, 3, 2))
 }
 else if (i <  4*k)
 { 
  par(mfg=c(2, 2, 3, 2))
 }
 else if (i <  5*k)
 {
  par(mfg=c(3, 1, 3, 2))
 }
 else par(mfg=c(3, 2, 3, 2))
 par(ylim = c(min(y),max(y)))
 plot(x,y,log="xy",xlab="sigma",ylab="K",col=i)
par(new=TRUE)
}
rm(i,f,x,y)