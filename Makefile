SHELL:=/bin/bash
.PHONY: clean plan generate apply destroy

clean:
	@echo Deleting generating terraform file and state files
	@find . | grep -P "terraform/[0-9]{4}-[0-9]{2}-[0-9]{2}-.*tf" | xargs -d"\n" rm -f || true
	@find . | grep -P "terraform/terraform.tfstate" | xargs -d"\n" rm -f || true
generate:
	@echo Generating terraform templates from YAML file
	@python terraform_generate.py
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
