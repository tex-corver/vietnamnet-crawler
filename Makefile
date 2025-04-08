project_path = $(shell pwd)
config_path = $(project_path)/.configs
service := $(shell basename $(project_path))
src = $(project_path)/$(shell echo $(service) | tr "-" "_")

local-run:
	CONFIG_PATH=$(config_path) python $(src)/main.py