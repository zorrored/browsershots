# Disable the following PyLint messages:
# R0903 - Not enough public methods
# W0142 - Used * or ** magic
# W0232 - Class has no __init__ method
# W0622 - Redefining built-in
DISABLE="R0903,W0142,W0232,W0622"

all : formatting doctest pylint

formatting :
	@echo Checking formatting...
	@find lib scripts -name "*.py" \
	    | grep -v scripts/xmlrpc_help.py \
	    | xargs devtools/formatting.py

doctest :
	@echo Checking doctest...
	@python lib/database/__init__.py
	@python lib/interface/xhtml.py
	@python lib/interface/menu.py
	@python lib/interface/human.py
	@python lib/xmlrpc/__init__.py
	@python lib/xmlrpc/system.py

pylint :
	@echo Checking pylint...
	@find lib scripts -name "*.py" \
	    | grep -v scripts/xmlrpc_help.py \
	    | xargs pylint --rcfile=conf/pylintrc --disable-msg=$(DISABLE) \
	    || exit 0

install :
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build dist
