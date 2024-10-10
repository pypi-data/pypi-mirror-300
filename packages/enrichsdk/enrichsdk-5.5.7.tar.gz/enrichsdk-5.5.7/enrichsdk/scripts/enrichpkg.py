#!/usr/bin/env python3


# Core
import os
import sys
import pip
import base64
import subprocess
import textwrap
import json
import imp
import yaml
import traceback
import pkg_resources
import logging, traceback
import pyfiglet
import warnings
import platform

# thirdparty
import click
from pythonjsonlogger import jsonlogger
from prompt_toolkit import prompt

# Disable warnings
import urllib3
urllib3.disable_warnings()

# self
import enrichsdk
from enrichsdk import (
    package,
    datasets,
    api as sdkapi,
    lib,
    featurestore as fslib,
    utils,
)
from enrichsdk.package.validators import GenericDescValidator

class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):

        if cmd_name == 'bootstrap':
            cmd_name = 'init'

        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        print(self.list_commands(ctx))
        print(cmd_name)
        matches = [x for x in self.list_commands(ctx)  if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def get_backend_obj(ctx, backend):
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    backends = config["backends"]

    relevant = None
    for b in backends:
        if (b.get("server", None) == backend) or (b.get("name", None) == backend):
            relevant = b
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))

    # Decode the key before accessing
    for col in ['key', 'htpasswd_user', 'htpasswd_pwd']:
        value = base64.b64decode(relevant[col].encode("utf-8")).decode("utf-8")
        relevant[col] = value

    backend = sdkapi.Backend(relevant)
    return backend

@click.group(cls=AliasedGroup)
def process():
    """
    init/test/install Enrich modules and access server

    \b
    Getting started:
       version:  Version of this sdk
       start:    First time instructions
       env:      Setup/check the setup

    \b
    Development:
       init:   Bootstrap modules including transforms*
       test:   Test transforms, manage datasets
       doodle: Access Doodle metadata server
       manage: Manage services such as mongo

    \b
    Server:
       api:       Access the server API

    \b
    Utils:
       sample:    Sample data for sharing

    \b
    Helpers:
       show-log:  Pretty print log output

    *Command used to be called bootstrap
    """
    pass


@click.command("version", hidden=True)
def _version():
    """
    Show version
    """
    print(enrichsdk.__version__)


