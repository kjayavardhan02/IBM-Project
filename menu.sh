#!/bin/bash

while true; do
    echo "=============================="
    echo "   ⚡ VM Energy Project Menu   "
    echo "=============================="
    echo "1. Run Scripts"
    echo "2. Run Dashboard"
    echo "3. Exit"
    echo "------------------------------"
    read -p "Enter your choice [1-3]: " main_choice

    case $main_choice in
        1)
            echo "------ Scripts ------"
            echo "1. Compare Results"
            echo "2. Monitor Usage"
            echo "3. Optimization"
            echo "4. Generate Full Report"
            echo "5. Back to Main Menu"
            read -p "Choose script [1-5]: " script_choice
            
            case $script_choice in
                1) echo "▶ Running compare_results.py..."
                   python3 compare_results_updated.py ;;
                2) echo "▶ Running monitor.py..."
                   python3 monitor_updated.py ;;
                3) echo "▶ Running optimization.py..."
                   sudo python3 optimization_updated.py ;;
                4) echo "📄 Generating full report..."
                   echo "Step 1️⃣: Monitoring system usage (before optimization)..."
                   python3 monitor_updated.py
                   echo "Step 2️⃣: Running optimization process..."
                   sudo python3 optimization_updated.py
                   echo "Step 3️⃣: Comparing results and generating PDF report..."
                   python3 compare_results_updated.py
                   echo "✅ Full report generated successfully." ;;
                5) echo "↩ Returning to main menu..." ;;
                *) echo "❌ Invalid option!" ;;
            esac
            ;;
        2)
            echo "▶ Running dashboard.py..."
            python3 dashboard.py
            ;;
        3)
            echo "👋 Exiting menu. Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice, please try again."
            ;;
    esac
    echo "" # spacing
done
