#!/bin/bash

# 🚀 MASSIVE MARRAKESH BUSINESS SEARCH - Quick Start (Linux/Mac)
# This will find THOUSANDS of business opportunities in Marrakesh!
# Results saved to results/ folder in JSON format

echo "🚀 MASSIVE MARRAKESH BUSINESS SEARCH - Quick Start"
echo ""
echo "This will find THOUSANDS of business opportunities in Marrakesh!"
echo "Results saved to results/ folder in JSON format"
echo ""

while true; do
    echo "================================================"
    echo "Choose your search size:"
    echo ""
    echo "1. Quick Test        (1,000 businesses - 2 minutes)"
    echo "2. Standard Search   (50,000+ businesses - 1 hour)"
    echo "3. MEGA Search       (200,000+ businesses - 4 hours)"
    echo "4. Setup Automation  (Weekly/Monthly searches)"
    echo "5. Exit"
    echo ""
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            echo ""
            echo "🧪 Running Quick Test Search..."
            echo "Expected: ~1,000 businesses in 2-5 minutes"
            python3 quick_marrakesh_search.py --test
            ;;
        2)
            echo ""
            echo "📊 Running Standard Search..."
            echo "Expected: ~50,000+ businesses in 30-60 minutes"
            python3 quick_marrakesh_search.py --standard
            ;;
        3)
            echo ""
            echo "🚀 Running MEGA Search..."
            echo "Expected: ~200,000+ businesses in 2-4 hours"
            echo "This is a MASSIVE search - make sure you have time!"
            read -p "Continue with MEGA search? (y/n): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                python3 quick_marrakesh_search.py --mega
            else
                echo "MEGA search cancelled."
                continue
            fi
            ;;
        4)
            echo ""
            echo "🔄 Setting up Automated Searches..."
            python3 quick_marrakesh_search.py --schedule
            echo ""
            echo "To start the scheduler:"
            echo "1. pip install schedule"
            echo "2. python3 simple_scheduler.py"
            continue
            ;;
        5)
            echo ""
            echo "Thanks for using Massive Marrakesh Business Search!"
            echo "Your business opportunities await in the results/ folder 🚀"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            continue
            ;;
    esac
    
    echo ""
    echo "✅ Search completed!"
    echo "📁 Check the 'results/' folder for your data"
    echo "💡 Look for businesses with 'opportunity_level': 'EXCELLENT'"
    echo ""
    read -p "Press Enter to continue..."
done