@click.command("start", hidden=True)
@click.option("--minimal/-m", default=False)
def _start(minimal):
    """
    Instructions to get started
    """

    opsys = platform.system()
    result = pyfiglet.figlet_format("Enrich SDK", font="slant")
    print(result)

    home = os.environ["HOME"]
    if "ENRICH_ROOT" in os.environ:
        enrich_root = os.environ["ENRICH_ROOT"]
    else:
        enrich_root = os.path.join(os.getcwd(), "enrich")

    if "VIRTUAL_ENV" in os.environ:
        venv_root = os.environ["VIRTUAL_ENV"]
        venv_name = os.path.abspath(os.path.basename(venv_root))
        install_settings = [
            'echo "source {}/bin/activate" > $ENRICH_ROOT/env.sh'.format(venv_root),
            'echo "#workon {}" >> $ENRICH_ROOT/env.sh'.format(venv_name),
        ]
    elif "CONDA_PREFIX" in os.environ:
        venv_root = os.environ["CONDA_PREFIX"]
        venv_name = os.path.basename(venv_root)
        install_settings = [
            'echo "conda activate {}" >> $ENRICH_ROOT/env.sh'.format(venv_name),
        ]
    else:
        print("Please use virtualenvwrapper or conda to install sdk")
        return

    enrich_root_prompt =   "$ENRICH_ROOT" if opsys != "Windows" else "%ENRICH_ROOT%"

    steps = [
        {
            "description": "Understand Enrich and SDK",
        },
        {
            "description": "set ENRICH_ROOT and populate. This will create the directory structure required to make enrich work. You will see several directories that are required at various points in the lifecycle of the project",
            "cmd": [
                f"export ENRICH_ROOT={enrich_root}" if opsys != "Windows" else f"set ENRICH_ROOT={enrich_root}",
                "enrichpkg env populate",
            ],
        },
        {
            "description": "Check and update siteconf and versionmap. Siteconf stores site-specific configuration required by pipelines including credentials, security policy etc.. Versionmap (which you dont have to worry about right now) allows the pipelines to track the version information of all the modules deployed",
            "cmd": [
                "enrichpkg env check",
                "cat $ENRICH_ROOT/etc/siteconf.json" if opsys != "Windows" else "type %ENRICH_ROOT%\\etc\\siteconf.json",
            ],
        },
        {
            "description": "[OPTIONAL] For complex deployments, create an environment/context file. Talk to Scribble before you use this.",
            "cmd": "enrichpkg env sample-context > context.yaml",
        },
        {
            "description": "[OPTIONAl] Create a simple settings file. This is useful in everyday execution. You can simply source this script and then run the enrichpkg",
            "cmd": [
                "# file to be sourced before you start working. use the appropriate",
                "# environment activation mechanism. Check the script generated by",
                "# populate",
                "",
                "cat $ENRICH_ROOT/env.sh",
                'echo "source $ENRICH_ROOT/env.sh" >> $HOME/.bashrc',
                "",
                "# If the file doesnt exist or doesnt look right, use the following"
            ]
            + install_settings
            + [
                'echo "export ENRICH_ROOT={}" >> $ENRICH_ROOT/env.sh'.format(
                    enrich_root
                ),
                'echo "source $ENRICH_ROOT/etc/django-env" >> $ENRICH_ROOT/env.sh'
            ],
        } if opsys != "Windows" else
        {
            "description": "[OPTIONAl] Create a simple batch file to set the environment variables and activate the environment. This is useful in everyday execution. You can simply execute this script and then run the enrichpkg.",
            "cmd": [
                "@echo off",
                "REM Sample batch file wenv.bat",
                "REM modify HOME according to the Windows user",
                "set HOME=C:\\Users\\winuser",
                "REM modify ENRICH_ROOT according to installation folder",
                "set ENRICH_ROOT=C:\\enrichapp\\enrich",
                "REM modify VENV_DIR according to python virtual env installation",
                "set VENV_DIR=C:\\enrichapp\\venv",
                "REM activate the virtual environment",
                "%VENV_DIR%\\Scripts\\activate"
            ]
        },
        {
            "description": "Customer directory has actual code repositories. Your code will be stored here. Change dir to $ENRICH_CUSTOMERS. You will find that it is empty but dont panic",
            "cmd": "cd "+os.path.join(enrich_root_prompt, "customers")
        },
        {
            "cmd": [
                "#To handle python paths etc. avoid spaces and hyphen in the names",
                "git clone https://github.com/pingali/enrich-acme.git acme",
            ],
            "description": "GIT checkout an example code repository. This time it is from a company called acme. You will have a similar repository and checkout. The process is similar whether it is on the local machine or on the server",
        },
        {
            "cmd": "cd " + os.path.join(enrich_root_prompt, "customers", "acme"),
            "description": "Change to checked out repository",
        },
        {
            "cmd": [
                "# if acme is already populated",
                "enrichpkg init repo -p ."
            ],
            "description": "[OPTIONAL] Initialize the repo, if not already done. In case of Acme you dont have tEnrich requires a particular structure to the repository. You will notice __init__.py and enrich.json. These are files that tell the Enrich system what is present where.",
        },
        {
            "cmd": [
                "# Typically usecases have first letter in capital",
                "enrichpkg init usecase -p Marketing",
            ],
            "description": "[OPTIONAL] The code is organized in terms of projects or usecase groups. Create one usecase, say Marketing. In case of acme, you dont have to do this. Just look around."
        },
        {
            "cmd": [
                "cd Marketing"
            ],
            "description": "Change to usecase"
        },
        {
            "description": "Initialize a simple transform. Transform is a python module. It could be a single file, directory or a full package.",
            "cmd": [
                "# Will create an example hello world script",
                "enrichpkg init transform-helloworld -p " + os.path.join("transforms", "helloworld.py")
            ]
        },
        {
            "description": "[OPTIONAL] You could do more complex transforms. You can initialize a python module directory or a full package. You can come back to this later on",
            "cmd": [
                "# Will create a more simple python script that is more complex than helloworld",
                "enrichpkg init transform-simple -p " + os.path.join("transforms", "simplefile.py"),
                "",
                "# Will create a python module (a full directory)",
                "enrichpkg init transform-simple -p " + os.path.join("transforms", "simpledir"),
                "",
                "# Will create a python package. Dont use this unless you are sure",
                "enrichpkg init transform-package -p " + os.path.join("transforms", "simplepackage"),
            ],
        },
        {
            "cmd": [
                "# Add any requirements and install them",
                "cat ../requirements.txt" if opsys != "Windows" else "type ..\\requirements.txt",
                "pip install -r " + os.path.join("..", "requirements.txt")
            ],
            "description": "[OPTIONAL] Each repository has additional requirements going beyond what enrich requires, e.g., a module to connect to snowfake. Install these repo-specific requirements to enable the transform to run. You can come back to this later on",
        },
        {
            "cmd": [
                "vi " + os.path.join("transforms", "helloworld.py")
            ],
            "description": "Eyeball the helloworld transform",
        },
        {
            "cmd": [
                "enrichpkg test transform " + os.path.join("transforms", "helloworld.py")
            ],
            "description": "You have to locally test the transform to make sure everything is working as planned including the parameters"
        },
        {
            "cmd": [
                "enrichpkg init pipeline -p " + os.path.join("pipelines", "conf", "helloworld.py")
            ],
            "description": "Transforms are like plugins. They have to be incorporated into a pipeline to ensure that it runs on server. Initialize a pipeline. Note the path to the pipelines. They have a particular structure as described in the SDK and at particular location. The Enrich execution engine searches these paths",
        },
        {
            "cmd": [
                "enrichpkg test conf --capture " + os.path.join("pipelines", "conf", "helloworld.py")
            ],
            "description": "Sanity check the pipeline to ensure that everything is as per plan. Note that in some cases where credentials are being accessed etc. we will have additional setup"
        },
        {
            "cmd": [
                "# prefect is the default workflow engine",
                "enrichpkg init prefectjob -p " + os.path.join("workflows", "prefect", "daily.py")
            ],
            "description": "A workflow allows us to combine multiple pipelines and multiple runs of each into a single activity. We use prefect for the same. We could use something else. We dont need prefect cloud though. We will run the workflow from our scheduler"
        },
        {
            "cmd": [
                "cat workflows/prefect/daily.py" if opsys != "Windows" else "type workflows\\prefect\\daily.py",
                "python3 " + os.path.join("workflows", "prefect", "daily.py")
            ],
            "description": "Check the content of the workflow. Once ready you can include this workflow in the nextdoor scheduler"
        },
    ]

    for i, s in enumerate(steps):
        print("[{:2}] {}".format(i + 1, "\n".join(textwrap.wrap(s["description"]))))
        print("")
        if minimal:
            continue
        if "cmd" in s:
            if isinstance(s["cmd"], str):
                cmds = [s["cmd"]]
            else:
                cmds  = s["cmd"]
            for c in cmds:
                if not c.startswith("#") and len(c) > 0:
                    print("    $ {}".format(c)) if opsys != "Windows" else print("    {}".format(c))
                else:
                    print("    {}".format(c))
        print("")


