# Disable the following PyLint messages:
# R0903 - Not enough public methods
# W0142 - Used * or ** magic
# W0232 - Class has no __init__ method
# W0622 - Redefining built-in
DISABLE="R0903,W0142,W0232,W0622"

pylint :
	@find shotserver03 scripts -name "*.py" > check-pylint
	@echo "Running PyLint on "`wc -l < check-pylint`" files..."
	@xargs -a check-pylint pylint \
		--rcfile=pylintrc --disable-msg=$(DISABLE)

install :
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build dist *.png *.ppm check-*
