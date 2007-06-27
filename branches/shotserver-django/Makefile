pep8 :
	pep8.py --filename=*.py --repeat .

pylint :
	-pylint shotserver04 \
	| grep -v "/tests\.py:" \
	| grep -v "Invalid name \"urlpatterns\"" \
	| grep -v "\.Admin] Missing docstring" \
	| grep -v "\.Admin] Class has no __init__ method" \
	| grep -v "\.Admin] To few public methods" \
	| grep -v "\.Meta] Missing docstring" \
	| grep -v "\.Meta] Class has no __init__ method" \
	| grep -v "\.Meta] To few public methods" \
	| grep -v "Unused argument 'http_request'" \
	| grep -v "Access to a protected member _meta" \
	| grep -v "Undefined variable '_'" \
	| grep -v "E1101" \
	| grep -v "W0142"

docstrings :
	-pylint shotserver04 \
	| grep -v "/tests\.py:" \
	| grep -v "\.Admin] Missing docstring" \
	| grep -v "\.Meta] Missing docstring" \
	| grep "docstring"

doctest :
	grep -rl --include "*.py" "doctest.testmod()" . | xargs -n1 python

headers :
	find shotserver04 -name "*.py" \
	| xargs header.py shotserver04/settings.py

backup :
	pg_dump shotserver04 | bzip2 \
	> /tmp/shotserver04.`date +%y%m%d-%H%M%S`.sql.bz2

reset : backup
	echo DROP DATABASE shotserver04 | psql template1
	echo CREATE DATABASE shotserver04 | psql template1
	shotserver04/manage.py syncdb

customsql :
	./django_dump.py -p shotserver04 -i \
	Architecture Platform OperatingSystem \
	Javascript Java Flash Engine BrowserGroup
