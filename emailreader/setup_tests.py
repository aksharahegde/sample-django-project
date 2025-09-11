#!/usr/bin/env python
"""
Setup script for Django Jet Calm compatibility tests.

This script installs the required packages and sets up the test environment.
"""

import subprocess
import sys
import os


def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Django Jet Calm Test Environment")
    print("=" * 50)
    
    # Required packages
    packages = [
        'Django==5.1.12',
        'feedparser',
        'psutil',
        'coverage'
    ]
    
    print("📦 Installing required packages...")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"   ✅ Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("\n🎉 All packages installed successfully!")
        print("\nYou can now run the tests with:")
        print("   python run_jet_tests.py")
        print("   python run_jet_tests.py --verbose")
        print("   python run_jet_tests.py --coverage")
    else:
        print(f"\n⚠️  {len(packages) - success_count} packages failed to install.")
        print("Please check the error messages above and install manually if needed.")
    
    # Test Django import
    print("\n🧪 Testing Django installation...")
    try:
        import django
        print(f"✅ Django {django.get_version()} is available")
    except ImportError:
        print("❌ Django import failed. Please check your installation.")
        return False
    
    # Test Jet import
    try:
        import jet
        print("✅ Django Jet is available")
    except ImportError:
        print("❌ Django Jet import failed. Please check your installation.")
        return False
    
    print("\n🎯 Test environment is ready!")
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
