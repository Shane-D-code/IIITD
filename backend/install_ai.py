#!/usr/bin/env python3
import subprocess
import sys

def install_ai_deps():
    """Install AI model dependencies"""
    deps = [
        "transformers==4.35.0",
        "torch",
        "tokenizers==0.14.1"
    ]
    
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    
    print("✓ AI dependencies installed!")
    print("Restart server to enable AI scoring")

if __name__ == "__main__":
    install_ai_deps()