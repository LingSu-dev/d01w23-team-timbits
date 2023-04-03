# Issue 50582 Acceptance Tests


To run the test, please make sure you setup as below:
1. Have python3 installed
2. correctly set up a development environment for pandas our updated version 1.1.x: https://pandas.pydata.org/docs/dev/development/contributing_environment.html#

Execute the following command:
```
pytest pandas/tests/Issue50582_DfBuilder_acceptanceTests/test_dfBuilder.py
```

Verify that the output is as below:
```
============ 15 passed ============
```    
If this is true, then the tests are successful.