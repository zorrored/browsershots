test :
	@find lib scripts -name "*.py" | xargs scripts/shotserver03_format.py
	@python lib/interface/xhtml.py

install :
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build
