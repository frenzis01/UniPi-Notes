# 🧪 TESTAR Lab: Scriptless Web Testing in Python

This project is a starter framework for building your own simplified version of [TESTAR](https://testar.org/): 
an autonomous testing tool that explores web applications without predefined test scripts.

## 🎯 Objective

Your task is to complete and extend this basic implementation so it can:
- Detect interactive elements (widgets) on a web page,
- Derive and execute meaningful actions,
- Use oracles to check for application correctness,
- Repeat the process over multiple test runs and sequences.

## 📂 Project Structure

- `TESTAR_template.py`: Core testing logic with TODOs for you to complete
- `testingTESTAR.py`: Example test cases for different web apps
- `input_data_generation.py`: Helpers for generating random text/numbers/naughty strings
- `blns.py`: A filtered subset of the Big List of Naughty Strings
- `logging_actions.py`: Utilities for logging and inspecting elements
- `requirements.txt`: Python dependencies (install with pip)

## 🚀 Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download and set up ChromeDriver**
   - Make sure `chromedriver` is in your PATH.
   - Compatible with your local version of Google Chrome.

3. **Run the tester**
   Try one of the example test cases:
   ```bash
   python testingTESTAR.py
   ```

## 🧠 What You Need to Do

### 1. Add More CSS Selectors
Start with just detecting `<a>` links and `<input type="submit">`. Add more to cover:
- Buttons (`button`)
- Input fields (`input[type='text']`, etc.)
- Dropdowns
- JavaScript-enhanced elements (`[onclick]`, `[role='button']`, etc.)

### 2. Derive More Actions
Understand how the `lambda` functions in `derive_actions()` work.
Then:
- Add actions like `send_keys()` for typing into fields
- Use the `Select` class for dropdowns

### 3. Add Oracles
Check that the system behaves as expected after each action:
- Is the page still reachable?
- Are there any error messages?
- Has the page changed correctly?

### 4. Print a Summary
Implement your own `print_test_summary()` to report:
- Number of actions
- Any errors
- Anything else useful!

---

Happy testing! 