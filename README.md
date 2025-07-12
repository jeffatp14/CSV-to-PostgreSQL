# CAD IT Data Engineer Test
This repository contains answer and documentation for CAD IT Code Test - Data Engineer by **Jeffa Triana Putra**.

## 1. Data Modeling
Based on given datasets about ratings and movie information in '.csv' format, writer designed ERD for conceptual, logical, and physical data model.
In the given datasets, there are 9 column, named MOVIES,YEAR,GENRE,RATING,ONE-LINE,STARS,VOTES,RunTime, and Gross. I decomposed the datasets into fact table, dimensional tables, and junction tables. **Fact table** contains measureable fields (year,rating,votes,runtime) and necessary information such as movie name. **Dimensional table** separated into 4 tables, which contains additional description of the fact table such as: stars, directors, movie one-line, and genre. Junction table will be needed as some of the table relation include **many-to-many relationship**.

### Conceptual data model : shows which table relate to each other
![alt text](https://github.com/jeffatp14/CadITDataEngTest/blob/main/conceptual_data%20model.jpeg)

### Logical data model : shows attribute of each table

### Logical data model : shows attribute of each table, implemented table name, and its column type

## 2. Database creation

