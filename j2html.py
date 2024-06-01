from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from bs4 import BeautifulSoup
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def print_help():
    eprint("""usage:
    python3 j2html.py input_file [-o output_file] [-d src_dir]""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        exit(-1)

    # Get the output_file if it exists.
    expect_output_path = False
    output_path = None
    for arg in sys.argv:
        if arg == "-o":
            expect_output_path = True
            continue
        if expect_output_path:
            output_path = arg
            break

    if expect_output_path and output_path == None:
        eprint("No output file specified, but -o was given.")
        exit(-1)

    # Get the src_dir if it exists.
    expect_src_dir = False
    src_dir = None
    for arg in sys.argv:
        if arg == "-d":
            expect_src_dir = True
            continue
        if expect_src_dir:
            src_dir = arg
            break

    if expect_src_dir and src_dir == None:
        eprint("No src dir specified, but -d was given.")
        exit(-1)

    # Default src_dir.
    if src_dir == None:
        src_dir = "./"

    # NOTE: The environment src_dir is prepended to both template files and the fragments they need to render.
    # I wish it *didn't* do this so we could specify only a fragments directory, but I don't know how to specify that if it exists and this works well enough for now.
    env = Environment(
        loader=FileSystemLoader(src_dir),
        autoescape=select_autoescape()
    )

    try:
        template = env.get_template(sys.argv[1])
    except:
        eprint("Could not find template:", sys.argv[1])
        exit(-1)

    try:
        rendered_template = template.render()
    except TemplateNotFound as e:
        eprint("Could not render template; could not find:", e)
        eprint("Set a source directory with -d so html fragments are visible to the environment.")
        exit(-1)

    # NOTE: Soup will separate <a> tags onto new lines, which causes a visual oddity when underlined.
    # soup = BeautifulSoup(rendered_template, 'html.parser')
    # output = soup.prettify(formatter="html")
    output = rendered_template;

    if output_path == None:
        print(output)
    else:
        try:
            f = open(output_path, "w")
        except:
            eprint("Could not open:", output_path)
            exit(-1)
        try:
            f.write(output)
        except:
            eprint("Could not write to:", output_path)
            f.close()
        f.close()
