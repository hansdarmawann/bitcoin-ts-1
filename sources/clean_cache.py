import os
import shutil
import sys
import importlib

def full_python_clean(root_dir="..", modules=None):
    # Remove __pycache__
    for root, dirs, _ in os.walk(root_dir):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(root, "__pycache__"))
            print(f"🧹 Removed __pycache__ in {root}")
    
    # Reload modules
    if modules:
        for m in modules:
            if m in sys.modules:
                importlib.reload(sys.modules[m])
                print(f"🔄 Reloaded module: {m}")

# Usage
full_python_clean(
    root_dir="..",
    modules=["src.model_loader"]
)