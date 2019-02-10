orator migrate -c config/database.yml --force
orator migrate:refresh -c config/database.yml --force --seed
rm -rf cover
rm -rf .coverage
nosetests tests/basic/test_* --with-coverage --cover-package=main,decorators,controllers --logging-level=DEBUG --no-byte-compile --cover-html -s

orator migrate:refresh -c config/database.yml --force --seed
rm -rf cover
rm -rf .coverage
nosetests tests/advance/test_* --with-coverage --cover-package=main,decorators,controllers --logging-level=DEBUG --no-byte-compile --cover-html -s