@click.command("init", hidden=True)
@click.argument("component")
@click.option(
    "--path", "-p", required=False, default=None, help="Directory where the files should be stored"
)
@click.option(
    "--template",
    "-t",
    required=False,
    default=None,
    help="Template to override the defaults",
)
@click.option("--context", required=False, default=None, help="Environment file")
def init_(component, path, template, context):
    """
    Bootstrap/initialize a fresh module

    Modules currently supported include transform, pipeline and asset. Use
    help to list possible components::

         enrichpkg init help*

    For now only the transforms and models are testable locally
    without the need for a test server.

    In future we expect to more comprehensively support the
    development of all modules.

    A custom template can be provided as well.

    * init command used to be called bootstrap

    """

    components = [
        ["repo" , "A new git repository"],
        ["usecase", "A collection of transforms, pipelines, assets and workflows"],
        ["transform-package", "A complex transform that is structured as a full python package"],
        ["transform-simple", "A transform structured as a python module"],
        ["transform-helloworld", "A simple hello world transform for study"],
        ["transform-query", "A  transform that uses a pre-existing database querying module"],
        ["transform-metrics", "A  transform that uses a pre-existing metrics module"],
        ["transform-iris", "Simple Iris post-processing example"],
        ["asset", "A reusable library "],
        ["dashboard", "A django app that fits the Enrich Dashboard framework"],
        ["pipeline", "A pipeline configuration"],
        ["prefectjob", "Prefect workflow template"],
        ["app-index", "Index page of a new app"],
        ["datasets", "Datasets specification file"],
        ["rscript", "R-Script template"],
        ["pyscript", "A python script template"],
        ["singlepageapp", "Single page app"]
    ]

    if component not in [c[0] for c in components]:
        print("The following components are supported:\n")
        for c in components:
            print(f"   {c[0]:20}: {c[1]}")
        print("\nUse the component name like this")
        print("    enrichpkg init repo -p <path>")
        print("")
        print("You can define your own templates as well. Please use the -t option\n")
        return

    if path is None:
        print("Path should specified using -p option")
        return

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        raise
    context.set_env()

    if not package.checkenv(validate_only=True):
        print("Environment is incomplete")
        print("Try: enrichpkg env check")
        return

    package.bootstrap(component, path, template)


@click.command("show-log", hidden=True)
@click.argument("logfile")
def _show_log(logfile):
    """
    Pretty-print run log
    """

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    package.print_log(logfile)


@click.group("env", hidden=True)
@click.pass_context
def envsetup(ctx):
    """
    Setup the environment. Environment includes:\n
      \b
      (a) Workspace for enrich to work
      (b) Minimal configuration

    This can be specified using environment variables
    and/or 'context' file.

    The absolute minimal required environment variable
    is ENRICH_ROOT (path to enrich workspace e.g.,
    ~/enrich)
    """

    ctx.ensure_object(dict)


