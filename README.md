# Journeo - Digital Travel Journal Platform

## 🌟 Overview

Journeo is a responsive web application designed to help travelers plan and document their activities at MGVC vacation club. Built with Django and Bootstrap 5, it offers a seamless experience across all devices, allowing users to organize activities, track costs, and preserve travel memories.

## ✨ Features

### User Features
- **Activity Planning**
  - Browse available activities by domain
  - Schedule activities with specific dates and times
  - Track activity costs and duration
  - Add personal memory notes to activities

### Admin Features
- **Domain Management**
  - Create and manage activity domains
  - Track activities within each domain
  - Monitor domain utilization

- **Activity Management**
  - Add/Edit/Delete activities
  - Set activity capacity limits
  - Define activity costs and duration
  - Assign activities to domains

### Core Functionality
- **Cost Management**
  - Automatic cost calculation
  - Budget tracking per travel program
  - Cost summaries and reports

- **Responsive Design**
  - Mobile-first approach
  - Touch-friendly interfaces
  - Adaptive layouts for all screen sizes
  - Responsive tables and forms

- **Reporting**
  - PDF report generation
  - Activity statistics
  - Cost summaries
  - Travel program details

## 🛠️ Technical Stack

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5
- **Database**: MySQL
- **PDF Generation**: ReportLab
- **Icons**: Font Awesome
- **Responsive Design**: Custom CSS with Media Queries

## 📋 Prerequisites

- Python 3.8+
- MySQL
- pip (Python package manager)

## 🚀 Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/journeo.git
cd journeo
\`\`\`

2. Create and activate a virtual environment:
\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Configure the database in settings.py:
\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'carnet_voyage',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
\`\`\`

5. Run migrations:
\`\`\`bash
python manage.py migrate
\`\`\`

6. Create a superuser:
\`\`\`bash
python manage.py createsuperuser
\`\`\`

7. Run the development server:
\`\`\`bash
python manage.py runserver
\`\`\`

## 📱 Usage

### For Travelers
1. Register an account
2. Create a new travel program
3. Browse and add activities to your program
4. Schedule activities with dates and times
5. Add memory notes to activities
6. Generate PDF reports of your travel program

### For Administrators
1. Access the admin dashboard
2. Manage activity domains
3. Create and edit activities
4. Monitor user programs
5. Generate reports

## 🔒 Security

- User authentication and authorization
- Form validation and sanitization
- CSRF protection
- Secure password handling

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## 👥 Authors

Achraf MALKI & Bilal ESSAFRIOUI

## 🙏 Acknowledgments

- MGVC Vacation Club for the project requirements
- Django community for the excellent framework
- Bootstrap team for the responsive design framework
