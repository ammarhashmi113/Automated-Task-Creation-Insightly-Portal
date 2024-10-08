# Automated Task Creation for Insightly Portal

## Overview

The **Automated Task Creation for Insightly Portal** project automates the process of creating tasks within the Insightly CRM portal using Selenium. This application improves efficiency by reducing manual input and streamlining task management.

## Features

- Automates task creation in the Insightly portal.
- Utilizes environment variables for secure credential management.
- Captures screenshots during the automation process for verification.
- Logs automation steps for easy bug tracking.

## Technologies Used

- [Python](https://www.python.org/) - Programming language
- [Selenium](https://www.selenium.dev/) - Web automation framework
- [Environment Variables](https://12factor.net/config) - For managing sensitive information

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ammarhashmi113/Automated-Task-Creation-Insightly-Portal.git
   cd Automated-Task-Creation-Insightly-Portal
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Set up your environment variables in a `.env` file.

## Usage

1. Configure the necessary environment variables in the `.env` file.
2. Run the script:

   ```bash
   python main.py
   ```

