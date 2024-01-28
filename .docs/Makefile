SPHINXOPTS  ?= -c .
SPHINXBUILD ?= sphinx-build
SOURCEDIR    = source
BUILDDIR     = build
REFERENCEDIR = $(SOURCEDIR)/refs
DOCSDIR      = ../docs

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clear-refs docs pages help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clear:
	rm -rf build

clear-refs:
	find $(REFERENCEDIR) -type f -name *.rst ! -name index.rst -exec rm -f {} \;

docs:
	make clear
	make html
	make clear-refs
	mkdir -p $(DOCSDIR) && rm -rf $(DOCSDIR)/*
	cp -r build/html/{_static,refs,*.html} $(DOCSDIR)

push:
	git add $(DOCSDIR)/
	git commit -m "Update pages"
	git push origin gh-pages