@envsetup.command("sample-context")
@click.option("--root", "-r", default=None, help="Root of enrich")
def _context_generate(root):
    """
    Generate sample context file
    """

    if root is not None:
        os.environ["ENRICH_ROOT"] = os.path.abspath(root)
    elif "ENRICH_ROOT" not in os.environ:
        os.environ["ENRICH_ROOT"] = os.path.expandvars("$HOME/enrich")

    context = lib.Context()
    context = context.asdict()

    if "siteconf" not in context:
        context["siteconf"] = os.path.join(context["ENRICH_ETC"], "siteconf.json")

    print("Please store this in context.yaml",file=sys.stderr)
    print("Minimum required valid paths include: siteconf, versionmap, enrich_data",file=sys.stderr)
    print("Example: enrichpkg api --context context.yaml ...",file=sys.stderr)
    print("----",file=sys.stderr)
    print(yaml.dump(context, indent=4))


@envsetup.command("sample-versionmap")
def _versionmap():
    """
    Generate sample versionmap
    """

    print(
        "Please store this in versionmap.json. Default is $ENRICH_ROOT/etc/versionmap.json",
        file=sys.stderr
    )
    print("Update context.yaml with this versionmap path", file=sys.stderr)
    print("----", file=sys.stderr)
    print(package.get_sample_versionmap())


@envsetup.command("dump-versionmap")
def _dump_versionmap():
    """
    Show versionmap
    """

    timestamp, versionmap = lib.read_versionmap()
    print(json.dumps(versionmap, indent=4))

@envsetup.command("sample-siteconf")
def _siteconf():
    """
    Generate sample siteconf
    """

    print(
        "Please store this in siteconf.json. Default is $ENRICH_ROOT/etc/siteconf.json",
        file=sys.stderr
    )
    print("Update context.yaml with this siteconf path",file=sys.stderr)
    print("----",file=sys.stderr)
    print(package.get_sample_siteconf())

@envsetup.command("sample-djangoenv")
def _env():
    """
    Sample django-env environment variables.
    """

    opsys = platform.system()  # WINDOWS PORTING
    print(
        "Please store this in django-env. Default is $ENRICH_ROOT/etc/django-env",
        file=sys.stderr
    ) if opsys != "Windows" else print(
        "Please store this in django-env.bat. Default is %ENRICH_ROOT%\\etc\\django-env.bat",
        file=sys.stderr
    )
    print(package.get_sample_djangoenv())


@envsetup.command("show-credential")
@click.argument("name")
def _show_cred(name):
    """
    Show credentials for a name
    """
    print(json.dumps(lib.get_credentials_by_name(name)))


@envsetup.command("populate")
@click.option("--context", default=None, help="Context file")
def _populate(context):
    """
    Populate the directories
    """
    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        print("Error! " + str(e))
        return

    context.set_env()

    package.populate(context=context.asdict())

@envsetup.command("prepare-data-roots")
@click.option("--context", default=None, help="Context file")
def _prepare_data_roots(context):
    """
    Prepare output directories
    """
    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        print("Error! " + str(e))
        return

    context.set_env()

    package.prepare_data_roots(context=context.asdict())


@envsetup.command("check")
@click.option("--context", default=None, help="Context file")
def _checkenv(context):
    """
    Check environment
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        print("Error! " + str(e))
        return

    context.set_env()

    package.checkenv(context=context)


##########################################################
# Test command
##########################################################
@click.group("test", hidden=True)
@click.option("--context", default=None, help="Environment file")
@click.pass_context
def test(ctx, context):
    """
    Test transforms/pipelines etc.
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        raise

    context.set_env()
    ctx.ensure_object(dict)
    ctx.obj["context"] = context.asdict()


@test.command("transform")
@click.argument("pkgdir")
@click.option("--capture/--no-capture", default=True, help="Capture output")
@click.pass_context
def test_pkg(ctx, pkgdir, capture):
    """
    Unit testing of a package module (transform)
    """
    context = ctx.obj["context"]

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg env check")
        raise Exception("Environment incomplete")

    package.test_transform(pkgdir, capture, context)


@test.command("task-lib")
@click.argument("taskdir")
@click.option("--capture/--no-capture", default=True, help="Capture output")
@click.pass_context
def test_task(ctx, taskdir, capture):
    """
    Unit testing of a task library
    """

    context = ctx.obj["context"]

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg env check")
        raise Exception("Environment incomplete")

    package.test_task(taskdir, capture, context)


@test.command("conf")
@click.argument("spec")
@click.option("--capture/--no-capture", default=True, help="Capture output")
@click.pass_context
def test_conf(ctx, spec, capture):
    """
    Minimal testing of pipeline/task configuration
    """

    context = ctx.obj["context"]

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg env check")
        raise Exception("Environment incomplete")

    package.test_conf(spec, capture, context)


@click.group("data")
@click.argument("spec")
@click.option("--capture/--no-capture", default=True, help="Capture output")
@click.pass_context
def testdata(ctx, spec, capture):
    """
    Manage test data


    spec could be transform or a spec file
    """
    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg env check")
        raise Exception("Environment incomplete")

    ctx.ensure_object(dict)
    ctx.obj["spec"] = spec
    ctx.obj["capture"] = capture


@testdata.command("list")
@click.pass_context
def _testdata_list(ctx):
    """
    List available test datasets
    """

    package.testdata_action(
        "list", ctx.obj["spec"], ctx.obj["capture"], ctx.obj["context"]
    )


