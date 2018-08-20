# DataCamp Download
I have built an unofficial class to give an easy way to download DataCamp source code, and the datasets used in the course.

## Getting Started

All the necesary libraries for run the project are in the requirements.txt.

### Use of the class

There is a simple practical example in dataCamp_download.py, for download your course code, you must have completed the course. This command will create a directory structure where you will find the chapters of the course and its source code.

```
python dataCamp_download.py -u user_datacamp -p pass_datacamp -q course_url
```

course_url sample
```
https://www.datacamp.com/courses/intro-to-python-for-data-science
```

Exercise source code file example
```
#COMPARING A HISTOGRAM AND DISTPLOT

#STATEMENT
'''
The pandas library supports simple plotting of data, which is very convenient when data
is already likely to be in a pandas DataFrame.

'''

#INSTRUCTIONS
'''
Use the pandas' plot.hist() function to plot a histogram of the Award_Amount column.
'''

#EXERCISE SOURCE CODE


#Comparing a histogram and distplot subexercise 0

# Display pandas histogram
df['Award_Amount'].plot.hist()
plt.show()

# Clear out the pandas histogram
plt.clf()

#Comparing a histogram and distplot subexercise 1

# Display a Seaborn distplot
sns.distplot(df['Award_Amount'])
plt.show()

# Clear the distplot
plt.clf()
```


## TODO

#### Get requirements.txt of the chapter