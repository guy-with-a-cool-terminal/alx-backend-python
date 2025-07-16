# 0x03. Unittests and Integration Tests

## Description

This project focuses on writing **unit** and **integration tests** in Python. It involves testing utilities, mocking HTTP requests, and ensuring code correctness through automated tests using the `unittest` module, `parameterized`, and `unittest.mock`.

---

## Learning Objectives

By the end of this project, you should be able to explain:

- The difference between **unit tests** and **integration tests**
- How and when to use:
  - **Mocking**
  - **Fixtures**
  - **Parameterized tests**
- How to use `unittest` effectively to write reliable and repeatable tests
- Why test coverage and mocking external dependencies is important

---

## Requirements

- Python 3.7
- Ubuntu 18.04 LTS
- All code complies with `pycodestyle` (PEP8) version 2.5
- All modules, classes, and functions contain full docstrings
- All code is executable and ends with a new line
- Type annotations are used in all functions and methods

---

## File Structure

```

.
├── client.py              # GithubOrgClient and related methods
├── fixtures.py            # Fixtures for integration tests
├── test\_client.py         # Unit tests for GithubOrgClient
├── test\_utils.py          # Unit tests for utility functions
├── utils.py               # Utility functions used by client.py
└── README.md              # Project documentation

````

---

## How to Run Tests

Run all tests:
```bash
python3 -m unittest discover
````

Run a specific test file:

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

---

## Author

Written by \Bri as part of the ALX Backend Python track.
