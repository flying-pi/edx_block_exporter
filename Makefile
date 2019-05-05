WORKDIR := $(shell pwd)

SONAR_SICRET=`cat sonar_login`
CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

SERVICE_VARIANT=cms
PYTHONPATH=$PYTHONPATH:/edx/app/edxapp/edx-platform/cms/djangoapps/:${WORKDIR}/
DJANGO_SETTINGS_MODULE=cms.envs.test
TEST_ROOT_DIR=./test_root

export SERVICE_VARIANT
export PYTHONPATH
export DJANGO_SETTINGS_MODULE

TEST_ARGS=
TEST_FILE_NAME=

help: ## Display help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

run_sonar_scanner: ## Run sonnar scaner and push statics to the https://sonarcloud.io
	sonar-scanner \
	  -Dsonar.projectKey=flying-pi_edx_block_exporter \
	  -Dsonar.organization=flying-pi-github \
	  -Dsonar.sources=. \
	  -Dsonar.host.url=https://sonarcloud.io \
	  -Dsonar.login=${SONAR_SICRET} \
	  -Dsonar.branch.name=${CURRENT_BRANCH} \
	  -Dsonar.branch.target=${CURRENT_BRANCH} \
	  -Dsonar.python.coverage.reportPaths=$(WORKDIR)/report/coverage/coverage.xml

run_test: ## Run test with root in the current directory by pytest runner
	mkdir -p ${TEST_ROOT_DIR}
	pytest --tb=native --showlocals $(TEST_ARGS) $(TEST_FILE_NAME)
	rm -R ${TEST_ROOT_DIR}

run_test_with_covarage: TEST_ARGS=--cov=$(WORKDIR)/edx_block_exporter  --cov-report xml --cov-report html
run_test_with_covarage: run_test