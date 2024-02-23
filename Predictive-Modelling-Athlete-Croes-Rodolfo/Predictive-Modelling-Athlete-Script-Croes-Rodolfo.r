# general prerequisites
#check for packages if they are installed and then installs them
if (!"tidyverse" %in% installed.packages())
  install.packages("tidyverse")

if (!"dplyr" %in% installed.packages())
  install.packages("dplyr")

if (!"aplpack" %in% installed.packages())
  install.packages("aplpack")

if (!"survival" %in% installed.packages())
  install.packages("survival")

if (!"nortest" %in% installed.packages())
  install.packages("nortest")

if (!"car" %in% installed.packages())
  install.packages("car")

library('tidyverse')
library('readxl')
library('dplyr')
library('nortest')
library('car')
#read data in
assignmentData <- read_excel(path = "Athlete Data.xlsx", sheet="Sheet1")
# Question 1
#check the head to see what data types I am dealing with
head(assignmentData)
#see what the column name in the data is
colnames(assignmentData)
#show dimension of entire dataset
dim(assignmentData)
#using plyr library, count occurences of unique variable in Sex
n_distinct(assignmentData$Sex)
sum(assignmentData$Sex=='male')
sum(assignmentData$Sex=='female')
#attach the data to use their names as variables
attach(assignmentData)
#check for missing values in LBM and BMI
which(is.na(LBM))
which(is.na(BMI))
#for the LBM and BMI, we show the five number summary and the mean to describe the data
summary(assignmentData, digits=5)
#find the variance and standard deviation of the LBM and BMI
var(LBM)
var(BMI)
sd(LBM)
sd(BMI)
#plot the data to visualize it, starting with LBM
ggplot(assignmentData, aes(x=LBM)) + 
  geom_histogram(fill="purple", color="black") +
  ggtitle("Histogram of LBM")
boxplot(LBM,
        main= "LBM plot",
        ylab="LBM in Kg")
stem(LBM)
#plot the BMI data
ggplot(assignmentData, aes(x=BMI)) +
  geom_histogram(fill="yellow", color="black") +
  ggtitle("Histogram of BMI")
boxplot(BMI,
        main="BMI plot",
        ylab="BMI unit")
stem(BMI)
# QUestion 2
#Use a T test to check if there is a difference between male and female LBM's
#separate male & female data in different dataframes
maledata <- filter(assignmentData, Sex=="male")
femaledata <- filter(assignmentData, Sex=="female")
#before using T-test, we must perform a normality test (this case Anderson darling test)
ad.test(maledata$LBM)
ad.test(femaledata$LBM)
#start with h0: mean male LBM = mean female LBM. H1: mean male LBM != mean female LBM
malemean <- mean(maledata$LBM)
malestd <- sd(maledata$LBM)
malecount <- nrow(maledata)
femalemean <- mean(femaledata$LBM)
femalestd <- sd(femaledata$LBM)
femalecount <- nrow(femaledata)
#find the pooled variance
sp2 <- ((malecount-1)*malestd^2+(femalecount-1)*femalestd^2)/(malecount+femalecount-2)
#calculate the observed statistic
tobs <- (malemean-femalemean)/(sqrt(sp2*(1/malecount+1/femalecount)))
#find the p value for the t test
pvalue <- 2*pt(abs(tobs),df=malecount+femalecount-2, lower.tail=FALSE)
#Question 3
#calculate the corelation coefficient of the LBM and BMI of both males and females
# start by plotting the LBM and BMI against eachother to see how they relate
plot(maledata$BMI, maledata$LBM)
plot(femaledata$BMI, femaledata$LBM)
#given that these data are normalized, we use the pearson corelation coefficient for both
malecor <- cor(maledata$LBM, maledata$BMI)
femalecor <- cor(femaledata$LBM, femaledata$BMI)
#Question 4
#start by looking at the box plot and see if there are any outliers to handle before making the model
boxplot(maledata$BMI,
        main="BMI plot",
        ylab="BMI unit")
boxplot(maledata$LBM,
        main="LBM plot",
        ylab="LBM in Kg")
#both the LBM and BMI of the male data have no extreme outliers thus we make the model using linear regression
malemodel <- lm(LBM ~ BMI, data = maledata)
#get a description of our model
summary(malemodel)
#plot the regression line of the model
plot(maledata$BMI, maledata$LBM)
abline(lm(LBM ~ BMI, data = maledata))
#Question 5
#Call a predict function to predict the LBM of a male with a BMI of 25
predictedLBM <- predict(malemodel, data.frame(BMI = 25))
print(predictedLBM)
#Question 6
#Assess the normality of the residuals of the model
ad.test(malemodel$residuals)
#Plot the fitted vs actual line of the model
plot(maledata$LBM, malemodel$fitted.values)
abline(a=0, b=1)
