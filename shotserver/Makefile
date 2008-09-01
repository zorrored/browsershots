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

precommit : docs headers properties pep8
	mkdir -p $@
	cat docs/xml-rpc.txt | sort -u > precommit/xml-rpc-sorted.txt
	cat shotserver05/*/models.py | sort -u > precommit/models-sorted.txt

headers :
	find . -name "*.py" | grep -v build/ \
        | xargs header.py shotserver05/__init__.py

properties :
        find . -name "*.py" \
        | grep -v build/ \
        | xargs svn propset svn:keywords "Rev Date Author"
        find . -type f | grep -v build/ | grep -v \\.svn \
        | grep -v \\.bz2 | grep -v \\.gz | grep -v \\.pyc \
        | grep -v \\.png | grep -v \\.ico | grep -v \\.jpg \
        | grep -v django.mo | grep -v rosetta-shotserver \
        | xargs svn propset svn:eol-style native

pep8 :
	pep8.py --filename=*.py shotserver05

jquery :
	wget -O shotserver05/static/js/jquery.form.js \
http://jqueryjs.googlecode.com/svn/trunk/plugins/form/jquery.form.js
	wget -O shotserver05/static/js/jquery.js \
http://jqueryjs.googlecode.com/files/jquery-1.2.6.min.js
#http://jqueryjs.googlecode.com/files/jquery-1.2.6.js
#http://jqueryjs.googlecode.com/files/jquery-1.2.6.pack.js
