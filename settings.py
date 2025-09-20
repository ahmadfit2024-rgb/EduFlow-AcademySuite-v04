# ===============================================
# EduFlow-AcademySuite Environment Variables
# ===============================================
# NOTE: This file should NOT be committed to version control (e.g., Git).

# --- Django Core Settings ---
# WARNING: Set DEBUG=False in production for security!
DEBUG=True
# Generate a new strong key for production: https://djecrety.ir/
SECRET_KEY='django-insecure-a-very-strong-and-random-secret-key-for-eduflow'
ALLOWED_HOSTS=127.0.0.1,localhost

# --- Database Settings (MongoDB) ---
DB_NAME=eduflow_db
DB_HOST=localhost
DB_PORT=27017
# DB_USER=your_mongo_user       # Uncomment if MongoDB authentication is enabled
# DB_PASSWORD=your_mongo_password # Uncomment if MongoDB authentication is enabled

# --- Redis & Celery Settings ---
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=${REDIS_URL}  # Celery can use the same Redis URL

# --- Third-Party Service URLs & Keys ---
# Fill these with your actual n8n webhook URLs
N8N_ENROLLMENT_CREATED_WEBHOOK_URL="http://localhost:5678/webhook/enrollment-created"
N8N_QUESTION_POSTED_WEBHOOK_URL="http://localhost:5678/webhook/question-posted" # <-- ADDED LINE

# Replace with your actual key from OpenRouter.ai
OPENROUTER_API_KEY="sk-or-v1-your-secret-api-key-from-openrouter-here"

# --- Email Settings (Example for Gmail) ---
# For production, use a dedicated email service like SendGrid or Mailgun.
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-google-app-password" # Use an App Password, not your main password