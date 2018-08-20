# DataCamp Download
I have built an unofficial class to give an easy way to download DataCamp source code, and the datasets used in the course.

## Getting Started

All the necesary libraries for run the project are in the requirements.txt.

### Use of the class

There is a simple practical example in dataCamp_download.py, for download your course code, you must have completed the course.

```
python dataCamp_download.py -u user_datacamp -p pass_datacamp -q course_url
```

course_url sample
```
https://www.datacamp.com/courses/intro-to-python-for-data-science
```
This command will create a directory structure where you will find the chapters of the course and its source code.


## TODO

#### Get requirements.txt of the chapter