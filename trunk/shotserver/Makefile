all : formatting doctest pylint
	@echo Finished checking $^.

formatting :
	@find lib scripts -name "*.py" | xargs scripts/shotserver03_formatting.py

doctest :
	@python lib/interface/xhtml.py

pylint :
	@find lib scripts -name "*.py" \
		| xargs pylint --rcfile=conf/pylintrc \
		| grep -v "Undefined variable 'req'" \
		| grep -v "Undefined variable 'con'" \
		| grep -v "Undefined variable 'cur'" \
		| grep -v "Not enough public methods" \
		| grep -v "Used \* or \*\* magic" \

install :
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build
