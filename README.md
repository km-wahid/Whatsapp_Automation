# WhatsApp Bulk Automation System

## Overview

The **WhatsApp Bulk Automation System** is a Django-based web application designed to streamline sending messages on WhatsApp at scale. It enables users to send messages to multiple contacts efficiently while maintaining session management and personalized messaging. The system leverages **Selenium automation, Chrome profiles, Celery tasks, and WebSocket real-time updates** for seamless operation.

This project is ideal for businesses, marketing teams, and developers who need automated WhatsApp messaging while preserving user session integrity.

---

## Features

* **User Authentication:** Secure login for multiple users.
* **WhatsApp QR Login:** Each user can log in using a unique QR code.
* **Chrome Profile Management:** Automatically creates and reuses unique Chrome profiles per WhatsApp session.
* **CSV Upload:** Bulk import of contacts and messages.
* **Message Templates:** Create reusable message templates with dynamic placeholders.
* **Campaign Management:** Schedule and send messages to multiple contacts in bulk.
* **Automation via Celery:** Background task processing for sending messages without blocking the server.
* **Selenium Integration:** Automates WhatsApp Web for message delivery.
* **WebSocket Real-Time Updates:** Display real-time QR code scanning status and message sending progress.
* **Retry Logic:** Automatic retries for failed message deliveries.
* **Admin Dashboard:** Manage users, sessions, campaigns, and logs.
* **Logs & Reporting:** View detailed logs for message delivery and session activity.
* **Docker Support:** Easily deploy with Docker for a consistent environment.

---

## Technology Stack

* **Backend:** Django, Django Channels, Celery
* **Frontend:** HTML, Tailwind CSS, Bootstrap, JavaScript
* **Automation:** Selenium WebDriver
* **Database:** PostgreSQL (preferred), MySQL, SQLite
* **Task Queue:** Celery with Redis or RabbitMQ
* **Containerization:** Docker
* **WebSocket:** Real-time QR code and progress updates

---

## System Requirements

* Python 3.10+
* Django 4.x
* Node.js (for WebSocket server if used separately)
* Redis or RabbitMQ for Celery
* Chrome Browser with Selenium WebDriver
* Docker (optional, for containerized deployment)

---

## Usage Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/whatsapp-bulk-automation.git
cd whatsapp-bulk-automation
```

### 2. Setup environment

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Configure settings

* Add database credentials in `settings.py`
* Configure Redis or RabbitMQ for Celery tasks
* Set Chrome WebDriver path if needed

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start services

```bash
# Start Django server
python manage.py runserver

# Start Celery worker
celery -A project_name worker --loglevel=info
```

### 6. Access application

Open `http://localhost:8000` in your browser and log in to start sending bulk messages.

---

## Drawbacks / Limitations

* **WhatsApp Web Restrictions:** May block accounts if too many messages are sent in a short period.
* **Selenium Dependence:** Relies on browser automation, which can break if WhatsApp Web updates.
* **Performance:** Large campaigns can be slow if many contacts are processed in a single batch.
* **Session Persistence:** Chrome profiles must be properly maintained; corrupted profiles may require re-login.
* **Error Handling:** Some message delivery failures may not be captured immediately.
* **Legal Considerations:** Bulk messaging may violate WhatsApp terms if used for spam.
* **Scalability:** High-scale deployments may require multiple servers and distributed task queues.

---

## Project Structure

```
whatsapp-bulk-automation/
│
├─ bulk_app/                 # Django app with views, models, templates
├─ celery_tasks/             # Celery tasks for message sending
├─ static/                   # Frontend static files (CSS, JS)
├─ templates/                # HTML templates for pages
├─ chromedriver/             # ChromeDriver executable
├─ manage.py                 # Django entry point
├─ requirements.txt          # Python dependencies
└─ README.md                 # Project documentation
```

---

## Future Enhancements

* Multi-account support for massive campaigns
* Integration with WhatsApp Business API for official automation
* Enhanced reporting dashboards with analytics
* Scheduled campaigns and cron jobs
* AI-based message personalization

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Implement your feature or fix.
4. Commit changes (`git commit -m "Add feature"`).
5. Push to your branch (`git push origin feature-name`).
6. Open a Pull Request.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contact

**Author:** Khalid Muhammad
**Email:** (khalidmuhammad.official@gmail.com)
**GitHub:** (https://github.com/km-wahid)
