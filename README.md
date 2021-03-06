# DS-GA 1004 Project Proposal

Hetian Bai (hb1500@nyu.edu), Jieyu Wang (jw4937@nyu.edu), Zhiming Guo (zg758@nyu.edu)

## Abstract

With the collection of various types of data in spatial and temporal over years, the urban environments in New York City can be represented by these datasets in different categories. To unfold the interesting and hidden relationship among NYC urban data, it is vital to not only consider the relationship between two features within a single dataset, but also the relationships cross many datasets. With a well-designed program, researchers can easily discover relationships between any two features in NYC city datasets. These new findings can possibly help city management, disease control, traffic improvement, etc.

Our goal for this project is to design a pipeline under Hadoop and Spark, which allows users to explore any two features' correlation (entropy and mutual information) from the existing datasets in NYC Open Data. At the same time, some hypotheses will be tested under this architecture, such as the faster speed of wind or the lower visibility would lead to more frequent collision; Poorer neighborhood has higher crime rate, etc. A further step of this project, we propose our innovative idea that is to use proper ways to visualize correlations of features.

## Introduction

NYC Open Data makes the wealth of public data generated by various New York City agencies and other City organizations available for public use. As of December 2016, there are over 1,600 datasets available on the NYC Open Data Catalog. These datasets cover categories such as Business, City Government, Education, Environment and Health. For this project, we propose to use 10 datasets, which are: taxi data, vehicle collision, weather, 311 service request, City bike trip histories, crime data, property price, Census demographics. Census income, and Census shape. Analyzing these datasets could reveal hidden correlations between different columns, and thus provide insights for lots of social challenges facing by New York Citizens such as transportation, resource consumption and public service quality. 

## Problem formulation

In order to compute hidden relationships between features cross multiple datasets and provide a user friendly interface, we are aiming to establish a package that can be used to compute correlations (entropy/mutual information) between columns in different datasets. In this package, in the first stage, data cleansing and formating will be applied to all datasets. Next, datasets will be combined and matched from two perspectives--spatial and temporal resolution. Following that, cross-entropy/mutual information will be calculated. Once the program has obtained all the correlations, results will be saved in the squared matrix like a covariance matrix. This allows used to query any two or more features to extract corresponding correlations. To have further analysis, we will propose possible hypothesis based on the correctional results. In order to better present our results, we will provide visualization and analytics of some significant and interesting correlations we found cross datasets.

We will wrap all algorithms into a package and make sure the reproducibility of the framework. The framework should contain data pre-processing pipeline, correlation statistical analysis, and visualization of relationships between interested features. By the end of the project, the team will present this project framework and outputs in GitHub with clear content logic, user instruction, and relevant codes embedded with detailed descriptions for users.


### Datasets Description

*[Yellow Taxi Data](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml)

This dataset includes fields capturing pick-up and drop-off dates/times, pick-up and drop-off locations, trip distances, itemized fares, rate types, payment types, and driver-reported passenger counts from 2009 to 2017.

*[Vehicle Collisions](https://data.cityofnewyork.us/Public-Safety/NYPD-Motor-Vehicle-Collisions/h9gi-nx95)

This dataset contains a breakdown of every collision in NYC by location and injury from July 2012 to March 2018. Each record represents a collision in NYC by city, borough, precinct and cross street. 

*[Weather](https://nyu.box.com/s/6epatrjp0bi8xvd17blzmoy301ikie9z)

This dataset contains weather information from Year 2011 to Year 2018. It includes fields capturing wind speed, viability and temperature. 

*[311](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9)

This dataset contains all 311 service requests from 2010 to April 15 2018. It contains fields capturing request date, agency, complaint type, location type, incident zip, incident address, street name, city, community board and borough.    

*[Citi Bike Trip Histories](https://www.citibikenyc.com/system-data)

This dataset contains Citi bike data from year 2013 to year 2018. It contains fields capturing trip duration, start time and date, stop time and date, start station name, end station name, station id, station latitude and longitude, bike id, user type, gender and year of birth.  

*[Crime Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i)

This dataset includes all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department (NYPD) from year 2006 to the end of year 2016. It contains fields capturing compliant number, complaint date, compliant time, offense description, borough etc.  

*[Property Price](https://nyu.box.com/s/hx7v2mpsw7rkdps6b613tvoiq9a1r448)

*[Census Data - income information](http://www.nyc.gov/html/dcp/html/census/socio_tables.shtml)

*[Census Data (shape files)](http://www.nyc.gov/html/dcp/html/bytes/districts_download_metadata.shtml)


### Methodology: 

* Dataset Transformation: 

In this step, we will implement necessary data cleansing. Also, transform non-numeric data type into numeric which makes further computation possible. 

* Feature Identification:

First, we need to identify which columns of information are redundant in computing correlations. Then, we will do feature engineering. For example, slicing datasets by certain divisions like gender, class, school neighborhood, etc. Also, we could subset data by quantiles or outliners. After having all data columns, subsets ready, we calculate correlations with various measurements like Pearson, Kendall, Spearman, or self-defined measurements. 

* Relationship Evaluation and Visualization:

This attribution allows users to evaluate the strength and direction of relationships between any two attributions in the datasets. User will have options to set thresholds to filter on correlation results. 
A basic visualization function in the algorithms provide users with visualization to help them understand the relationships between attributes. For instance, we could make an elegant and well-labelled correlation matrix which represents the strength and direction of correlation by color. 

## Related works and references: 

The main reference for our project is  "Data Polygamy: The Many-Many Relationships among Urban Spatio-Temporal Data Sets". (Chirigati, F., Doraiswamy, H., Damoulas, T., \& Freire, J, 2015)\cite{chirigati2016data} Data Polygamy, as proposed by this paper, is "a scalable topology-based framework that allows users to query statistically significant relationships between spatio-temporal data sets". Researchers have also performed an experimental evaluation using over 300 spatial-temporal urban data sets which shows that this framework is scalable and effective at identifying interesting relationships. 

## Methods, architecture and design: 

### Architecture and Design

This is the architecture we designed for this project. There are three general procedures which are framed in the figure above: Data Preprocessing, Datasets Combining Process, and Correlation Calculating \& Visualizing. See Figure 

By submitting this report, we have already implemented the first step -- Data Preprocessing. Detailed steps in each procedures will be discussed in Methodology below.

## Methodology

In this step, we use Hadoop Map-Reduce to preprocess each dataset. The preprocessing includes data cleaning and pre-aggregation. For data cleaning, we regulate that features will be ignored if there are over 80\% of values in that feature is missing. In pre-aggregation, we first need to define our unified MapReduce output format to make computing correlations between datasets with all possible spatial and temporal resolutions. In this unified MapReduce output format, the key is temporal and spatial data with identifiers that implies corresponding data resolution, whereas the value is all the other attributes that contains usable information. Specifically, the unified MapReduce format is defined as a key-value pair as follows: 

![cover image](/Architecture.png)

## Reference

[1] Chirigati, F., Doraiswamy, H., Damoulas, T., & Freire, J. (2016, June). Data polygamy: the many-many relationships among urban spatio-temporal data sets. In Proceedings of the 2016 International Conference on Management of Data (pp. 1011-1025). ACM.
