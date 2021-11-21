run:
	docker-compose up --no-deps --build
build:
	npm --prefix ./front i
	npm --prefix ./front run build
	rm -rf ./nginx/html
	mv ./front/build ./nginx/html
	docker-compose up --no-deps --build -d
stop:
	docker-compose down
clean:
	docker-compose rm -s -f
	docker-compose image rm -s -f

