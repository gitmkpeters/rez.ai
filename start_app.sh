#!/bin/bash

echo "🚀 Resume Tailor - Quick Start"
echo "=============================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if requirements are installed
echo "🔍 Checking dependencies..."
python -c "import flask, openai, reportlab" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing requirements..."
    pip install -r requirements.txt
fi

# Start the application
echo "🌐 Starting application..."
echo "📍 Access at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""

python run_simple_fixed.py
