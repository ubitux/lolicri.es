BASEURL := "."
all:
	@./gen.py "$(BASEURL)"
clean:
	$(RM) www/*.html
	$(RM) www/search-index.json
