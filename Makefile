up:
	@if [ -z "$$TECH" ] || [ -z "$$FILENAME" ] || [ -z "$$ROUND" ]; then \
		echo "Erro: Variáveis TECH, FILENAME ou ROUND não definidas."; \
		exit 1; \
	fi
	docker-compose up --build

down:
	docker-compose down