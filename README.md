[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# Codeforces Practice Contest Generator

## Description

This project is a web application that helps users create **custom practice contests** using Codeforces problems.

The application connects to the **Codeforces API** and checks which problems each user has already solved. It then filters out solved problems and selects **new unsolved problems** based on the chosen difficulty (rating range) and problem topics (tags). This saves time and makes practice more focused and effective.

Multiple users can join the same contest for **group practice**. All participants solve the same set of problems, and the application can display a **standings table** based on real Codeforces submission data.

The project is built with **Flask**, uses a **database** to store contest data, runs inside **Docker**, includes **CI/CD with GitHub Actions**, and is deployed online using **Railway**.


## Setup

### Run locally (Python)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py

## Requirements

Describe technologies, libraries, languages you are using (this can be updated in the future).

## Features

Describe the main features the application performs.
Filters out previously solved tasks and selects only unsolved ones.

Allows choosing problem tags (e.g., dp, graphs, math) for targeted practice.

Supports rating-range filtering (e.g., 1200–1700).

Randomly generates a contest of any desired size (e.g., 5–10 problems).

Produces direct links to all selected Codeforces problems.

Works for one user or multiple users (team practice).

## Git

Specify which branch will store the latest stable version of the application

## Success Criteria

Describe the criteria by which the success of the project can be determined
(this will be updated in the future)

* Criteria 1

https://cs-project-2025-hasan2oo6-production-74aa.up.railway.app/
