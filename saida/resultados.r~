file_list = dir("./",pattern = "dat$")
err_rms = NULL
mean = NULL
for (f in file_list) {
 aux <- read.table(f,header=TRUE)
 err_rms <- cbind(err_rms,aux$err_rms)
 mean <- cbind(mean,aux$mean)
}
rm(aux,f)

