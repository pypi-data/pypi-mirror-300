ROOT := $(shell pwd)

.PHONY: build run run-vocabuilder gen_archive

USERNAME := dockeruser
TAG_NAME := pyml-life-expectancy
GIT_ARCH_NAME := git_repo.tar.gz

gen_archive:
	@echo "Checking for unstaged and untracked files..."
	@./check_unstaged_files.sh
	@echo "Generating Git archive of current HEAD including staged files..."
	@cd .. && \
	git ls-files -s | awk '{print $$4}' | tar -czf docker/$(GIT_ARCH_NAME) -T -
#		git archive -o docker/$(GIT_ARCH_NAME) --format=tar.gz HEAD


build: gen_archive
	@echo "Building Docker image..."
	@docker build --build-arg HOST_UID=$(shell id -u) \
	              --build-arg HOST_GID=$(shell id -g) \
	              --build-arg USERNAME=$(USERNAME) \
				  --build-arg GIT_ARCH=$(GIT_ARCH_NAME) \
	              -t $(TAG_NAME) .
	@rm $(GIT_ARCH_NAME) # remove the archive file

run:
	@echo "Running Docker container..."
	@mkdir -p $(ROOT)/share
	@if command -v xhost >/dev/null 2>&1; then \
	    mkdir -p $(ROOT)/share; \
		xhost +local:docker ; \
		docker run --user $(shell id -u):$(shell id -g) \
		           -v $(ROOT)/share:/home/$(USERNAME)/share \
		           -v /tmp/.X11-unix:/tmp/.X11-unix \
		           -e DISPLAY=$(DISPLAY) \
		           -it --rm $(TAG_NAME) ; \
		xhost -local:docker; \
	else \
		echo "xhost command not found. Please ensure X11 is set up correctly."; \
		exit 1; \
	fi

