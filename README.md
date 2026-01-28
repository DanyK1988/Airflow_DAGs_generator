# Airflow_DAGs_generator
Built automatic DAG generator for Airflow supporting Python &amp; SQL, task extraction, scheduling, and template-based DAG creation.

🚀 Airflow DAG Auto Generator
A local tool for automatic generation of Apache Airflow DAGs from Python and SQL source files.
The generator scans a folder with scripts and produces ready-to-run DAGs using Jinja2 templates.
Each source file becomes a single DAG, and internal logic is automatically split into multiple Airflow tasks.
This project is designed for local usage with Docker-based Airflow setups (no cluster required).  

✨ Features
 - Supports Python and SQL scripts 

 - Automatically generates one DAG per source file  

 Task splitting:
 - Python → one task per def function
 - SQL → one task per statement / DDL block (CREATE, DROP, ALTER, TRUNCATE)
 - Schedule extracted directly from source code
 - DAG start date = generation date
 - Jinja2-based templating
 - Automatic task dependencies
 - Prevents duplicate processing by marking scripts as .processed
 - No credentials stored inside DAGs (uses Airflow connections)
 - Docker-friendly

 📁 Project Structure  
 
 .  
 
├── scripts/        # Input Python / SQL files  

├── templates/      # Jinja2 DAG templates  

├── dags/           # Generated Airflow DAGs  

├── generator.py    # Main generator script  

└── README.md  


🧠 How It Works
Python scripts
Each .py file becomes one DAG
Every def function becomes a separate Airflow task
Tasks are chained in definition order

SQL scripts
Each .sql file becomes one DAG
SQL is split into blocks based on DDL / statements
Each block becomes a separate task

⏰ Scheduling  

Schedule is extracted from the script using a comment:  

-- schedule: @daily  

schedule: 0 2 * * *  


🛠 Requirements
Python 3.9+
Apache Airflow
Jinja2

🎯 Use Cases
 - Rapid DAG prototyping
 - SQL → Airflow migration
 - Automating legacy scripts
 - Analytics / Data Engineering pipelines
 - Educational Airflow projects

