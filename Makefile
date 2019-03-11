SHELL:=/bin/bash
.PHONY: clean plan generate apply destroy init

# pass arguments to make as described at
# https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
# If the first argument is "generate"...
ifeq (generate,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  GENERATE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(GENERATE_ARGS):;@:)
endif

init:
	@cd terraform; terraform init
clean:
	@echo Deleting generating terraform file and state files
	@find . | grep -P "terraform/[0-9]{4}-[0-9]{2}-[0-9]{2}_.*tf" | xargs -d"\n" rm -f || true
	@find . | grep -P "terraform/terraform.tfstate" | xargs -d"\n" rm -f || true

generate: clean
	@echo Generating terraform templates from YAML file
	@python terraform_generate.py $(GENERATE_ARGS)
	@cd terraform;terraform fmt
plan:
	@echo Executing terraform plan
	@cd terraform;terraform plan
apply:
	@echo Executing terraform plan
	@cd terraform;terraform apply
destroy:
	@echo Executing terraform destroy
	@cd terraform;terraform destroy
