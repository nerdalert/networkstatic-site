HUGO ?= hugo
PYTHON ?= python3
PAGES_BASE_URL ?= https://nerdalert.github.io/networkstatic-site/

.PHONY: dev build-review build-staging build-production-preview validate audit-assets install-theme check-hugo

install-theme:
	./scripts/install_theme.sh

check-hugo:
	./scripts/check_hugo_version.sh "$(HUGO)"

dev: check-hugo install-theme
	$(HUGO) server --environment development --baseURL http://localhost:1313/

build-review:
	./scripts/build_review.sh "$(HUGO)"

build-staging: check-hugo install-theme
	rm -rf public-staging
	$(HUGO) --environment staging --baseURL "$(PAGES_BASE_URL)" --destination public-staging --gc --minify
	$(PYTHON) scripts/audit_site.py --site public-staging --mode staging --base-url "$(PAGES_BASE_URL)" --require-content
	$(PYTHON) scripts/security_audit.py --repo . --site public-staging --include-index --include-history

build-production-preview: check-hugo install-theme
	rm -rf public-production-preview
	$(HUGO) --environment production --baseURL https://networkstatic.net/ --destination public-production-preview --gc --minify
	$(PYTHON) scripts/audit_site.py --site public-production-preview --mode production --base-url https://networkstatic.net/ --require-content --report reports/production-local-audit.json
	$(PYTHON) scripts/security_audit.py --repo . --site public-production-preview --include-index --include-history

validate:
	$(PYTHON) -m py_compile scripts/*.py
	$(PYTHON) scripts/audit_site.py --site public-staging --mode staging --base-url "$(PAGES_BASE_URL)" --require-content
	$(PYTHON) scripts/security_audit.py --repo . --site public-staging

audit-assets:
	$(PYTHON) scripts/audit_site.py --site public-staging --mode staging --base-url "$(PAGES_BASE_URL)" --require-content
