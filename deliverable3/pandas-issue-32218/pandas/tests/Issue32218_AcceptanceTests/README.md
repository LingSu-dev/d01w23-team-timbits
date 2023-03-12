# Issue 50456 Acceptance Tests


To run the test, please make sure you setup as below:
1. Have python3 installed
2. correctly set up a development environment for pandas our updated version 1.1.x: https://pandas.pydata.org/docs/dev/development/contributing_environment.html#

Execute the following command:
```
python pandas/tests/Issue32218_AcceptanceTests/test_32218.py
```

Open pandas/tests/Issue32218_AcceptanceTests/expected_output.pdf
     pandas/tests/Issue32218_AcceptanceTests/issue_output.pdf

Verify that the generated output look like expected_output.pdf and do not look like issue_output.pdf      
If this is true, then the tests are successful.