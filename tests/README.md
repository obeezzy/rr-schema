# How to run tests

```bash
$ cd tests # Go to 'tests' directory
$ python3 -m venv env # Create a virtual environment
$ source env/bin/activate # Activate virtual environment
$ pip install -r requirements.txt # Install all required Python packages
$ chmod +x runtests.sh # Make 'run' script executable
$ export PYTHONPATH=.
$ ./runtests.sh # Run all tests
```

To run tests in sales subdirectory:
```bash
$ ./runtests proctests.common.sales
```

To run the "AddDebtor" test case:
```bash
$ ./runtests proctests.common.debtor test_adddebtor.py
```