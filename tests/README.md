# Testing
To ensure that the our scripts are compatible with possible changes, we implemented some test cases here. These tests are running each of the use cases and check if they are running without runtime errors and also if they are executed successfully.

## Run the tests
To execute the tests you need to do the following steps:
1. Install standard requirements
   ```
   pip install -r requirements.txt
   ```
1. Install test requirements
   ```
   pip install -r test_requirements.txt
   ```
1. Create test `.env`-file
    - Rename `env.example` to `.env`
    - Edit the file and insert all the required information described in the file
1. Run all the tests
   ```
   pytest tests/test_use_cases.py
   ```