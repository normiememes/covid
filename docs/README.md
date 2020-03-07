# Covid Docs

## Contents

- [Usage](#Usage)

## Usage

### Docker
#### Build
```bash
docker build . -t covid:local
```

#### Docker-compose
```bash
docker-compose up -d

# command override
gunicorn main:api -c gunicorn_config.py
```

#### Test
```bash
pytest tests -s --cov=. --cov-report html:./htmlcov --cov-fail-under 50 --log-cli-level DEBUG

# view coverage output
open htmlcov/index.html
```
