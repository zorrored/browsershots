# Disable the following PyLint messages:
# F0203 - Bug in pylint (Unable to resolve tabledict)
# W0142 - Used * or ** magic
# W0232 - Class has no __init__ method
# R0903 - Not enough public methods
DISABLE="F0203,W0142,W0232,R0903"

all : formatting doctest pylint
	@echo Checked: $^

formatting :
	@find lib scripts -name "*.py" \
	    | xargs scripts/shotserver03_formatting.py

doctest :
	@python lib/interface/xhtml.py
	@python lib/interface/menu.py
	@python lib/database/__init__.py

pylint :
	@find lib scripts -name "*.py" \
	    | xargs pylint --rcfile=conf/pylintrc --disable-msg=$(DISABLE) \
	    | grep -v "Undefined variable 'req'" \
	    | grep -v "Undefined variable 'con'" \
	    | grep -v "Undefined variable 'cur'" \

install :
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build
