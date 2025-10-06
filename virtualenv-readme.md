# Complete Guide to Using virtualenv in Bash

## ✅ How to Run virtualenv from Bash

### 1. **Create a Virtual Environment**
```bash
# Use Python module syntax (recommended)
python -m virtualenv env_name

# Or if virtualenv is in PATH
virtualenv env_name
```

### 2. **Activate the Virtual Environment**
```bash
# On Windows with Bash
source env_name/Scripts/activate

# On Linux/Mac
source env_name/bin/activate
```

### 3. **Verify Activation**
When activated, you'll see:
- Your prompt changes to show `(env_name)` at the beginning
- `which python` points to the virtual environment's Python
- `pip --version` shows it's using the virtual environment's pip

### 4. **Deactivate the Virtual Environment**
```bash
deactivate
```

### 5. **Example: Creating and Using a Virtual Environment**
```bash
# Create virtual environment
python -m virtualenv myproject

# Activate it
source myproject/Scripts/activate  # Windows
# source myproject/bin/activate    # Linux/Mac

# Verify activation
which python
pip --version

# Install packages (they'll be isolated to this environment)
pip install requests numpy

# Work on your project...

# Deactivate when done
deactivate
```

### 6. **Alternative: Use venv (built into Python)**
You can also use Python's built-in `venv` module:
```bash
python -m venv env_name
source env_name/Scripts/activate  # Windows
# source env_name/bin/activate    # Linux/Mac
```

### 7. **Troubleshooting**

#### Problem: `virtualenv: command not found`
**Solution:** Use the Python module syntax:
```bash
python -m virtualenv env_name
```

#### Problem: Virtual environment not activating
**Solution:** Make sure to use the correct path:
- Windows: `source env_name/Scripts/activate`
- Linux/Mac: `source env_name/bin/activate`

#### Problem: Still using system Python after activation
**Solution:** Check if activation worked:
```bash
which python  # Should point to env_name/Scripts/python or env_name/bin/python
```

### 8. **Best Practices**

1. **Use descriptive names** for your virtual environments
2. **Always activate** before working on a project
3. **Create a requirements.txt** file to track dependencies:
   ```bash
   pip freeze > requirements.txt
   ```
4. **Install from requirements.txt** in new environments:
   ```bash
   pip install -r requirements.txt
   ```
5. **Add virtual environment folders to .gitignore**:
   ```
   env/
   venv/
   .env/
   ```

### 9. **Key Benefits**
- **Isolation**: Each project has its own dependencies
- **Version Control**: Different projects can use different package versions
- **Clean System**: Keeps your system Python installation clean
- **Reproducibility**: Easy to recreate environments on different machines

### 10. **Common Commands Summary**
```bash
# Create
python -m virtualenv myenv

# Activate
source myenv/Scripts/activate  # Windows
source myenv/bin/activate      # Linux/Mac

# Check status
which python
pip list

# Install packages
pip install package_name

# Save dependencies
pip freeze > requirements.txt

# Deactivate
deactivate

# Remove environment (just delete the folder)
rm -rf myenv
```

---

**Note:** This guide was created based on a successful virtualenv setup on Windows using Bash, where Python 3.12.0 and pip 25.2 were installed and working properly.