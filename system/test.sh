rm -rf cover
rm -rf .coverage
nosetests tests/test_* --with-coverage --cover-package=main,decorators,controllers --logging-level=DEBUG --no-byte-compile --cover-html