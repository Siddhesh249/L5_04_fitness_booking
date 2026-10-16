# Static Code Analysis Issues Report

This document details all issues identified in `gym_system.py` using **Bandit**, **Pylint**, **Flake8**, and dynamic execution analysis, prioritized by severity, along with resolution details and verification results.

## Summary Table of Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach | Status |
|---|---|---|---|---|---|
| Command Injection via Shell (`B605` / `B607`) | Security (High) | 36 | `os.system("rm -f " + prefix + "*.json")` invokes a system shell with unsanitized parameters, vulnerable to command injection and platform incompatibility. | Replaced shell call with safe Python standard library functions (`glob.glob` and `os.remove`). | **Fixed** |
| Mutable Default Argument (`W0102`) | Bug / Code Quality (High) | 8 | `def book_class(..., attendance_log=[])` binds default list at function definition time, sharing mutating state across separate function calls. | Set default argument to `None` and initialized `attendance_log = [] if attendance_log is None else attendance_log` inside the function. | **Fixed** |
| Off-by-One Capacity Enforcement | Logic Bug (High) | 11 | `len(rosters[class_name]) > class_capacity.get(...)` uses `>` instead of `>=`, allowing classes to overbook by one member beyond limit (e.g. 4 bookings for Yoga with capacity 3). | Changed comparison operator from `>` to `>=`. | **Fixed** |
| Bare Exception Handler (`W0702` / `E722`) | Error Handling (Medium) | 21 | `except:` catches all exceptions blindly, including `KeyboardInterrupt`, `SystemExit`, and unexpected runtime errors, masking bugs. | Specified exact expected exception types: `except (KeyError, ValueError):`. | **Fixed** |
| Resource Leak & Unspecified Encoding (`R1732` / `W1514` / `W0622`) | Resource Management (Medium) | 31-33 | `f = open(file, "w")` leaves file unclosed if exceptions occur, does not specify explicit encoding (`utf-8`), and parameter name `file` shadows the built-in. | Renamed parameter to `filepath`, specified `encoding="utf-8"`, and managed file lifecycle using `with open(...) as f:`. | **Fixed** |
| Missing Input Validation on Capacity | Data Integrity / Bug (Medium) | 24-25 | `set_capacity` allows negative capacity values (e.g. `set_capacity("Spin", -2)`), resulting in invalid state and permanently full classes. | Added validation to reject negative seat counts (`if seats < 0: ... return`) with user warning. | **Fixed** |
| Non-conforming Function Name (`C0103`) | Code Style / PEP 8 (Low) | 27 | `def addMembers` uses camelCase instead of PEP 8 standard `snake_case`. | Renamed function to `add_members` and updated all invocation sites. | **Fixed** |
| Non-idiomatic String Formatting (`C0209`) | Code Style (Low) | 15 | `"%s -> %s" % (member_id, class_name)` uses deprecated C-style formatting instead of modern f-strings. | Replaced with f-string: `f"{member_id} -> {class_name}"`. | **Fixed** |
| Non-idiomatic Dictionary Iteration (`C0206`) | Performance / Style (Low) | 39-40 | `for c in rosters:` followed by `rosters[c]` redundantly queries keys instead of directly iterating key-value pairs. | Used `for class_name, members in rosters.items():`. | **Fixed** |
| Missing Module & Function Docstrings (`C0114` / `C0116`) | Documentation (Low) | 1, 8, 18, 24, 27, 31, 35, 38, 42 | Missing docstrings for module and all functions, reducing code readability and maintainability. | Added PEP 257 compliant docstrings describing purpose, arguments, and return values. | **Fixed** |
| Missing Blank Lines (`E302` / `E305`) | PEP 8 Formatting (Low) | 8, 18, 24, 27, 31, 35, 38, 42, 58 | Top-level function definitions and call statements were separated by only 1 blank line instead of PEP 8 standard 2 blank lines. | Formatted code with exactly 2 blank lines surrounding top-level definitions. | **Fixed** |

---

## Static Analysis Metrics: Before vs. After

| Metric / Tool | Before Fixes | After Fixes | Target / Standard |
|---|---|---|---|
| **Bandit (Security)** | 1 High Severity issue (`B605` shell injection) | **0 issues identified** | 0 High/Medium issues |
| **Pylint (Code Quality & Logic)** | 6.60 / 10 (12 warnings/conventions) | **10.00 / 10** (0 warnings/conventions) | > 9.50 / 10 |
| **Flake8 (PEP 8 Compliance)** | 10 style violations (`E722`, `E302`, `E305`) | **0 style violations** | Clean PEP 8 compliance |

---

## Detailed Tool Output Comparison

### 1. Bandit
- **Before:**
  ```text
  >> Issue: [B605:start_process_with_a_shell] Starting a process with a shell, possible injection detected, security issue.
     Severity: High   Confidence: High
     Location: ./gym_system.py:36:4
  ```
- **After:**
  ```text
  Test results:
      No issues identified.
  Run metrics:
      Total issues: 0 (High: 0, Medium: 0, Low: 0)
  ```

### 2. Pylint
- **Before:**
  ```text
  gym_system.py:1:0: C0114: Missing module docstring (missing-module-docstring)
  gym_system.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
  gym_system.py:8:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
  gym_system.py:15:26: C0209: Formatting a regular string which could be an f-string (consider-using-f-string)
  gym_system.py:21:4: W0702: No exception type(s) specified (bare-except)
  gym_system.py:27:0: C0103: Function name "addMembers" doesn't conform to snake_case naming style (invalid-name)
  gym_system.py:32:8: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
  gym_system.py:32:8: R1732: Consider using 'with' for resource-allocating operations (consider-using-with)
  gym_system.py:39:4: C0206: Consider iterating with .items() (consider-using-dict-items)
  Your code has been rated at 6.60/10
  ```
- **After:**
  ```text
  Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
  ```

### 3. Flake8
- **Before:**
  ```text
  gym_system.py:8:1: E302 expected 2 blank lines, found 1
  gym_system.py:18:1: E302 expected 2 blank lines, found 1
  gym_system.py:21:5: E722 do not use bare 'except'
  gym_system.py:24:1: E302 expected 2 blank lines, found 1
  gym_system.py:27:1: E302 expected 2 blank lines, found 1
  gym_system.py:31:1: E302 expected 2 blank lines, found 1
  gym_system.py:35:1: E302 expected 2 blank lines, found 1
  gym_system.py:38:1: E302 expected 2 blank lines, found 1
  gym_system.py:42:1: E302 expected 2 blank lines, found 1
  gym_system.py:58:1: E305 expected 2 blank lines after class or function definition, found 1
  ```
- **After:**
  ```text
  (Clean output - 0 violations)
  ```
