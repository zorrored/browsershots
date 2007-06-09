pep8 :
	pep8.py --filename=*.py --repeat .

pylint :
	pylint shotserver04 \
	| grep -v "/tests\.py:" \
	| grep -v "Invalid name \"urlpatterns\"" \
	| grep -v "\.Admin] Missing docstring" \
	| grep -v "\.Admin] Class has no __init__ method" \
	| grep -v "\.Admin] To few public methods" \
	| grep -v "\.Meta] Missing docstring" \
	| grep -v "\.Meta] Class has no __init__ method" \
	| grep -v "\.Meta] To few public methods" \
	| grep -v "E1101"

reset :
	echo DROP DATABASE shotserver04 | psql template1
	echo CREATE DATABASE shotserver04 | psql template1
	shotserver04/manage.py syncdb
	cat sql/platforms_architecture.sql | psql shotserver04
	cat sql/platforms_platform.sql | psql shotserver04
	cat sql/platforms_operatingsystem.sql | psql shotserver04
	cat sql/browsers_engine.sql | psql shotserver04
	cat sql/browsers_browsergroup.sql | psql shotserver04
