# All of the pages we want to compile.
pages := index.html about.html posts.html links.html projects.html
posts := finding-datasets-to-map-the-undersea-cable-network.html

# The default rule.
all: $(pages) $(posts)

# A static pattern rule. Thank you https://makefiletutorial.com/#static-pattern-rules.
# It tells make that each page in $(pages) has a dependency on its respective %.html.jinja file.
# That means it knows to recompile when we update a source file.
# Also, jinja files are dependent on html fragments, so include them too.
$(pages): %.html: src/%.html.jinja src/nav_header.frag.html src/page_footer.frag.html

$(posts): %.html: src/%.html.jinja src/nav_header.frag.html src/page_footer.frag.html

# How to compile each page.
$(pages):
	python3 j2html.py $@.jinja -o $@ -d src/

$(posts):
	python3 j2html.py $@.jinja -o $@ -d src/

clean:
	rm -f $(pages)
	rm -f $(posts)
