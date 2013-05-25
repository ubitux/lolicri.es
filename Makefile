BASEURL := "."
all:
	@./gen.py "$(BASEURL)"
clean:
	$(RM) www/*.html
