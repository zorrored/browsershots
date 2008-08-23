install :
	python setup.py install

initial_data : \
shotserver05/platforms/fixtures/initial_data.json \
shotserver05/browsers/fixtures/initial_data.json \

shotserver05/%/fixtures/initial_data.json :
	mkdir -p shotserver05/$*/fixtures
	shotserver05/manage.py dumpdata --indent=4 $* > $@

docs : \
docs/xml-rpc.txt \

docs/xml-rpc.txt :
	xmlrpcdoc http://127.0.0.1:8000/xmlrpc/ > $@

docs/html : docs
	mkdir -p $@
	ls docs | grep txt | sed s/.txt// \
	| xargs -Iname rst2html.py docs/name.txt docs/html/name.html
