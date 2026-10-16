# Static Code Analysis Issues Report

This document details all issues identified in `gym_system.py` using **Bandit**, **Pylint**, **Flake8**, and dynamic execution analysis, prioritized by severity.

## Summary Table of Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Command Injection via Shell (`B605` / `B607`) | Security (High) | 36 | `os.system("rm -f " + prefix + "*.json")` invokes a system shell with unsanitized parameters, vulnerable to command injection and platform incompatibility. | Replace shell call with safe Python standard library functions (`glob.glob` / `Path.glob` and `os.remove` / `Path.unlink`). |
| Mutable Default Argument (`W0102`) | Bug / Code Quality (High) | 8 | `def book_class(..., attendance_log=[])` binds default list at function definition time, sharing mutating state across separate function calls. | Set default argument to `None` and initialize `attendance_log = [] if attendance_log is None else attendance_log` inside the function. |
| Off-by-One Capacity Enforcement | Logic Bug (High) | 11 | `len(rosters[class_name]) > class_capacity.get(...)` uses `>` instead of `>=`, allowing classes to overbook by one member beyond limit (e.g. 4 bookings for Yoga with capacity 3). | Change comparison operator from `>` to `>=`. |
| Bare Exception Handler (`W0702` / `E722`) | Error Handling (Medium) | 21 | `except:` catches all exceptions blindly, including `KeyboardInterrupt`, `SystemExit`, and unexpected runtime errors, masking bugs. | Specify exact expected exception types: `except (KeyError, ValueError):`. |
| Resource Leak & Unspecified Encoding (`R1732` / `W1514` / `W0622`) | Resource Management (Medium) | 31-33 | `f = open(file, "w")` leaves file unclosed if exceptions occur, does not specify explicit encoding (`utf-8`), and parameter name `file` shadows the built-in. | Rename parameter to `filepath`, specify `encoding="utf-8"`, and manage file lifecycle using `with open(...) as f:`. |
| Missing Input Validation on Capacity | Data Integrity / Bug (Medium) | 24-25 | `set_capacity` allows negative capacity values (e.g. `set_capacity("Spin", -2)`), resulting in invalid state and permanently full classes. | Add validation to reject negative seat counts (`if seats < 0: raise ValueError(...)`). |
| Non-conforming Function Name (`C0103`) | Code Style / PEP 8 (Low) | 27 | `def addMembers` uses camelCase instead of PEP 8 standard `snake_case`. | Rename function to `add_members` and update all invocation sites. |
| Non-idiomatic String Formatting (`C0209`) | Code Style (Low) | 15 | `"%s -> %s" % (member_id, class_name)` uses deprecated C-style formatting instead of modern f-strings. | Replace with f-string: `f"{member_id} -> {class_name}"`. |
| Non-idiomatic Dictionary Iteration (`C0206`) | Performance / Style (Low) | 39-40 | `for c in rosters:` followed by `rosters[c]` redundantly queries keys instead of directly iterating key-value pairs. | Use `for class_name, members in rosters.items():`. |
| Missing Module & Function Docstrings (`C0114` / `C0116`) | Documentation (Low) | 1, 8, 18, 24, 27, 31, 35, 38, 42 | Missing docstrings for module and all 8 functions, reducing code readability and maintainability. | Add PEP 257 compliant docstrings describing purpose, arguments, and return values. |
| Missing Blank Lines (`E302` / `E305`) | PEP 8 Formatting (Low) | 8, 18, 24, 27, 31, 35, 38, 42, 58 | Top-level function definitions and call statements are separated by only 1 blank line instead of PEP 8 standard 2 blank lines. | Ensure exactly 2 blank lines surround top-level functions. |

## Tool Reports Overview Before Fixes

- **Bandit Score:** 1 High Severity issue (`B605` in `clear_old_exports`).
- **Pylint Score:** 6.60 / 10 (12 code style, warning, and refactoring issues).
- **Flake8 Issues:** 10 violations (1 bare except `E722`, 9 whitespace/blank line issues `E302` & `E305`).
