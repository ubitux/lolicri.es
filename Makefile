BASEURL := "$(shell pwd)/www"
all:
	@./gen.py "$(BASEURL)"
