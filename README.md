# login_boilerplate_api
Boilerplate for login function

<!-- suppress ALL -->
<div align="center">
    <h1>LOGIN Boilerplate API</h1>
    <p>Backend for Login Boilerplate</p>
</div>

## Usage
Setup your virtual environment
```sh
virtualenv venv or python -m venv <directory>
source venv/bin/activate
```

Install app requirements, make sure you have every environment variable setup properly, and run

```sh
pip install -r requirements/base.txt
uvicorn app.main:app --reload
```

### Linting
Fix format
```
yarn lint
```