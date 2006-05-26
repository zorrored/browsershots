test :
	@find lib scripts -name "*.py" | xargs scripts/shotserver03_format.py
	@python lib/interface/xhtml.py

pylint :
	@find lib scripts -name "*.py" | xargs pylint --reports=n --max-line-length=120 --enable-similarities=n --parseable=y

install : test
	python setup.py install
	apache2ctl restart

clean :
	rm -rf build
