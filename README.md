# JEDHA BOOTCAMP PROJECTS

This repository contains all the projects needed to validate the certification blocks for the RNCP level 7 "Machine Learning Engineer" qualification.

## Contents
* **Block 1** - Build & Manage a Data Infrastructure
  * _Data Collection and Management project (Kayak)_

* **Block 2** - Exploratory Data Analysis
  * _Exploratory Data Analysis project (Speed Dating)_
  * _Big Data project_

* **Block 3** - Machine Learning
* **Block 4** - Deep Learning
* **Block 5** - Deployment
* **Block 6** - Lead a data project

---

All projects are composed in this way:
* A `work` folder containing all the code
* A `resources` folder containing all initial resources (datasets, instructions, notebooks)
* Deliverables are at the root of the project.

## Installation

```bash
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

Add a `.env` file with :

```js
WEATHER_USERNAME=fill_this
WEATHER_PASSWORD=fill_this
WEATHER_KEY=fill_this
AWS_KEY=fill_this
AWS_SECRET=fill_this
```
