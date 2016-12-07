# type of method
method.type <- "ANFIS"

# a list containing all arguments
# differs per method
# 5 linguistic terms, 100 maximum iterations, step size 0.1
# tnorm is min, implication function is Zadeh, name is fuzzybnb
# implication function applies to rules, Zadeh function means
######################################################
# IF a < 0.5 OR 1 - a < b THEN
#  IF TRUE
#    return 1 - a
#  ELSE
#    IF a < b THEN
#      IF TRUE
#        return a
#      ELSE
#        return b
# (a < 0.5 || 1 - a > b ? 1 - a : (a < b ? a : b))
######################################################
control <- list(num.labels = 5, max.iter = 100, step.size = 0.1,
  type.tnorm = "PRODUCT", type.implication.func = "DIENES_RESHER", name = "fuzzybnbANFIS")

# Learn rules, to get membership functions
# explanation of arguments:
# https://www.rdocumentation.org/packages/frbs/versions/3.1-0/topics/frbs.learn
object.reg <- frbs.learn(data.train, range.data, method.type, control)

# output should be [1] 5.1 4.1 4.1 2.1
par("mar")

par(mar=c(1,1,1,1))

# show membership functions
pdf("RLearn/ANFISMF.pdf")
par("mar")

par(mar=c(1,1,1,1))
plotMF(object.reg)
dev.off()

# test
res.test <- predict(object.reg, data.test)

# show error
error = sum(abs(res.test - data.targets))/length(data.targets)
print(error)
