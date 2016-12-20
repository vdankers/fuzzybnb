
showAbsErrorRatio <- function(res.test,data.targets,steps=5,max=300, save=FALSE, name="AbsErrorRatio") {
	plotthis <- c()
	i <- steps
	while (i < max) {
	  plotthis[i] <- length(which(abs(res.test-data.targets)<i))/length(data.targets)
	  i <- i + steps
	}
	if (save) {
		pdf(paste("Rplots/", name, "pdf", sep=""))
		par(mar=c(1,1,1,1))
		plot(plotthis, xlab="error in amount of euros", ylab="percentage of data set with error x or less")
		dev.off()
	} else {
		dev.new()
		plot(plotthis, xlab="error in amount of euros", ylab="percentage of data set with error x or less")
	}
	return (plotthis)
}

showPercErrorRatio <- function(res.test,data.targets, steps=0.01, max=1,save=FALSE, name="PercErrorRatio") {
	nums <- seq(0,1,0.01)
	plotthis <- c()
	for (num in nums) {plotthis <- c(plotthis, length(which(abs(res.test-data.targets)/data.targets<num))/length(data.targets)) }
	if (save) {
		pdf(paste("Rplots/", name, "pdf", sep=""))
		par(mar=c(1,1,1,1))
		plot(plotthis,ylab="Percentage of the data which is off by x percent or less", xlab="Percentage by which the price is off" )
		dev.off()
	} else {
		dev.new()
		plot(plotthis,ylab="Percentage of the data which is off by x percent or less", xlab="Percentage by which the price is off" )
	}

	return (plotthis)
}

showMAPE <- function(res.test,data.targets) {
	return (sum((abs(res.test-data.targets)/data.targets)/length(data.targets))*100)
}

showMAE <- function(res.test,data.targets) {
	return (sum(abs(data.targets-res.test))/length(data.targets))
}

showPredVsTarg <- function (res.test,data.targets) {
	dev.new()
	plot(data.targets, col="red", ylab="prices", xlab="index")
	points(res.test)

	return (showMAE(res.test,data.targets))
}

showAll <- function(res.test, data.targets) {
	AbsRatio <- showAbsErrorRatio(res.test,data.targets)
	PercRatio <- showPercErrorRatio(res.test,data.targets)
	MAE <- showPredVsTarg(res.test,data.targets)
	MAPE <- showMAPE(res.test,data.targets)

	print("MAE:")
	print(MAE)

	print("MAPE:")
	print(MAPE)
	return (c(AbsRatio, PercRatio, MAE, MAPE))
}