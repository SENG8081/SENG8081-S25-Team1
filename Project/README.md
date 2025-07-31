# Project

## Install Dependencies

```shell
$ pip install -r requirements.txt
```

## Start

```shell
$ python main.py
```

## Configuration Tasks

- Configure tasks in setup_scheduler() in main.py
- if you want to add a task, add a tuple type element to the tasks[] array like: `(taskFunc, trigger)`
  - taskFunc, is a function type variable
  - trigger, can be a CronTrigger or an IntervalTrigger (more details see the doc of apscheduler)

## Data Storage and Maintenance

For this project, long-term and secure data storage is essential to ensure both regulatory compliance and practical access in the future. We need a solution that supports scalability, flexibility, and efficient data retrieval as our dataset grows.

- i. Where to store the data: Currently, we are running MongoDB locally in a Docker container for development and testing purposes. This setup provides flexibility and ease of setup during early-stage development. In the future, we plan to migrate to MongoDB Atlas, a fully managed cloud service that offers high availability, automated backups, and built-in tools for data visualization and advanced querying. It also supports features like full-text search and AI-powered capabilities such as vector search, which may be useful as our project evolves.

- ii. What tools to store the data: We chose MongoDB as our primary database system. A key advantage of MongoDB is its schema-free document model, which is ideal for handling data from diverse and inconsistent sources. Our project integrates data from multiple channels—such as public APIs, scraped content, and CSV imports—each with its own structure and format. MongoDB allows us to store and query these varied datasets in a flexible way, without enforcing a rigid schema. This greatly simplifies our data ingestion and transformation process, while supporting efficient querying and future scalability.

