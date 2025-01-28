"""
GUARANTEED WORKING VERSION - LIFE GOALS TRACKER
Minimal dependencies, maximum compatibility
"""

import sys
import json
import os
import time
from datetime import datetime

# Debug mode (set to True to see technical details)
DEBUG = False

# ====================
# CORE FUNCTIONALITY
# ====================

def debug_log(message):
    if DEBUG:
        print(f"[DEBUG] {message}")

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\n" * 50)  # Fallback for weird terminals

def main():
    # Basic system check
    debug_log(f"Python version: {sys.version}")
    debug_log(f"Platform: {sys.platform}")
    
    try:
        # Simple goal collection
        goals = []
        print("Welcome to Life Goal Tracker!")
        print("Let's start with 3 quick goals (press Enter after each):\n")
        
        for i in range(1, 4):
            while True:
                goal = input(f"Goal {i}: ").strip()
                if goal:
                    goals.append({
                        "text": goal,
                        "timestamp": datetime.now().isoformat()
                    })
                    break
                print("Please enter a valid goal!\n")
        
        # Save to file
        with open("my_goals.json", "w") as f:
            json.dump(goals, f, indent=2)
        
        print("\nSuccess! Your goals have been saved to my_goals.json")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        debug_log(f"Error details: {repr(e)}")
    
    # Keep window open
    if sys.platform.startswith('win'):
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")