up:
	@if [ -z "$$TECH" ] || [ -z "$$EXTENSION" ] || [ -z "$$ROUND" ]; then \
		echo "Erro: Variáveis TECH, EXTENSION ou ROUND não definidas."; \
		exit 1; \
	fi
	docker-compose up --build

down:
	docker-compose down