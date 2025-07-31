#!/bin/bash

# 🎨 Colors
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
CYAN='\e[36m'
NC='\e[0m' # No color

# Center horizontally
center_text() {
    local text="$1"
    local width=$(tput cols)
    local clean_text=$(echo -e "$text" | sed 's/\x1B\[[0-9;]*[A-Za-z]//g')
    local padding=$(( (width - ${#clean_text}) / 2 ))
    printf "%*s%s\n" $padding "" "$(echo -e "$text")"
}

while true; do
    clear
    echo ""
    center_text "${CYAN}==============================${NC}"
    center_text "⚡ ${GREEN}VM Energy Project Menu${NC}"
    center_text "${CYAN}==============================${NC}"
    echo ""
    center_text "1. Run Scripts"
    center_text "2. Run Dashboard"
    center_text "3. Exit"
    echo ""
    center_text "${CYAN}------------------------------${NC}"
    echo ""
    read -p "👉 Enter your choice [1-3]: " main_choice

    case $main_choice in
        1)
            clear
            echo ""
            center_text "${CYAN}------ Scripts ------${NC}"
            echo ""
            center_text "1. Compare Results"
            center_text "2. Monitor Usage"
            center_text "3. Optimization"
            center_text "4. Generate Full Report"
            center_text "5. Back to Main Menu"
            echo ""
            read -p "👉 Choose script [1-5]: " script_choice
            
            case $script_choice in
                1) center_text "${YELLOW}▶ Running compare_results.py...${NC}"
                   python3 compare_results.py ;;
                2) center_text "${YELLOW}▶ Running monitor.py...${NC}"
                   python3 monitor.py ;;
                3) center_text "${YELLOW}▶ Running optimization.py (sudo required)...${NC}"
                   sudo python3 optimization.py ;;
                4) center_text "${CYAN}📄 Generating full report...${NC}"
                   if [[ -f "usage_before.csv" && -f "usage_after.csv" ]]; then
                       center_text "${GREEN}✅ Found existing usage files. Skipping monitoring & optimization...${NC}"
                   else
                       center_text "${RED}⚠️  Files not found. Running full process again...${NC}"
                       center_text "${YELLOW}Monitoring system usage (before optimization)...${NC}"
                       python3 monitor.py
                       center_text "${YELLOW}Running optimization process...${NC}"
                       sudo python3 optimization.py
                   fi
                   center_text "${YELLOW}Comparing results and generating PDF report...${NC}"
                   python3 compare_results.py
                   center_text "${GREEN}✅ Full report generated successfully.${NC}" ;;
                5) center_text "${CYAN}↩ Returning to main menu...${NC}" ;;
                *) center_text "${RED}❌ Invalid option!${NC}" ;;
            esac
            ;;
        2)
            center_text "${YELLOW}▶ Running dashboard.py...${NC}"
            python3 dashboard.py
            ;;
        3)
            center_text "${GREEN}👋 Exiting menu. Goodbye!${NC}"
            exit 0
            ;;
        *)
            center_text "${RED}❌ Invalid choice, please try again.${NC}"
            ;;
    esac

    echo ""
    read -p "🔁 Press Enter to return to menu..." temp
done
