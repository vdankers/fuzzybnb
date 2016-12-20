# Test all parameters
method.type <- "WM"

mfs <- c("TRIANGLE", "TRAPEZOID", "SIGMOID","BELL")
defuzzes <- c("WAM", "FIRST.MAX", "LAST.MAX", "MEAN.MAX")
imps <- c("DIENES_RESHER", "LUKASIEWICZ", "GOGUEN", "GODEL", "SHARP", "MIZUMOTO", "DUBOIS_PRADE")
norms <- c("HAMACHER", "YAGER", "BOUNDED")

for (numlab in c(3,4,6,7)) {
  control <- list(num.labels = numlab, type.mf = "GAUSSIAN", type.tnorm = "PRODUCT",
    type.defuz = "COG", type.implication.func = "ZADEH", name = "fuzzybnbWM")

  object.reg <- frbs.learn(data.train, range.data, method.type, control)

  print("Done learning, starting testing phase for:")
  print(as.character(numlab))

  res.cv <- predict(object.reg, data.cv)

  # show MAE
  error = sum(abs(data.cvtargets-res.cv))/length(data.cvtargets)
  print(error)
  plot(data.cvtargets, col="red", ylab="prices", xlab="index")
  points(res.cv)

  # save workspace for easy access and generating figures
  save.image(file=as.character(numlab))
}

for (mf in mfs) {
  control <- list(num.labels = 5, type.mf = mf, type.tnorm = "PRODUCT",
    type.defuz = "COG", type.implication.func = "ZADEH", name = "fuzzybnbWM")

  object.reg <- frbs.learn(data.train, range.data, method.type, control)

  print("Done learning, starting testing phase for:")
  print(mf)

  res.cv <- predict(object.reg, data.cv)

  # show MAE
  error = sum(abs(data.cvtargets-res.cv))/length(data.cvtargets)
  print(error)
  plot(data.cvtargets, col="red", ylab="prices", xlab="index")
  points(res.cv)
  # save workspace for easy access and generating figures
  save.image(file=as.character(mf))
}

for (norm in norms) {
  control <- list(num.labels = 5, type.mf = "GAUSSIAN", type.tnorm = norm,
    type.defuz = "COG", type.implication.func = "ZADEH", name = "fuzzybnbWM")

  object.reg <- frbs.learn(data.train, range.data, method.type, control)

  print("Done learning, starting testing phase for:")
  print(norm)

  res.cv <- predict(object.reg, data.cv)

  # show MAE
  error = sum(abs(data.cvtargets-res.cv))/length(data.cvtargets)
  print(error)
  plot(data.cvtargets, col="red", ylab="prices", xlab="index")
  points(res.cv)
  # save workspace for easy access and generating figures
  save.image(file=norm)
}

for (defuz in defuzzes) {
  control <- list(num.labels = 5, type.mf = "GAUSSIAN", type.tnorm = "PRODUCT",
    type.defuz = defuz, type.implication.func = "ZADEH", name = "fuzzybnbWM")

  object.reg <- frbs.learn(data.train, range.data, method.type, control)

  print("Done learning, starting testing phase for:")
  print(defuz)

  res.cv <- predict(object.reg, data.cv)

  # show MAE
  error = sum(abs(data.cvtargets-res.cv))/length(data.cvtargets)
  print(error)
  plot(data.cvtargets, col="red", ylab="prices", xlab="index")
  points(res.cv)
  # save workspace for easy access and generating figures
  save.image(file=defuz)
}

for (im in imps) {
  control <- list(num.labels = 5, type.mf = "GAUSSIAN", type.tnorm = "PRODUCT",
    type.defuz = "COG", type.implication.func = im, name = "fuzzybnbWM")

  object.reg <- frbs.learn(data.train, range.data, method.type, control)

  print("Done learning, starting testing phase for:")
  print(im)

  res.cv <- predict(object.reg, data.cv)

  # show MAE
  error = sum(abs(data.cvtargets-res.cv))/length(data.cvtargets)
  print(error)
  plot(data.cvtargets, col="red", ylab="prices", xlab="index")
  points(res.cv)
  # save workspace for easy access and generating figures
  save.image(file=im)
}
