#!/usr/bin/env python
"""
Simple test runner for Django Jet Calm compatibility tests.

This is a simplified version that works without complex dependencies.
"""

import os
import sys
import subprocess


def run_simple_tests():
    """Run tests using Django's manage.py command"""
    print("🚀 Django Jet Calm Compatibility Test Suite")
    print("=" * 50)
    
    # Check if manage.py exists
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the Django project directory.")
        return False
    
    # Test patterns to run
    test_classes = [
        'polls.tests.DjangoJetCalmCompatibilityTests',
        'polls.tests.JetThemeTests', 
        'polls.tests.JetDashboardTests',
        'polls.tests.JetAdminIntegrationTests',
        'polls.tests.JetStaticFilesTests',
        'polls.tests.JetSecurityTests',
        'polls.tests.JetPerformanceTests',
    ]
    
    print(f"🧪 Running {len(test_classes)} test classes...")
    print()
    
    all_passed = True
    
    for test_class in test_classes:
        print(f"Running {test_class}...")
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'test', test_class, '--verbosity=1'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"  ✅ {test_class} - PASSED")
            else:
                print(f"  ❌ {test_class} - FAILED")
                print(f"     Error: {result.stderr}")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"  ⏰ {test_class} - TIMEOUT")
            all_passed = False
        except Exception as e:
            print(f"  ❌ {test_class} - ERROR: {e}")
            all_passed = False
        
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_passed


def main():
    """Main function"""
    success = run_simple_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
