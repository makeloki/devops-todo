.PHONY: help ansible-deploy ansible-local ansible-check

help:
	@echo "Available commands:"
	@echo "  make ansible-local  - Deploy locally using Ansible"
	@echo "  make ansible-check  - Check syntax and dry-run"
	@echo "  make ansible-deploy - Deploy to production (edit inventory first)"

ansible-local:
	@echo "🚀 Deploying locally with Ansible..."
	ansible-playbook -i ansible/hosts/inventory.ini ansible/playbooks/deploy.yml --ask-become-pass

ansible-check:
	@echo "🔍 Checking Ansible playbook syntax..."
	ansible-playbook -i ansible/hosts/inventory.ini ansible/playbooks/deploy.yml --syntax-check
	ansible-playbook -i ansible/hosts/inventory.ini ansible/playbooks/deploy.yml --check

ansible-deploy:
	@echo "🚀 Deploying to production..."
	ansible-playbook -i ansible/hosts/inventory.ini ansible/playbooks/deploy.yml
