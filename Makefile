# All of the pages we want to compile.
pages := index.html about.html blog.html links.html projects.html

# The default rule.
all: $(pages)

# A static pattern rule.
# It tells make that each page in $(pages) has a dependency on its respective %.html.jinja file.
# That means it knows to recompile when we update a source file.
$(pages): %.html: src/%.html.jinja

# How to compile each page.
$(pages):
	python3 j2html.py $@.jinja -o $@ -d src/

clean:
	rm $(pages)
