# Disable the following PyLint messages:
# R0903 - Not enough public methods
# W0142 - Used * or ** magic
# W0232 - Class has no __init__ method
# W0622 - Redefining built-in
DISABLE="R0903,W0142,W0232,W0622"

all : formatting doctest pylint

formatting :
	@find lib -name "*.py" > check-formatting
	@find scripts -name "*.py" >> check-formatting
	@echo "Checking formatting on "`wc -l < check-formatting`" files..."
	@xargs -a check-formatting devtools/formatting.py

doctest :
	@rm -f check-doctest
	@echo lib/database/__init__.py >> check-doctest
	@echo lib/interface/xhtml.py >> check-doctest
	@echo lib/interface/menu.py >> check-doctest
	@echo lib/interface/human.py >> check-doctest
	@echo lib/xmlrpc/__init__.py >> check-doctest
	@echo lib/xmlrpc/system.py >> check-doctest
	@echo "Running doctest on "`wc -l < check-doctest`" files..."
	@xargs -a check-doctest -n 1 python

pylint :
	@find lib scripts -name "*.py" > check-pylint
	@echo "Running PyLint on "`wc -l < check-pylint`" files..."
	@xargs -a check-pylint pylint \
		--rcfile=pylintrc --disable-msg=$(DISABLE)

install :
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build dist *.png *.ppm check-*
