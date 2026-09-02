import os
import pandas as pd

courses = [
    {
        "course_id": "IGOT-STAT-001",
        "course_name": "Fundamentals of Official Statistics & National Accounts",
        "domain": "Statistical",
        "skills_covered": "National Accounts, GDP Estimation, Macroeconomic Aggregates, Statistical Standards",
        "description": "Comprehensive guide to national accounting frameworks, GDP calculation methodologies, and macroeconomic data collection standards used in India's official statistical system.",
        "duration_hours": 15
    },
    {
        "course_id": "IGOT-STAT-002",
        "course_name": "Sample Survey Design & Estimation Methodologies",
        "domain": "Statistical",
        "skills_covered": "Sample Surveys, Stratified Sampling, Cluster Sampling, Estimation Error, NSSO Framework",
        "description": "Mastering sample survey design, probability sampling techniques, weight generation, and sampling error estimation for large-scale household and enterprise surveys.",
        "duration_hours": 20
    },
    {
        "course_id": "IGOT-STAT-003",
        "course_name": "Consumer Price Index (CPI) & Inflation Metrics Calculation",
        "domain": "Statistical",
        "skills_covered": "Inflation Analytics, CPI Calculation, Index Number Theory, Laspeyres Index, Price Data Collection",
        "description": "In-depth training on price index construction, basket weighting, urban and rural CPI estimation, and inflation trend monitoring.",
        "duration_hours": 12
    },
    {
        "course_id": "IGOT-TECH-001",
        "course_name": "Python for Statistical Data Analytics & Processing",
        "domain": "Technical",
        "skills_covered": "Python, Pandas, NumPy, Data Cleaning, Exploratory Data Analysis, Matplotlib",
        "description": "Hands-on Python programming for automated data ingestion, missing value imputation, tabular data manipulation, and statistical visualization.",
        "duration_hours": 25
    },
    {
        "course_id": "IGOT-TECH-002",
        "course_name": "R Programming for Survey Data Analysis & Econometrics",
        "domain": "Technical",
        "skills_covered": "R Language, Tidyverse, Regression Analysis, Survey Package, Econometrics",
        "description": "Statistical modeling and econometrics using R. Learn to process survey micro-data, run linear regressions, and generate publication-ready tables.",
        "duration_hours": 30
    },
    {
        "course_id": "IGOT-TECH-003",
        "course_name": "Geospatial Data Analytics & GIS in Official Statistics",
        "domain": "Technical",
        "skills_covered": "GIS, QGIS, Spatial Analytics, Geo-tagging, Boundary Mapping, Remote Sensing Data",
        "description": "Introduction to Geographic Information Systems (GIS) for spatial sampling, district-level data visualization, and integrating satellite imagery with census data.",
        "duration_hours": 18
    },
    {
        "course_id": "IGOT-TECH-004",
        "course_name": "Big Data Analytics & Cloud Infrastructure for Large Datasets",
        "domain": "Technical",
        "skills_covered": "Big Data, PySpark, Distributed Computing, SQL Databases, Data Warehousing",
        "description": "Managing terabyte-scale administrative and sensor data pipelines using Spark, distributed databases, and modern cloud analytics.",
        "duration_hours": 22
    },
    {
        "course_id": "IGOT-GOV-001",
        "course_name": "Data Privacy, Security & Ethics in Government Statistics",
        "domain": "Digital Governance",
        "skills_covered": "Data Privacy, DPDP Act 2023, Data Security, Anonymization Techniques, Ethical AI",
        "description": "Understanding compliance under the DPDP Act 2023, micro-data anonymization techniques, data confidentiality protocols, and responsible AI usage.",
        "duration_hours": 10
    },
    {
        "course_id": "IGOT-GOV-002",
        "course_name": "Digital Governance & Open Data Dissemination Platforms",
        "domain": "Digital Governance",
        "skills_covered": "Open Data Portals, API Development, Data Dissemination, Metadata Standards, SDMX",
        "description": "Best practices for open data dissemination, setting up statistical APIs, complying with SDMX standards, and managing public data portals.",
        "duration_hours": 14
    },
    {
        "course_id": "IGOT-MGT-001",
        "course_name": "Field Survey Team Leadership & Operational Management",
        "domain": "Behavioural/Managerial",
        "skills_covered": "Field Operations, Team Management, Data Quality Control, Conflict Resolution",
        "description": "Leadership techniques for field supervisors overseeing primary data collection, managing survey teams, and ensuring field-level data quality.",
        "duration_hours": 8
    },
    {
        "course_id": "IGOT-STAT-004",
        "course_name": "Index of Industrial Production (IIP) & Economic Indicators",
        "domain": "Statistical",
        "skills_covered": "IIP Calculation, Factory Sector Statistics, Manufacturing Growth, Base Year Revisions",
        "description": "Detailed walkthrough of IIP compilation, factory data collection from ASI, monthly growth index computation, and seasonal adjustment.",
        "duration_hours": 12
    },
    {
        "course_id": "IGOT-STAT-005",
        "course_name": "Periodic Labour Force Survey (PLFS) & Employment Analytics",
        "domain": "Statistical",
        "skills_covered": "PLFS Methodology, Labour Force Participation Rate, Worker Population Ratio, Unemployment Metrics",
        "description": "Understanding key labor indicators, activity status classification (CWS vs USAE), and quarterly/annual PLFS report analysis.",
        "duration_hours": 16
    }
]

df = pd.DataFrame(courses)
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
output_path = os.path.join(output_dir, "mock_igot_catalog.csv")

df.to_csv(output_path, index=False)
print(f"Successfully generated {len(df)} courses in {output_path}")
