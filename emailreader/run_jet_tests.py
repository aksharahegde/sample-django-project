#!/usr/bin/env python
"""
Test runner script for Django Jet Calm compatibility tests.

This script provides an easy way to run all Jet compatibility tests
with proper setup and reporting.

Usage:
    python run_jet_tests.py
    python run_jet_tests.py --verbose
    python run_jet_tests.py --coverage
    python run_jet_tests.py --help
"""

import os
import sys
import argparse
import subprocess


def check_django_environment():
    """Check if Django environment is properly set up"""
    try:
        import django
        from django.conf import settings
        return True
    except ImportError:
        return False


def setup_django():
    """Setup Django environment for testing"""
    try:
        import django
        from django.conf import settings
        from django.test.utils import get_runner
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailreader.settings')
        django.setup()
        return True
    except ImportError as e:
        print(f"❌ Django import error: {e}")
        print("Please make sure Django is installed and you're in the correct virtual environment.")
        return False
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False


def run_tests_with_django(verbosity=1):
    """Run Django Jet Calm compatibility tests using Django's test runner"""
    try:
        import django
        from django.conf import settings
        from django.test.utils import get_runner
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        
        # Test patterns to run
        test_patterns = [
            'polls.tests.DjangoJetCalmCompatibilityTests',
            'polls.tests.JetThemeTests',
            'polls.tests.JetDashboardTests',
            'polls.tests.JetAdminIntegrationTests',
            'polls.tests.JetStaticFilesTests',
            'polls.tests.JetSecurityTests',
            'polls.tests.JetPerformanceTests',
        ]
        
        print("=" * 60)
        print("Django Jet Calm Compatibility Test Suite")
        print("=" * 60)
        print(f"Running {len(test_patterns)} test classes...")
        print()
        
        failures = test_runner.run_tests(test_patterns, verbosity=verbosity)
        
        if failures:
            print(f"\n❌ {failures} test(s) failed!")
            return False
        else:
            print("\n✅ All tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_tests_with_manage_py(verbosity=1):
    """Run tests using Django's manage.py command"""
    print("=" * 60)
    print("Django Jet Calm Compatibility Test Suite")
    print("=" * 60)
    print("Running tests using manage.py...")
    print()
    
    try:
        # Use manage.py to run tests
        cmd = ['python', 'manage.py', 'test', 'polls.tests']
        if verbosity > 1:
            cmd.extend(['--verbosity', str(verbosity)])
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests with manage.py: {e}")
        return False


def run_tests(verbosity=1, coverage=False):
    """Run Django Jet Calm compatibility tests"""
    # First try to run with Django directly
    if check_django_environment():
        if setup_django():
            return run_tests_with_django(verbosity)
    
    # Fallback to manage.py
    print("⚠️  Django environment not available, using manage.py...")
    return run_tests_with_manage_py(verbosity)


def run_coverage_tests():
    """Run tests with coverage reporting"""
    try:
        import coverage
    except ImportError:
        print("❌ Coverage module not installed.")
        print("📦 Installing coverage...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'coverage'])
            print("✅ Coverage installed successfully!")
            import coverage
        except Exception as e:
            print(f"❌ Failed to install coverage: {e}")
            print("Please install manually with: pip install coverage")
            return False
    
    # Start coverage
    cov = coverage.Coverage()
    cov.start()
    
    # Run tests
    success = run_tests(verbosity=2)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\n" + "=" * 60)
    print("Coverage Report")
    print("=" * 60)
    cov.report()
    
    # Generate HTML coverage report
    try:
        cov.html_report(directory='htmlcov')
        print(f"\n📊 HTML coverage report generated in 'htmlcov' directory")
    except Exception as e:
        print(f"⚠️  Could not generate HTML report: {e}")
    
    return success


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run Django Jet Calm compatibility tests')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Run tests in verbose mode')
    parser.add_argument('--coverage', '-c', action='store_true',
                       help='Run tests with coverage reporting')
    
    args = parser.parse_args()
    
    verbosity = 2 if args.verbose else 1
    
    if args.coverage:
        success = run_coverage_tests()
    else:
        success = run_tests(verbosity=verbosity)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
