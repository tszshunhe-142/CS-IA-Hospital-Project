# Automated tests

Run all tests from the project root:

```powershell
python -m unittest discover -s tests -v
```

Algorithm and Flask route tests use fictional in-memory lecture records. Route tests mock the MySQL data access functions, so they validate page integration and rendering without requiring a running MySQL server. They do not replace a real database connection check.
