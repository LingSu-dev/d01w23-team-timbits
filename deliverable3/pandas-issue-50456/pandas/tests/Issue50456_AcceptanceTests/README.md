# Issue 50456 Acceptance Tests


To run the test, please make sure you setup as below:
1. Have python3 installed
2. correctly set up a development environment for pandas 1.5.3: https://pandas.pydata.org/docs/dev/development/contributing_environment.html#

Execute the following command:
```js
pytest pandas/tests/Issue50456_AcceptanceTests/test_50456.py
```

Verify that the three generated output look like expected_outcome.pdf and do not look like issue_outcome.pdf      
If this is true, then the tests are successful 