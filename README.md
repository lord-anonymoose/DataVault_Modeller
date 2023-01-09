# DataVault_Modeller
Cross-platform application for modelling databases based on Data Vault architecture

The following app helps system analysts DWH and ETL-developers build Data Warehouses based on Data Vault architecture. Data Vault implies 3 stereotypes for tables:
- Hubs. Tables consisting primary key and technical attributes of a specific business entity (e.g. clients, accounts and employees)
- Sattelite. Tables referencing a hub by primary key and containing descriptive data with business history support
- Link. Tables referencing connection between two different hubs (e.g. clients and accounts)

The application takes 2 Excel files as its input:
- Logical Data Model (see a template in Sample/LDM_Sample.xlsx) with all existing fields and tables.
- Data Modelling Standard (see a template in Sample/Standards_Sample.xlsx) with all mandatory fields for hubs, sattelites and links.

There are two major functions of DataVault_Modeller: checking Logical Data Model file and generating DDL-scripts for creating tables in a database.

App includes following tests:
- Input file structure
- Symbols validation for table and column names
- Stereotype validation (should only include HUB/SAT/LNK values)
- Data Types validation
- Column duplicates
- Empty table and column descriptions
- Mandatory fields for stereotypes based on Data Modelling Standards

DataVault_modeleler gives output to a folder chosen by user. error_report.txt file contains Model errors, while scripts.sql - DDL-scripts for creating tables.  
