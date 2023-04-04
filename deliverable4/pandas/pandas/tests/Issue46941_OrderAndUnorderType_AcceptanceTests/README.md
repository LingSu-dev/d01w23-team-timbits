# Issue 46941 Acceptance Tests


To run the test, please make sure you setup as below:
1. Have python3 installed
2. correctly set up a development environment for pandas our updated version 1.5.x: https://pandas.pydata.org/docs/dev/development/contributing_environment.html#

Execute the following command:
```
python pandas/tests/Issue46941_Accessor_AcceptanceTests/test_order_and_unorder_type.py
```

Open pandas/tests/Issue46941_OrderAndUnorderType_AcceptanceTests/expected_output.pdf

Verify that the generated output look like expected_output.pdf    
If this is true, then the tests are successful.
