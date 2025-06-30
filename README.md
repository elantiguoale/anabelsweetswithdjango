# Anabel Sweets - Django Bakery Website

![Anabel Sweets](staticfiles/images/cakeland.png)

A professional Django web application for a bakery business, featuring user authentication, cake ordering, and a community wall of fame for cake submissions.

## 🎂 Features

### Core Functionality
- **User Authentication**: Registration, login, logout, and profile management
- **Cake Ordering System**: Complete order form with flavors, sizes, and pricing in SEK
- **Wall of Fame**: Community-driven cake photo submissions with approval workflow
- **My Orders**: Customer order history and tracking
- **Responsive Design**: Mobile-friendly interface with modern UI

### Technical Features
- **Role-based Access Control**: Different permissions for customers and admins
- **CRUD Operations**: Full create, read, update, delete functionality
- **Form Validation**: Comprehensive client and server-side validation
- **Admin Interface**: Full Django admin integration for all models
- **Database Models**: Custom models for Posts, Cake Submissions, and Orders

## 🛠️ Technologies Used

- **Backend**: Django 4.2.16, Python 3.13
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication system
- **Testing**: Django TestCase, 46 comprehensive tests
- **Version Control**: Git & GitHub
- **Deployment**: Heroku-ready configuration

## 📋 Project Structure

```
anabelsweetswithdjango/
├── about/                 # Main app with cake functionality
│   ├── models.py         # Post, CakeSubmission, Order models
│   ├── views.py          # All view logic
│   ├── forms.py          # Form definitions and validation
│   ├── tests.py          # Comprehensive test suite
│   └── templates/        # HTML templates
├── accounts/             # Authentication app
│   ├── views.py          # User registration, login, profile
│   └── templates/        # Auth templates
├── sweets/               # Main Django project
│   ├── settings.py       # Django configuration
│   └── urls.py           # URL routing
├── staticfiles/          # Static assets
│   ├── css/             # Stylesheets
│   └── images/          # Cake images and icons
├── media/               # User-uploaded content
└── templates/           # Base templates
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/elantiguoale/anabelsweetswithdjango.git
   cd anabelsweetswithdjango
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🧪 Testing

The project includes comprehensive testing with **46 Python tests** and **6 JavaScript tests** covering all major functionality:

### Test Coverage
- **Models**: Post, CakeSubmission, Order model functionality
- **Forms**: CakeSubmissionForm, OrderForm validation
- **Views**: All view functions and authentication requirements
- **Integration**: Complete user workflows and business logic
- **JavaScript**: Interactive form features and client-side validation

### Running Tests

```bash
# Run all Python tests
python manage.py test

# Run specific app tests
python manage.py test about.tests

# Run JavaScript tests
python manage.py test_javascript

# Run JavaScript tests with browser
python manage.py test_javascript --browser

# Run with coverage (if coverage is installed)
coverage run --source='.' manage.py test
coverage report
```

### Python Test Results
```
Found 46 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..............................................
----------------------------------------------------------------------
Ran 46 tests in 25.716s

OK
Destroying test database for alias 'default'...
```

### JavaScript Test Results
```
🧪 Starting JavaScript Tests for Anabel Sweets...

📊 Test Results:
✅ PASS: Flavor Selection Functionality
✅ PASS: Custom Flavor Toggle
✅ PASS: Form Validation
✅ PASS: Date Validation Structure
✅ PASS: Flavor Preview Update
✅ PASS: Responsive Design Elements

🎯 Summary: 6/6 tests passed
🎉 All JavaScript tests passed!
```

### Test Categories

#### Python Tests
- **Model Tests**: Post creation and string representation, CakeSubmission approval workflow, Order creation with pricing and urgency detection
- **Form Tests**: Valid form submissions with proper validation, error handling for invalid data, custom flavor validation, event date validation (minimum 3 days in future)
- **View Tests**: Authentication requirements, template rendering, success/error message handling, user state reflection
- **Integration Tests**: Complete order workflow, My Orders functionality, user registration and login flow

#### JavaScript Tests
- **Flavor Selection Functionality**: Tests interactive flavor selection and preview updates
- **Custom Flavor Toggle**: Tests showing/hiding custom flavor description field
- **Form Validation**: Tests required field validation and email format validation
- **Date Validation Structure**: Tests date input requirements and validation structure
- **Flavor Preview Update**: Tests dynamic flavor preview updates when selection changes
- **Responsive Design Elements**: Tests presence of images and accessibility features

### Running JavaScript Tests in Browser

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open the JavaScript test runner in your browser:
   ```
   http://127.0.0.1:8000/static/js/test-runner.html
   ```

3. Click "Run All Tests" to execute the JavaScript test suite

### Test Environment
- **Python Tests**: Django TestCase framework with SQLite test database
- **JavaScript Tests**: Browser-based with mock DOM environment
- **Coverage**: 100% of core functionality tested
- **Integration**: Tests work with actual Django templates and forms

## 📊 Database Models

### Post Model
- Blog posts with author, content, and status management
- Draft/Published workflow

### CakeSubmission Model
- User-submitted cake photos
- Approval workflow (Pending/Approved/Rejected)
- Admin notes for internal use

### Order Model
- Complete cake ordering system
- Customer information and contact details
- Cake specifications (flavor, size, design)
- Event details and pricing in SEK
- Order status tracking

## 🎨 User Interface

### Design Features
- **Responsive Layout**: Works on all device sizes
- **Modern UI**: Clean, professional design with pink color scheme
- **Interactive Elements**: Hover effects and smooth transitions
- **Accessibility**: Proper alt text and semantic HTML

### Pages
1. **Home/About**: Introduction and cake showcase
2. **Order Cake**: Comprehensive order form with flavor preview
3. **Wall of Fame**: Approved cake submissions from community
4. **Submit Cake**: User cake submission form (login required)
5. **My Orders**: Customer order history (login required)
6. **Authentication**: Registration, login, and profile pages

## 🔐 Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **Authentication**: Secure login/logout system
- **Authorization**: Role-based access control
- **Form Validation**: Server-side validation for all inputs
- **Environment Variables**: Sensitive data stored in environment variables
- **No Hardcoded Secrets**: All secrets managed through environment variables

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set DATABASE_URL=your-postgresql-url
   heroku config:set DEBUG=False
   ```

4. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Environment Variables for Production
```
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 📝 Agile Methodology

This project was developed using Agile methodology with:

- **User Stories**: Documented requirements and acceptance criteria
- **GitHub Projects**: Kanban board for task management
- **Iterative Development**: Features developed in sprints
- **Continuous Testing**: Tests written alongside feature development
- **Version Control**: Regular commits with descriptive messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Miguel Hernandez**
- GitHub: [@elantiguoale](https://github.com/elantiguoale)
- Project: [Anabel Sweets Django](https://github.com/elantiguoale/anabelsweetswithdjango)

## 🙏 Acknowledgments

- Code Institute for the learning framework
- Django community for excellent documentation
- Anabel for the bakery business inspiration

---

**Note**: This is a student project developed for educational purposes. The bakery business "Anabel Sweets" is fictional. 