@testdata.command("show")
@click.argument("dataset")
@click.pass_context
def _testdata_show(ctx, dataset):
    """
    Show the details of a given dataset
    """

    package.testdata_action(
        "show", ctx.obj["spec"], ctx.obj["capture"], ctx.obj["context"], name=dataset
    )


@testdata.command(
    "run",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.argument("dataset")
@click.argument("command")
@click.pass_context
def _testdata_action(ctx, dataset, command):
    """
    Generate action commands for a dataset over a specified range

    Pass additional parameters as key-value pairs as
    shown in show.
    """

    args = dict()
    for item in ctx.args:
        args.update([item.split("=")])

    package.testdata_action(
        "action",
        ctx.obj["spec"],
        ctx.obj["capture"],
        ctx.obj["context"],
        name=dataset,
        command=command,
        **args
    )


test.add_command(testdata)

##########################################################
# Doodle
##########################################################
@click.group("doodle", hidden=True)
@click.option("--context", default=None, help="Environment file")
@click.option("--cred", default="doodle", help="Doodle credential name")
@click.pass_context
def doodle(ctx, context, cred):
    """
    Access doodle server
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        raise

    context.set_env()
    ctx.ensure_object(dict)
    ctx.obj["context"] = context.asdict()
    ctx.obj["cred"] = cred

@doodle.command("list-catalogs")
@click.pass_context
def _list_catalogs(ctx):
    """
    List catalogs
    """

    cred = enrichsdk.lib.get_credentials_by_name(ctx.obj['cred'])
    doodle = datasets.Doodle(cred)
    catalogs = doodle.list_catalogs()
    print(json.dumps(catalogs, indent=4))

@doodle.command("search-catalogs")
@click.argument("name")
@click.option("-v", "--version", default="v1")
@click.pass_context
def _search_catalogs(ctx, name, version):
    """
    Search catalogs
    """

    cred = enrichsdk.lib.get_credentials_by_name(ctx.obj['cred'])
    doodle = datasets.Doodle(cred)
    catalogs = doodle.search_catalogs(name=name,version=version)
    print(json.dumps(catalogs, indent=4))

@doodle.command("list-sources")
@click.pass_context
def _list_sources(ctx):
    """
    List sources
    """

    cred = enrichsdk.lib.get_credentials_by_name(ctx.obj['cred'])
    doodle = datasets.Doodle(cred)
    sources = doodle.list_sources()
    print(json.dumps(sources, indent=4))

@doodle.command("search-sources")
@click.argument("name")
@click.option("-v", "--version", default="v1")
@click.pass_context
def _search_sources(ctx, name, version):
    """
    Search sources
    """

    cred = enrichsdk.lib.get_credentials_by_name(ctx.obj['cred'])
    doodle = datasets.Doodle(cred)
    sources = doodle.search_sources(name=name,version=version)
    print(json.dumps(sources, indent=4))

@doodle.command("show-source")
@click.argument('source_id')
@click.pass_context
def _show_source(ctx, source_id):
    """
    Show source
    """

    cred = enrichsdk.lib.get_credentials_by_name(ctx.obj['cred'])
    doodle = datasets.Doodle(cred)
    source = doodle.get_source(source_id)
    print(json.dumps(source, indent=4))


@doodle.command("update-source")
@click.argument('source_id')
@click.argument('filename')
@click.pass_context
def _update_source_metadata(ctx, source_id, filename):
    """
    List sources
    """

    cred = enrichsdk.lib.get_credentials_by_name(ctx.obj['cred'])
    doodle = datasets.Doodle(cred)

    try:
        update = json.load(open(filename))
    except Exception as e:
        print("Error!", e)
        print("Unable to read filename. It should be a valid json file")

    result = doodle.update_source(source_id, update)
    print(json.dumps(result, indent=4))

#########################################
# API
#########################################
@click.group(hidden=True)
@click.option("--config", default=None, help="API Config File")
@click.pass_context
def api(ctx, config):
    """
    Access Enrich Server
    """

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg env check")
        raise Exception("Environment incomplete")

    alt = os.path.expandvars("$ENRICH_ETC/api.json")
    if config is None:
        config = alt

    # Write a default
    default = {"schema": "v1:api:enrich", "backends": []}
    if not os.path.exists(config):
        with open(config, "w") as fd:
            fd.write(json.dumps(default, indent=4))

    ctx.ensure_object(dict)
    ctx.obj["config"] = config


####################################
# Support for sampling data
####################################
@click.group("sample", hidden=True)
@click.pass_context
def sample(ctx):
    """
    Sample data from blockstores
    """
    pass


@sample.command("crawl")
@click.argument("root")
@click.option("--ext", default="json", help="Extension of files to look for")
@click.pass_context
def crawl(ctx, root, ext):
    """
    Crawl the root to find possible files

    Args:
       root: Path in blockstore with s3:// prefix
    """

    utils.sample_crawl(root, ext)


@sample.command("cat")
@click.argument("path")
@click.pass_context
def crawl(ctx, path):
    """
    Show the contents of path

    Args:
       path: Path to file in blockstore with s3:// prefix
    """

    utils.sample_cat(path)


####################################
# Configure access to server
####################################
@click.group()
@click.pass_context
def config(ctx):
    """
    Configure access to Enrich Server
    """
    pass


@config.command("init")
@click.pass_context
def _config_init(ctx):
    """
    Initialize the config file
    """
    default = {
        "schema": "v1:api:enrich",
        "backends": [],
        "services": [],
    }
    filename = ctx.obj["config"]
    if os.path.exists(filename):
        print("API access configuration file already exists. Please remove it first")
        print("See:", filename)
        return

    with open(filename, "w") as fd:
        fd.write(json.dumps(default, indent=4))

    print("Initialized config")


@config.command("list")
@click.pass_context
def _config_list(ctx):
    """
    List available backends/services
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    print("Backends")
    print("-----")
    backends = config["backends"]
    for b in backends:
        key = base64.b64decode(b["key"].encode("utf-8")).decode("utf-8")
        try:
            print("{} [{} @ {}]".format(b["name"], key, b["server"]))
        except:
            pass

    print("\n")
    print("Services")
    print("-----")
    services = config.get("services", [])
    for s in services:
        try:
            print("{} [{}]".format(s["name"], s["path"]))
        except:
            pass


@config.command("backend-add")
@click.argument("name")
@click.argument("server")
@click.pass_context
def _backend_add(ctx, name, server):
    """
    Add backend
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    key = prompt(">API Key: ")
    htpasswd_user = prompt(">HTPasswd Username: ")
    htpasswd_pwd = prompt(">HTPasswd Password: ",)

    if len(key) == 0 or len(htpasswd_user) == 0 or len(htpasswd_pwd) == 0:
        print("Empty APIKey or HTPasswd username or password")
        return

    # Encode the key before storing
    key = base64.b64encode(key.encode("utf-8")).decode("utf-8")
    htpasswd_user  = base64.b64encode(htpasswd_user.encode("utf-8")).decode("utf-8")
    htpasswd_pwd  = base64.b64encode(htpasswd_pwd.encode("utf-8")).decode("utf-8")

    backends = config["backends"]
    missing = True
    for b in backends:
        if ("server" in b) and (b["server"] == server):
            b["name"] = name
            b["server"] = server
            b["key"] = key
            b["htpasswd_user"] = htpasswd_user
            b["htpasswd_pwd"] = htpasswd_pwd
            missing = False
            break

    if missing:
        backends.append({
            "name": name,
            "server": server,
            "key": key,
            "htpasswd_user": htpasswd_user,
            "htpasswd_pwd": htpasswd_pwd,
        })

    with open(filename, "w") as fd:
        fd.write(json.dumps(config, indent=4))

    print("Added {}".format(name))


@config.command("backend-remove")
@click.argument("name")
@click.pass_context
def _backend_remove(ctx, name):
    """
    Add backend
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    backends = config["backends"]
    missing = True
    updated = [
        b
        for b in backends
        if ((b.get("server", None) != name) and (b.get("name", None) != name))
    ]

    if len(backends) == len(updated):
        raise Exception("Backend not found: {}".format(name))

    config["backends"] = updated

    with open(filename, "w") as fd:
        fd.write(json.dumps(config, indent=4))

    print("Removed {}".format(name))


@config.command("service-add")
@click.argument("name")
@click.argument("path")
@click.pass_context
def _service_add(ctx, name, path):
    """
    Add URL
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    if "services" not in config:
        config["services"] = []

    services = config["services"]
    missing = True
    for s in services:
        if ("name" in s) and (s["name"] == name):
            s["name"] = name
            s["path"] = path
            missing = False
            break

    if missing:
        services.append({"name": name, "path": path})

    with open(filename, "w") as fd:
        fd.write(json.dumps(config, indent=4))

    print("Added {}".format(name))


@config.command("service-remove")
@click.argument("name")
@click.pass_context
def _service_remove(ctx, name):
    """
    Remove service
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    services = config["services"]
    missing = True
    updated = [s for s in services if s.get("name", None) != name]

    if len(services) == len(updated):
        raise Exception("Service not found: {}".format(name))

    config["services"] = updated

    with open(filename, "w") as fd:
        fd.write(json.dumps(config, indent=4))

    print("Removed {}".format(name))


@click.group()
@click.argument("backend")
@click.pass_context
def show(ctx, backend):
    """
    Access a backend
    """
    ctx.obj["backend"] = get_backend_obj(ctx, backend)


@click.command("health")
@click.argument("backend")
@click.pass_context
def _health(ctx, backend):
    """
    Show system health
    """

    backend = get_backend_obj(ctx, backend)
    result = backend.health()

    status = result["status"]
    if status in ["failure", "error"]:
        print("Failure while accessing backend")
        if "error" in result:
            print("Reason:", result["error"])
        return

    sdkapi.draw_dict(backend, "Health", result)


@click.command("app-list")
@click.argument("backend")
@click.pass_context
def _app_list(ctx, backend):
    """
    Show apps available
    """

    backend = get_backend_obj(ctx, backend)
    try:
        result = backend.app_list()
        print(json.dumps(result, indent=4))
    except:
        traceback.print_exc()

@click.command("app-detail")
@click.argument("backend")
@click.argument("name")
@click.pass_context
def _app_detail(ctx, backend,name):
    """
    Show detail of an app
    """

    backend = get_backend_obj(ctx, backend)
    try:
        result = backend.app_detail(name)
        print(json.dumps(result, indent=4))
    except:
        traceback.print_exc()


@click.command("pipeline-runs")
@click.argument("backend")
@click.argument("usecase")
@click.argument("pipeline")
@click.pass_context
def _run_list(ctx, backend, usecase, pipeline):
    """
    Show available runs for pipeline
    """

    backend = get_backend_obj(ctx, backend)
    result = backend.run_list(usecase, pipeline)

    status = result["status"]
    if status in ["failure", "error"]:
        print("Failure while accessing backend")
        if "error" in result:
            print("Reason:", result["error"])
        if "message" in result:
            print("Reason:", result["message"])
        return

    result["data"] = sorted(result["data"], key=lambda r: r["start_time"], reverse=True)

    print(json.dumps(result['data'], indent=4))
    #columns = ["runid", "status", "start_time", "end_time"]
    #sdkapi.draw(
    #    backend, "run-list", result['data'], columns, {"Usecase": usecase, "Pipeline": pipeline}
    #)

@click.group("scheduler")
@click.argument("backend")
@click.pass_context
def scheduler(ctx, backend):
    """
    Access scheduler at backend
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    backends = config["backends"]

    relevant = None
    for b in backends:
        if (b.get("server", None) == backend) or (b.get("name", None) == backend):
            relevant = b
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))

    # Decode the key before accessing
    for col in ['key', 'htpasswd_user', 'htpasswd_pwd']:
        value = base64.b64decode(relevant[col].encode("utf-8")).decode("utf-8")
        relevant[col] = value

    backend = sdkapi.Backend(relevant)
    ctx.obj["backend"] = backend


@scheduler.command("list")
@click.pass_context
def _scheduler_list(ctx):
    """
    Show the scheduled jobs
    """
    backend = ctx.obj['backend']
    try:
        result = backend.scheduler_jobs_list()

        jobs = result['jobs']

        #print(json.dumps(jobs, indent=4))
        for j in jobs:
            schedule = "%(minute)s %(hour)s %(day)s %(month)s %(day_of_week)s" % j
            j['cron'] = schedule
            for col in ['minute', 'hour', 'day', 'month', 'day_of_week']:
                j.pop(col, None)

        sdkapi.draw_dict(backend, "Scheduler List", jobs)
    except:
        traceback.print_exc()

@show.command("run-detail")
@click.argument("usecase")
@click.argument("pipeline")
@click.argument("runid")
@click.pass_context
def _run_detail(ctx, usecase, pipeline, runid):
    """
    Show detail of a given run
    """

    backend = ctx.obj["backend"]
    result = backend.run_detail(usecase, pipeline, runid)

    status = result["status"]
    if status in ["failure", "error"]:
        print("Failure while accessing backend")
        if "error" in result:
            print("Reason:", result["error"])
        return

    sdkapi.draw_run_detail(
        backend,
        "run-detail",
        result,
        {"Usecase": usecase, "Pipeline": pipeline, "RunID": runid},
    )


@show.command("tasks")
@click.argument("usecase")
@click.pass_context
def _tasks(ctx, usecase):
    """
    Show available tasks
    """

    backend = ctx.obj["backend"]
    result = backend.tasks(usecase)

    status = result["status"]
    if status in ["failure", "error"]:
        print("Failure while accessing backend")
        if "error" in result:
            print("Reason:", result["error"])
        return

    data = result["data"]
    for d in data:
        d["description"] = d["description"][:20]
        runs = sorted(d["runs"], reverse=True)
        if len(runs) > 0:
            d["lastrun"] = runs[0]
            d["runs"] = len(runs)
        else:
            d["lastrun"] = ""
            d["runs"] = 0

    columns = ["usecase", "name", "description", "path", "runs", "lastrun"]
    sdkapi.draw(
        backend,
        "tasks",
        result,
        columns,
        {
            "Usecase": usecase,
        },
    )


@show.command("task-run-list")
@click.argument("usecase")
@click.argument("task")
@click.pass_context
def _task_runs(ctx, usecase, task):
    """
    Show available runs for task
    """

    backend = ctx.obj["backend"]
    result = backend.task_run_list(usecase, task)

    status = result["status"]
    if status in ["failure", "error"]:
        print("Failure while accessing backend")
        if "error" in result:
            print("Reason:", result["error"])
        return

    result["data"] = sorted(result["data"], key=lambda r: r["start_time"], reverse=True)

    columns = ["runid", "status", "start_time", "end_time"]
    sdkapi.draw(
        backend, "task-run-list", result, columns, {"Usecase": usecase, "Task": task}
    )


@show.command("task-run-detail")
@click.argument("usecase")
@click.argument("task")
@click.argument("runid")
@click.pass_context
def _task_run_detail(ctx, usecase, task, runid):
    """
    Show detail of a given run
    """

    backend = ctx.obj["backend"]
    result = backend.task_run_detail(usecase, task, runid)

    status = result["status"]
    if status in ["failure", "error"]:
        print("Failure while accessing backend")
        if "error" in result:
            print("Reason:", result["error"])
        return

    sdkapi.draw_run_detail(
        backend,
        "run-detail",
        result,
        {"Usecase": usecase, "Task": task, "RunID": runid},
    )


@click.group()
@click.argument("backend")
@click.argument("service")
@click.pass_context
def featurestore(ctx, backend, service):
    """
    Access featurestore at backend
    """
    try:
        filename = ctx.obj["config"]
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj["config"]))

    backends = config["backends"]

    relevant = None
    for b in backends:
        if (b.get("server", None) == backend) or (b.get("name", None) == backend):
            relevant = b
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))

    # Decode the key before accessing
    key = base64.b64decode(relevant["key"].encode("utf-8")).decode("utf-8")
    relevant["key"] = key

    backend = sdkapi.Backend(relevant)
    ctx.obj["backend"] = backend

    # Lookup the service as well..
    services = config["services"]
    relevant = None
    for s in services:
        if s.get("name", None) == service:
            relevant = s
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))
    ctx.obj["service"] = s


@featurestore.command("post")
@click.argument("filename")
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def _post(
    ctx,
    filename,
    debug,
):
    """
    Post json to server
    """

    backend = ctx.obj["backend"]
    service = ctx.obj["service"]

    response = fslib.post(
        backend=backend, service=service, filename=filename, debug=debug
    )
    print(response)


@featurestore.command("generate")
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def _generate(ctx, debug):
    """
    Generate sample files
    """

    backend = ctx.obj["backend"]
    service = ctx.obj["service"]

    response = fslib.generate(backend=backend, service=service, debug=debug)
    print(json.dumps(response, indent=4))


@featurestore.command("download")
@click.option("--featuregroup_id", default=None)
@click.option("--run_id", default=None)
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def _spec_download(
    ctx,
    featuregroup_id,
    run_id,
    debug,
):
    """
    Download a featuregroup specification
    """

    if featuregroup_id is None and run_id is None:
        raise Exception("One of the featuregroup_id or run_id should be specified")

    backend = ctx.obj["backend"]
    service = ctx.obj["service"]

    response = fslib.download(
        backend=backend,
        service=service,
        featuregroup_id=featuregroup_id,
        run_id=run_id,
        debug=debug,
    )
    print(json.dumps(response, indent=4))


@featurestore.command(
    "search",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option("--debug/--no-debug", default=False)
@click.argument("params", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def _spec_search(ctx, debug, params):
    """
    Search for a feature spec or run
    """

    backend = ctx.obj["backend"]
    service = ctx.obj["service"]

    def error():
        print("Args should have attr=value format")
        print("Example: ....local spec search name=customer_persona")
        print("You can give django filter query name__icontains=persona")
        return

    for p in params:
        if p.count("=") != 1:
            return error()

    params = {p.split("=")[0]: p.split("=")[1] for p in params}
    if len(params) == 0:
        return error()

    response = fslib.search(
        backend=backend, service=service, params=params, debug=debug
    )

    print(json.dumps(response, indent=4))

#api.add_command(show)
#api.add_command(featurestore)
api.add_command(config)
api.add_command(_run_list)
api.add_command(_health)
api.add_command(scheduler)
api.add_command(_app_list)
api.add_command(_app_detail)

##########################################################
# Manage commands
##########################################################
@click.group("manage", hidden=True)
@click.option("--context", default=None, help="Environment file")
@click.pass_context
def manage(ctx, context):
    """
    Manage mongo/postgres etc.
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        raise

@manage.command("mongo")
@click.pass_context
def mongo_manage(ctx):
    """
    Start/stop mongo
    """

    commands = [
        "docker run --name alpha -d -p 27017:27017 mongo",
        "docker container stop alpha",
        "docker container ls"
        "docker container prune"
    ]

    for c in commands:
        print(c)


###################################
# Add to process
###################################
process.add_command(_version)
process.add_command(_start)
process.add_command(init_)
process.add_command(envsetup)
#process.add_command(api)
process.add_command(test)
process.add_command(doodle)
#process.add_command(sample)
process.add_command(manage)
process.add_command(_show_log)


def main():
    process()

if __name__ == "__main__":
    main()
