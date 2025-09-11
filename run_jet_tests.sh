#!/bin/bash
# Simple shell script to run Django Jet Calm compatibility tests
# This script activates the virtual environment and runs the tests

echo "🚀 Django Jet Calm Compatibility Test Runner"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the Django project root directory."
    exit 1
fi

# Check if virtual environment exists
if [ -d "env" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
elif [ -d "emailreader/env" ]; then
    echo "📦 Activating virtual environment..."
    source emailreader/env/bin/activate
else
    echo "⚠️  Virtual environment not found. Make sure Django is installed."
fi

# Check if Django is available
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not found. Please install Django and activate your virtual environment."
    echo "   Try: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Django environment ready!"
echo ""

# Run the tests
echo "🧪 Running Django Jet Calm compatibility tests..."
echo ""

# Try the custom test runner first
if [ -f "run_jet_tests.py" ]; then
    echo "Using custom test runner..."
    python run_jet_tests.py "$@"
elif [ -f "emailreader/run_jet_tests.py" ]; then
    echo "Using custom test runner..."
    cd emailreader
    python run_jet_tests.py "$@"
else
    echo "Using Django's manage.py test command..."
    python manage.py test polls.tests --verbosity=2
fi

echo ""
echo "🏁 Test run completed!"
