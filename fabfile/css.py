from fabric.api import local
from fabric.api import task
from fabric.colors import yellow


# ----------------------------------------------------------------------------#
# VARIABLES ------------------------------------------------------------------#
# ----------------------------------------------------------------------------#


# paths
base_path           = "project/static/css"
src_path   = base_path + "/src"
css_path    = base_path + "/"

# sass execs
exec_sass_watch   = "sass -l --watch {}:{}"
exec_sass_compile = "sass --update --style compressed {}:{}"


# ----------------------------------------------------------------------------#
# TASKS ----------------------------------------------------------------------#
# ----------------------------------------------------------------------------#


@task
def watch():
    """
    start a scss "watch" process
    """
    print(yellow("\n[CSS] Watching CSS\n", bold=True))
    local(exec_sass_watch.format(src_path, css_path))


@task
def compile():
    """
    compile desktop scss to css; returns an array of css file paths
    """
    print(yellow("\n[CSS] Compiling CSS\n", bold=True))
    local(exec_sass_compile.format(src_path, css_path))
    
