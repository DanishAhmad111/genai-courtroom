#!/usr/bin/env python3
"""
Test script for the GenAI Courtroom with Hybrid Judge
Tests both fine-tuned model + API model integration
"""

import os
import sys

# Ensure UTF-8 console output on Windows to avoid encoding errors
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.append('backend')

from courtroom_logic import run_courtroom

def test_hybrid_judge():
    """Test the hybrid judge functionality with a sample case"""
    
    print("GenAI Courtroom - Hybrid Judge Test")
    print("=" * 50)
    
    # Sample legal case
    test_case = """
    Case: State vs. Rajesh Kumar
    
    Facts: The accused Rajesh Kumar was found in possession of 500 grams of cannabis 
    during a police search at his residence. He claims the substance was for personal 
    medicinal use due to chronic pain from an accident. The prosecution argues this 
    exceeds the permissible limit for personal consumption under the NDPS Act.
    
    Evidence: 
    - 500g cannabis recovered from accused's residence
    - Medical certificate showing chronic pain condition
    - No evidence of sale or distribution
    - Accused has no prior criminal record
    """
    
    print(f"Test Case:\n{test_case}\n")
    print("Processing case through hybrid judge system...")
    print("-" * 50)
    
    try:
        # Run the courtroom simulation
        prosecution, defense, verdict = run_courtroom(test_case)
        
        print("COURTROOM PROCEEDINGS:")
        print("=" * 50)
        
        print("\nPROSECUTION ARGUMENT:")
        print("-" * 30)
        print(prosecution)
        
        print("\nDEFENSE ARGUMENT:")
        print("-" * 30)
        print(defense)
        
        print("\nJUDGE'S VERDICT (HYBRID MODEL):")
        print("-" * 40)
        print(verdict)
        
        print("\nTest completed successfully!")
        print("Fine-tuned model + API model integration working!")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        print("Please check your configuration and model files.")

if __name__ == "__main__":
    test_hybrid_judge()
