method.type <- "WM"

# params needed to run frbs.learn
control <- list(num.labels = 8, type.mf = "GAUSSIAN", type.tnorm = "PRODUCT",
  type.defuz = "COG", type.implication.func = "DIENES_RESHER", name = "fuzzybnbWM")


# Learn rules, to get membership functions
# explanation of arguments:
# https://www.rdocumentation.org/packages/frbs/versions/3.1-0/topics/frbs.learn
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# show membership functions

print("Learning phase is over, starting testing")

res.test <- predict(object.reg, data.test)

# show MAE
error = sum(abs(data.targets-res.test))/length(data.targets)
print(error)
save.image(file=im)


# plot some figures
pdf("RPlots/WMMF-latest.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

pdf("Rlearn/WMErrorRatio.pdf")
par("mar")
par(mar=c(1,1,1,1))
plotthis <- c()
i <- 1
while (i < 200) {
  plotthis[i] <- length(which(abs(res.test-data.targets)>i))/length(data.targets)
  i <- i + 1
}
plot(plotthis, xlab="error in amount of euros", ylab="percentage of data set with error higher than x")
dev.off()


pdf("Rlearn/WMTargetsVsPredict.pdf")
par("mar")
par(mar=c(1,1,1,1))
plot(res.test, col="red", ylab="prices", xlab="index")
points(data.targets)
dev.off()
