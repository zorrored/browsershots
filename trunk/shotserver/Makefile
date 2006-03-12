test : format.py
	@find lib scripts -name "*.py" | xargs python format.py
	@python lib/interface/xhtml.py

install :
	python setup.py install
	apache2ctl restart
