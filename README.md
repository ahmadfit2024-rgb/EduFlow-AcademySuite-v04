# EduFlow-AcademySuite - The Integrated Learning Management Ecosystem

## Overview

EduFlow-AcademySuite is a comprehensive, web-based ecosystem designed by **Fit4Future** to empower educational institutions and training centers. It provides a sophisticated, centralized solution to design, manage, and deliver exceptional learning experiences, from single workshops to complete professional diplomas.

This project replaces fragmented manual processes with an intelligent, automated, and interactive platform. It allows administrators, supervisors, instructors, and students to focus on what matters most: impactful education and skill development. Built on a robust and scalable architecture, the system provides distinct role-based access, tailored dashboards, and a full suite of features covering the entire educational lifecycle.

## Tech Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| Language | **Python 3.11+** | Modern, powerful, and possesses a massive ecosystem for web development, data analysis, and AI. |
| Backend Framework | **Django 5.0+** | A high-level framework that enables rapid development of secure, maintainable, and scalable web applications. |
| API Framework | **Django REST Framework** | The gold standard for building powerful and flexible RESTful APIs in Django, enabling seamless integration. |
| Database | **MongoDB 7.0+** | A highly flexible NoSQL database, perfect for handling the complex and nested structures of educational content like courses, lessons, and quizzes. |
| Frontend | **Bootstrap 5 & HTMX** | A modern combination for creating responsive, professional UIs with dynamic, high-performance interactions without the complexity of a full JavaScript framework. |
| Automation | **n8n.io (via Webhooks)** | An open-source workflow automation tool used to connect EduFlow-AcademySuite with external services like email, SMS, and communication platforms. |
| AI Assistant | **OpenRouter API** | Provides flexible access to various Large Language Models to power the platform's intelligent student assistant. |

## Project Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd EduFlow-AcademySuite
    ```

2.  **Environment Variables:**
    -   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    -   Populate the `.env` file with your specific credentials for the database, Django `SECRET_KEY`, and API keys. This file is intentionally not tracked by Git.

3.  **Setup Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Database Setup:**
    -   Ensure you have a MongoDB instance running.
    -   The database and collections will be created automatically by Django and `djongo` on the first run.

6.  **Run Initial Migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## Key Features

-   **Role-Based Dashboards:** Customized, intuitive views for Admins, Supervisors, Instructors, Students, and Third-Party Clients.
-   **Interactive Learning Path Builder:** A powerful drag-and-drop interface for designing complete diplomas and programs.
-   **Rich Content Management:** Support for video, PDF, text, and interactive quizzes as lesson content.
-   **Student Progress Tracking:** Detailed analytics on student performance, completion rates, and engagement.
-   **Intelligent Reporting Engine:** Generate and export detailed reports in PDF and Excel formats.
-   **Integrated AI Assistant:** Provides instant, context-aware support to students.
-   **Webhook Integration:** Seamless automation of workflows via n8n for notifications, onboarding, and more.