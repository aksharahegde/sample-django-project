# Django Jet Calm Compatibility Test Suite

This test suite provides comprehensive testing for Django Jet Calm compatibility with your Django application.

## Overview

The test suite includes multiple test classes that cover various aspects of Django Jet Calm integration:

### Test Classes

1. **DjangoJetCalmCompatibilityTests** - Main compatibility tests

   - Jet apps installation verification
   - Theme configuration testing
   - Admin interface accessibility
   - URL routing and accessibility
   - Model admin integration
   - Database compatibility
   - Template rendering
   - Security headers
   - Performance testing
   - Error handling

2. **JetThemeTests** - Theme-specific functionality

   - CSS and JavaScript loading
   - Theme configuration validation
   - Color format validation

3. **JetDashboardTests** - Dashboard functionality

   - URL structure testing
   - Widget configuration
   - Permission testing

4. **JetAdminIntegrationTests** - Admin integration

   - Change forms
   - Add forms
   - Delete confirmations
   - History views
   - Bulk actions

5. **JetStaticFilesTests** - Static files handling

   - File structure validation
   - Static files collection

6. **JetSecurityTests** - Security features

   - CSRF protection
   - XSS protection
   - SQL injection protection

7. **JetPerformanceTests** - Performance testing
   - Large dataset handling
   - Memory usage monitoring

## Running Tests

### Using the Test Runner Script

```bash
# Run all tests
python run_jet_tests.py

# Run with verbose output
python run_jet_tests.py --verbose

# Run with coverage reporting
python run_jet_tests.py --coverage
```

### Using the Simple Test Runner

If you're having issues with the main test runner, use the simple version:

```bash
# Simple test runner (no coverage, no complex dependencies)
python simple_test_runner.py
```

### Using Django's Test Command

```bash
# Run all Jet tests
python manage.py test polls.tests

# Run specific test class
python manage.py test polls.tests.DjangoJetCalmCompatibilityTests

# Run with verbose output
python manage.py test polls.tests --verbosity=2
```

### Using pytest (if installed)

```bash
# Run all tests
pytest polls/tests.py

# Run with coverage
pytest polls/tests.py --cov=polls
```

## Test Coverage

The test suite covers:

- ✅ Jet app installation and configuration
- ✅ Theme system functionality
- ✅ Dashboard widgets and modules
- ✅ Admin interface integration
- ✅ URL routing and accessibility
- ✅ Static files serving
- ✅ Database operations
- ✅ Security features (CSRF, XSS, SQL injection)
- ✅ Performance with large datasets
- ✅ Error handling
- ✅ Permission system
- ✅ Internationalization support

## Prerequisites

### Quick Setup

Run the setup script to install all required packages:

```bash
python setup_tests.py
```

### Manual Setup

Make sure you have the following installed:

```bash
pip install -r requirements.txt
```

Required packages:

- Django==5.1.12
- FeedParser
- psutil (for performance tests)
- coverage (for coverage reporting)

Optional packages:

- pytest (alternative test runner)

## Test Data

The tests create and manage their own test data:

- Test users (admin and regular users)
- Sample questions, choices, answers, and quiz records
- Test data is automatically cleaned up after each test

## Configuration

The tests use your existing Django settings with Jet configuration:

- `INSTALLED_APPS` includes 'jet' and 'jet.dashboard'
- `JET_THEMES` configuration is validated
- Static files configuration is tested

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure Django is properly installed and configured
2. **Static Files**: Ensure `python manage.py collectstatic` has been run
3. **Database**: Make sure migrations are applied
4. **Permissions**: Tests require superuser access for admin functionality

### Debug Mode

To run tests in debug mode:

```bash
python manage.py test polls.tests --verbosity=2 --debug-mode
```

## Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Include proper docstrings
3. Clean up test data in `tearDown()` methods
4. Use descriptive test method names
5. Add appropriate assertions

## Test Results Interpretation

- **✅ All tests passed**: Jet Calm is fully compatible
- **❌ Some tests failed**: Check specific failures for compatibility issues
- **⚠️ Warnings**: Non-critical issues that should be investigated

## Performance Benchmarks

The performance tests expect:

- Admin list views to load in < 5 seconds with 100 records
- Memory usage increase < 50MB during test operations
- Static files to be served efficiently

Adjust these thresholds based on your specific requirements.
