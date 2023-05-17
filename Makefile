IMAGE_NAME = tessnt
TAG = 1.0

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run -d --name tessnt $(IMAGE_NAME):$(TAG)

.PHONY: build run
