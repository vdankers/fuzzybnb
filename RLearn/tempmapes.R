
mfs <- c("TRIANGLE", "TRAPEZOID", "SIGMOID","BELL")
defuzzes <- c("WAM", "FIRST.MAX", "LAST.MAX", "MEAN.MAX")
imps <- c("DIENES_RESHER", "LUKASIEWICZ", "GOGUEN", "GODEL", "SHARP", "MIZUMOTO", "DUBOIS_PRADE")
norms <- c("HAMACHER", "YAGER", "BOUNDED")
for (numlab in c(3,4,6,7)) {
	load(paste("C:\\Users\\Alex\\Documents\\GitHub\\fuzzybnb\\RLearn\\RWorkspaces\\", as.character(numlab), sep=""))
	print(as.character(numlab))
	print(showMAPE(res.test, data.targets))
}

for (mf in mfs) {
	load(paste("C:\\Users\\Alex\\Documents\\GitHub\\fuzzybnb\\RLearn\\RWorkspaces\\", mf, sep=""))
	print(mf)
	print(showMAPE(res.test, data.targets))
}
for (defuzz in defuzzes) {
	load(paste("C:\\Users\\Alex\\Documents\\GitHub\\fuzzybnb\\RLearn\\RWorkspaces\\", defuzz, sep=""))
	print(defuzz)
	print(showMAPE(res.test, data.targets))
}
for (imp in imps) {
	load(paste("C:\\Users\\Alex\\Documents\\GitHub\\fuzzybnb\\RLearn\\RWorkspaces\\", imp, sep=""))
	print(imp)
	print(showMAPE(res.test, data.targets))
}

for (norm in norms) {
	load(paste("C:\\Users\\Alex\\Documents\\GitHub\\fuzzybnb\\RLearn\\RWorkspaces\\", norm, sep=""))
	print(norm)
	print(showMAPE(res.test, data.targets))
}