Author: Jai Rathinavel
Contest Submission: Aug 2025 Fabric Notebook Contest

[LinkedIn]([https://www.linkedin.com/in/jai-rathinavel/])

GitHub

📖 Overview
This repository contains a Microsoft Fabric notebook that launches an interactive user interface to refresh semantic models (formerly Power BI datasets) directly within the notebook environment. It leverages the semantic-link (sempy) and semantic-link-labs libraries to discover models across workspaces, manage refresh operations, and visualize the refresh trace logs.

The main goal is to provide a user-friendly "app" experience for data professionals to perform and monitor targeted refreshes of tables and partitions without leaving their Fabric workspace.

✨ Features
Interactive UI: A simple application interface built with ipywidgets for an intuitive user experience.

Workspace & Model Discovery: Automatically fetches all accessible semantic models, tables, and partitions.

Data Caching: Ability to save the model metadata to a Lakehouse table to speed up subsequent runs and avoid redundant API calls.

Granular Refreshes: Select specific workspaces, models, tables, and even individual partitions to refresh.

Advanced Options: Configure advanced settings for each refresh operation, such as:

Refresh Type (Full, DataOnly, Calculate, etc.)

Retry Count

Max Parallelism

Commit Mode

Apply Refresh Policy

Refresh Monitoring: Visualizes the SSAS trace output as a Gantt chart upon completion, showing the duration of each step.

📷 Screenshot
Here is a snapshot of the Notebook Application in action:

🔧 Prerequisites
A Microsoft Fabric Workspace with a Lakehouse.

The notebook must be attached to a Lakehouse to function correctly.

Appropriate permissions for the user to list workspaces and refresh the selected semantic models.
