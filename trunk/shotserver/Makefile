test :
	@find lib scripts -name "*.py" | xargs scripts/shotserver03_format.py
	@python lib/interface/xhtml.py

pylint :
	@find lib scripts -name "*.py" | xargs pylint --rcfile=conf/pylintrc \
		| grep -v "Undefined variable 'req'" \
		| grep -v "Undefined variable 'con'" \
		| grep -v "Undefined variable 'cur'" \
		| grep -v "Not enough public methods" \

install : test
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build
