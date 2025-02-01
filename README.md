# Small Application

This is an application that carries out some data processing tasks.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Project Background](#project-background)
4. [Approach to Project](#approach-to-project)
    - [Logic for some decisions taken](#logic-for-some-decisions-taken)
    - [Best Practices](#best-practices)
    

## Prerequisites

- Ensure Docker is running

## Environment Setup

- Clone the repo

```bash 
git clone https://github.com/Nancy9ice/sample-project.git
```

- Build the docker application

```bash
docker build -t simple-app
```

- Run the docker application

```bash
docker run simple-app
```

## Project Background

A community of 500 members in Canada wants to launch a mentorship program within its peers.

The program comes with the following requirements:
- Mentors: Every female who is at least 40yo (>=40) and who joined the community before or on the 1st January 2004 (<= 2004-01-01).

- Mentorees: Every member who is under 30yo (<=30).

Here are the following steps as expected to complete this project:

- Step 1: Write a code that collects 500 records using this API: Random User Generator. In order
to retrieve the right dataset of users, you need to make sure to use the ca nationality and the
seed vendease.

- Step 2: Create a class that will be used to create members objects, Every member object should have at least the following information:
    - UUID (login UUID)
    - Fullname (Firstname + Lastname)
    - Email
    - Age
    - Gender
    - Id (Value)
    - Registered date (date and time)
    - Address (Street + Postcode + City)

- Step 3: Use the data retrieved in Step 1 to create a list of 500 members' objects

- Step 4: Create a class that will be used to create mentorships object, every mentorship should have at least the following information:

    - UUID (randomly generated)
    - Mentor_uuid (UUID from the member object of the mentor)
    - Mentoree_uuid (UUID from the member object of the mentoree)

- Step 5: Use the members' objects to generate mentorships following this model:

Every mentoree is assigned by order of registered date ( first joined is first assigned ). Mentorees will be assigned evenly to mentors following the registered date of the mentors. 

For example: given the following input with 2 mentors and 5 mentorees

    
| Mentor name |Mentor registered date |
|-------------|------------------------|
|Colin Matthews | 2001-03-18T11:00:29.000Z
|Depp Williams | 2002-03-19T10:07:46.000Z

| Mentoree name | Mentoree registered date |
|-------------|------------------------|
|John Davis | 2005-06-20T10:05:29.000Z
|Patrick Kart | 2002-01-09T03:06:56.000Z
|Emma Themp | 2010-02-07T05:04:23.000Z
|Will Burt | 2011-04-08T06:02:12.000Z
|Jack Riep | 2020-12-30T00:01:10.000Z

The mentorships that will be generated should be in this order:

1. Patrick kart to Colin Matthews
2. John Davis to Depp Williams
3. Emma Themp to Colin Matthews
4. Will Burt to Depp Williams
5. Jack Riep to Colin Matthew

- Step 6: Create 1 dataframe that will contain all 500 member objects generated in Step 3, the columns should match the member class properties.

- Step 7: Create 1 dataframe that will contain all mentorships objects generated in Step 5, the columns should match the mentorship class properties.

- Step 8: Create a function that will take as parameters the 2 dataframes created in Step 6&7 and return the median age of male mentorees that registered after 2010 (>=2010-01-01).

- Step 9: Create a function that will take as parameters the 2 dataframes created in Step 6&7. Write a SQL query inside the function that will calculate the total number of mentorees (by gender) who are mentored by a member who is at least 60yo Then print that number. To execute the query you could use a library such as pandasql.

- Step 10. Create a function that checks for data discrepancy.

## Approach to Project

### Logic for some decisions taken

To accomplish this project, I made certain decisions and implemented some best practices. 

Listed below are the decisions I took as I followed the stated steps:

- I used classes and functions to ensure that the code can be easily maintained and be readable.

- The registered_date was parsed using `datetime.strptime` to ensure that it's in the correct datetime format. This is important to aid data filtering.

- Merging both the mentorship_df and member_df makes it easy to access user information that I couldn't access when I use either of the dataframes.

- Using the Round-Robin method in assigning mentees to mentors ensures even allocation. This prevents one mentor from having so much more mentees that others.

- It was important to convert the list of dictionaries to a dataframe for further processing. Hence, the `json_normalize` method was used.

- `pandasql` library was used to ensure good interaction with the pandas dataframe using SQL. This allowed me the need to not write complex queries to get desired results.

### Best Practices

Listed Below are best practices that I adopted while working on this project:

- Logging: The use of logging was important to know the progress of the execution of my code. And in cases where errors occur, logging helps to identify the codelines that cause these errors.

- Use of functions and Classes: Functions and classes were used to make the code modular. This helps in making it readable and easy to maintain.

- Error handling: Error handling was implemented to ensure that scenarios are caught when the code doesn't do the desired.

- Data Validation: It was important to check for missing data during data processing steps to aid data integrity.
