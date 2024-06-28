- File names should start or end with "test", as in `test_example.py` or `example_test.py`.
- If tests are defined as methods on a class, the class name should start with "Test", as in `TestExample`. The class should not have an `__init__` method.
- Test method names or function names should start with "test_", as in `test_example`. Methods with names that don’t match this pattern won’t be executed as tests.
- Each test function or method should have one and only one `assert` statement. <br/>
  An example: <br/>
    ```
    # contents of source code

    def vowels():
        return set('aeiou')


    # content of test_language.py

    def test_vowels():
        result =  vowels()
        expected = set('aeyou')
        assert result == expected
    ```

- Calling `make unittest` to run unittest and generate HTML reports in reports directory.