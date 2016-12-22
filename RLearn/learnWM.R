method.type <- "WM"

# params needed to run frbs.learn
control <- list(num.labels = 7, type.mf = "GAUSSIAN", type.tnorm = "PRODUCT",
  type.defuz = "FIRST_MAX", type.implication.func = "MIN", name = "fuzzybnbWM")


# Get frbs object
object.reg <- frbs.learn(data.train, range.data, method.type, control)

print("Learning phase is over, starting testing")
res.test <- predict(object.reg, data.test)

# show MAE
error = sum(abs(data.targets-res.test))/length(data.targets)
print(error)

save.image(file="Latest-optimal-wm")


# plot some figures
pdf("Rplots/WMMF-latest.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

pdf("Rplots/WMErrorRatio.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotthis <- c()
i <- 5
while (i < 300) {
  plotthis[i] <- length(which(abs(res.test-data.targets)<i))/length(data.targets)
  i <- i + 5
}
plot(plotthis, xlab="error in amount of euros", ylab="percentage of data set with error x or less")
dev.off()


pdf("Rplots/WMTargetsVsPredict.pdf")
par("mar")
par(mar=c(1,1,1,1))
plot(data.targets, col="red", ylab="prices", xlab="index")
points(res.test)
dev.off()

pdf("Rlearn/WMErrorRatio.pdf")
par("mar")
par(mar=c(1,1,1,1))
nums <- seq(0,1,0.01)
plotthis <- c()
for (num in nums) {plotthis <- c(plotthis, length(which(abs(res.test-data.targets)/data.targets<num))/length(data.targets)) }
plot(plotthis,ylab="Percentage of the data which is off by x percent or less", xlab="Percentage by which the price is off" )
dev.off()
