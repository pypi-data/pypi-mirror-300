SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

.PHONY: clean help Makefile doc build

reinstall: clean uninstall install
	@echo "DONE"

help:
	@echo "Available targets:"
	@echo "  reinstall  - Clean, uninstall, and reinstall the package"
	@echo "  install    - Install the package"
	@echo "  dev        - Uninstall and install the package in editable mode"
	@echo "  uninstall  - Uninstall the package"
	@echo "  upgrade    - Upgrade the package"
	@echo "  test       - Run mypy, pylint, and pytest"
	@echo "  doc        - Generate API documentation and build HTML"
	@echo "  clean      - Remove Python cache files and build artifacts"
	@echo "  help       - Show this help message"

# help:
# 	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

install:
	pip install .

dev: uninstall
	pip install -e .[dev]

uninstall:
	pip uninstall -y aigor || echo "Not installed"

upgrade:
	pip install --upgrade .

test: 
	mypy src/aigor
	pylint src/aigor
	pytest -v -s
	
upload-test: test
	twine upload --repository testpypi dist/*

upload: build
	twine upload dist/*

build: clean
	python -m build

doc:
	# sphinx-build -b html docs/source docs/build
	sphinx-apidoc -f -o  docs/source src/aigor
	make html

clean:
	@echo "Cleaning Python cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name "build" -exec rm -rf {} +
	@find . -type d -name "*.egg-info"  -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@echo "Done!"

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
