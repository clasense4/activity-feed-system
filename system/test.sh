cd ..
orator migrate:refresh -c system/config/database.yml --force --seed
cd system
rm -rf cover
rm -rf .coverage
nosetests tests/basic/test_* --with-coverage --cover-package=main,decorators,controllers --logging-level=DEBUG --no-byte-compile --cover-html -s