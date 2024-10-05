PACKAGE_NAME = modelstat
VERSION := $(shell cat VERSION.txt)
PYTHON = python3
SRC_DIR = $(PACKAGE_NAME)
OUT_DIR = dist
DOCS_DIR = docs

.PHONY: build docs install clean release test lint type-check dev-install

build: pyproject.toml
	$(PYTHON) -m build

pyproject.toml: VERSION.txt requirements.txt
	@echo "Generating pyproject.toml"
	@echo "[build-system]" > $@
	@echo "requires = [\"hatchling\"]" >> $@
	@echo "build-backend = \"hatchling.build\"" >> $@
	@echo "[project]" >> $@
	@echo "name = \"$(PACKAGE_NAME)\"" >> $@
	@echo "version = \"$(VERSION)\"" >> $@
	@echo "description = \"Your package description\"" >> $@
	@echo "readme = \"README.md\"" >> $@
	@echo "authors = [{name = \"Your Name\", email = \"your.email@example.com\"}]" >> $@
	@echo "dependencies = [" >> $@
	@sed -e 's/^/    "/' -e 's/$$/"/' -e 's/==/~=/' requirements.txt | sed '$$!s/$$/,/' >> $@
	@echo "]" >> $@
	@echo "requires-python = \">= 3.11\"" >> $@
	@echo "[tool.hatch.build.targets.wheel]" >> $@
	@echo "include = [\"$(SRC_DIR)\", \"tests/**/*\", \"pyproject.toml\", \"README.md\", \"LICENSE\"]" >> $@

docs:
	@echo "Generating Doxyfile"
	@echo "PROJECT_NAME           = $(PACKAGE_NAME)" > Doxyfile
	@echo "INPUT                  = $(SRC_DIR)" >> Doxyfile
	@echo "OUTPUT_DIRECTORY       = $(DOCS_DIR)" >> Doxyfile
	@echo "OPTIMIZE_OUTPUT_PYTHON = YES" >> Doxyfile
	@echo "PYTHON_DOCSTRING       = YES" >> Doxyfile
	@echo "PREDEFINED             = __all__" >> Doxyfile
	@echo "FILE_PATTERNS          = *.py" >> Doxyfile
	@echo "AUTOBRIEF              = NO" >> Doxyfile
	@echo "QT_AUTOBRIEF           = NO" >> Doxyfile
	@echo "JAVADOC_AUTOBRIEF      = NO" >> Doxyfile
	@echo "MARKDOWN_SUPPORT       = NO" >> Doxyfile
	@echo "AUTOLINK_SUPPORT       = NO" >> Doxyfile
	@echo "GENERATE_LATEX         = YES" >> Doxyfile
	@echo "GENERATE_HTML          = NO" >> Doxyfile
	@echo "LATEX_OUTPUT           = latex" >> Doxyfile
	@echo "EXTRACT_ALL            = NO" >> Doxyfile
	@echo "EXTRACT_PRIVATE        = NO" >> Doxyfile
	@echo "EXTRACT_STATIC         = NO" >> Doxyfile
	@echo "EXTRACT_LOCAL_CLASSES  = NO" >> Doxyfile
	@echo "HAVE_DOT               = NO" >> Doxyfile
	@echo "RECURSIVE              = YES" >> Doxyfile
	@echo "QUIET                  = YES" >> Doxyfile
	@echo "WARNINGS               = NO" >> Doxyfile
	@echo "WARN_IF_UNDOCUMENTED   = NO" >> Doxyfile
	@echo "WARN_IF_DOC_ERROR      = NO" >> Doxyfile
	@echo "WARN_NO_PARAMDOC       = NO" >> Doxyfile
	doxygen Doxyfile
	@echo "Compiling LaTeX to PDF"
	cd $(DOCS_DIR)/latex && pdflatex refman.tex
	cd $(DOCS_DIR)/latex && pdflatex refman.tex
	@echo "Cleaning up auxiliary files"
	find $(DOCS_DIR)/latex -type f ! -name "refman.pdf" -delete
	mv $(DOCS_DIR)/latex/refman.pdf $(DOCS_DIR)/$(PACKAGE_NAME)_documentation.pdf
	rmdir $(DOCS_DIR)/latex
	@rm Doxyfile
	@echo "Documentation generated: $(DOCS_DIR)/$(PACKAGE_NAME)-$(VERSION)_documentation.pdf"

install: build
	$(PYTHON) -m pip install $(OUT_DIR)/$(PACKAGE_NAME)-$(VERSION)-py3-none-any.whl

depens: requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

dev-install: pyproject.toml
	$(PYTHON) -m pip install -e .

clean:
	rm -rf dist build *.egg-info
	rm -f pyproject.toml

test:
	pytest tests

lint:
	pylint $(SRC_DIR)
	ruff check $(SRC_DIR)

type-check:
	mypy $(SRC_DIR)

release: clean build lint type-check test docs
	@echo "Release $(VERSION) is ready"
