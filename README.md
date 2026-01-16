[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# Codeforces Practice Contest Generator

## Description

This project is a web application that helps users create **custom practice contests** using Codeforces problems.

The application connects to the **Codeforces API** and checks which problems each user has already solved. It then filters out solved problems and selects **new unsolved problems** based on the chosen difficulty (rating range) and problem topics (tags). This saves time and makes practice more focused and effective.

Multiple users can join the same contest for **group practice**. All participants solve the same set of problems, and the application can display a **standings table** based on real Codeforces submission data.

The project is built with **Flask**, uses a **database** to store contest data, runs inside **Docker**, includes **CI/CD with GitHub Actions**, and is deployed online using **Railway**.
Creating practice contests for students who are training for competitive programming or exams usually requires manually checking which problems they have already solved. This process is time-consuming and error-prone, especially for groups of students. This project solves that problem by automatically checking solved problems using the Codeforces API and selecting only new unsolved tasks. As a result, teachers, coaches, and students can quickly create fair and useful practice contests without manual work.


## Setup

### Run locally (Python)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
### Open in browser:
```bash
http://127.0.0.1:8000
```

### Run with Docker
```bash
docker build -t cf-contest .
docker run --rm -p 8000:8000 cf-contest
```


## Requirements

The project is developed using **Python** as the main programming language.  
The web server is built with the **Flask** framework.  
The **requests** library is used to communicate with the Codeforces API.  
**Jinja2** is used for rendering HTML templates.  
An **SQLite** database is used to store contest and application data.  
The application is containerized using **Docker**.  
**GitHub Actions** is used for CI/CD to automatically build and test the project.  
The project is deployed online using **Railway**.





## Features
Automatically generates Codeforces-style practice contests

Uses Codeforces API to check solved problems for each user

Filters out solved problems and selects only unsolved ones

Filters problems by rating range (difficulty)

Filters problems by tags (topics like dp, graphs, math)

Supports multiple users in one contest (group practice)

Displays contest standings using Codeforces submissions

Provides direct links to all selected Codeforces problems

Useful for competitive programming training and exam preparation

Saves time compared to manual problem selection

## Git

Specify which branch will store the latest stable version of the application

## Success Criteria
The project is considered successful if the application runs correctly both locally and inside Docker without errors.

Users must be able to create practice contests and receive valid Codeforces problem sets based on the selected difficulty and tags.

Previously solved problems should be correctly excluded for all users.

Contest standings should be generated and updated using real submission data from Codeforces.

The GitHub Actions CI pipeline must pass successfully, confirming that the application builds and runs as expected.

The deployed application on Railway should be accessible and working correctly.


## Deployed Application
https://cs-project-2025-hasan2oo6-production-74aa.up.railway.app/
