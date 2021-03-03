# fake-catalog-generator
Fake Catalog Item Generator 

1. `pyenv virtualenv 3.9.1 fake-catalog-generator`
2. `pyenv local fake-catalog-generator`
3. `pip install -r requirements.txt`
4. ` uvicorn app.main:app --workers <num_procs>` or if you are developing this library run ` uvicorn app.main:app --reload` for hot reloading
