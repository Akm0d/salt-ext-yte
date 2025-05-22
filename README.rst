===========
salt-ext-yte
===========

A Salt “renderer” plugin implementing the YTE (YAML-Template-Engine) renderer for SaltStack.  
Combines plain YAML with embedded template logic (variables, conditionals, loops, custom definitions) without leaving YAML.

Overview
--------

The YTE renderer lets you write Salt states and Pillar data in a single YAML-first syntax, with a small set of directives (`__variables__`, `__definitions__`) for setup and Python snippets. It folds into the normal Salt render pipeline and works alongside Jinja/YAML.

Features
--------

- **YTE renderer plugin** for SaltStack (loadable via `renderer: yte` in your Salt config)
- **Embedded variables**: define defaults, derive from grains/pillar, use Python expressions
- **Custom definitions**: write Python helper functions or blocks and have them execute during render
- **Standard Salt context**: access `salt`, `grains`, `pillar`, `opts`, `__proxy__`, `saltenv`, `sls`
- **Fall-through**: if no YTE directives are present, it behaves like plain YAML

Requirements
------------

- SaltStack ≥ 3006
- Python 3.10+

Installation
------------

1. **Install** the plugin via salt-pip:

   .. code-block:: bash

      salt \* pip.install salt-ext-yte

2. **Enable** the renderer in `/etc/salt/master` and/or `/etc/salt/minion`:

   .. code-block:: yaml

      renderer:
        - yaml_jinja
        - yte
        - yaml

3. **Restart** the Salt daemons:

   .. code-block:: bash

      systemctl restart salt-master
      systemctl restart salt-minion

YTE Constructs
--------------

Within any `.sls` or Pillar file rendered by YTE, you can use two special top-level keys:

1. **`__variables__`**  
   A mapping of names to Python expressions (prefixed with `?`). These expressions are evaluated once, and their results are bound as local variables.

2. **`__definitions__`**  
   A list of Python code blocks. Each block can define helper functions or mutate the variable namespace.

Example `vars.sls`
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    #!yte

    __variables__:
        ray: ?pillar.get("ray", {})
        head: ?ray.get("head", grains["master"])
        port: ?ray.get("port", 6379)
        python: ?grains["pythonexecutable"]
        win: ?(grains["os"] == "Windows")
        path: ?("C:\\ray_venv" if win else "/opt/ray_venv")
        address: ?ray.get("head_address", "")

   __definitions__:
     - |
       def reachable():
           salt["mine.update"]()
           for ip in salt["mine.get"](head, "network.fqdns"):
               if salt["network.ping"](ip, return_boolean=True, timeout=3):
                   return f"{ip}:{port}"
           return "auto"

       if not address:
           address = reachable()

State Usage Examples
--------------------

Installing ray wiht `relenv`:

.. code-block:: sls

    #!jinja|yte
    {% include 'vars.sls' %}

    relenv:
      pip.installed:
        - bin_env: ?python
        - upgrade: True

    relenv_fetch:
      cmd.run:
        - name: ?f'"{python}" -m relenv fetch'
        - require:
          - pip: relenv

   ray:
     pip.installed:
       - pkgs:
         - ?if is_head:
             "ray[default]"
           ?else:
             ray
       - bin_env: ?python

Development
-----------

1. **Install** dev dependencies:

   .. code-block:: bash

      pip install -r requirements/tests.txt

2. **Test**:

   .. code-block:: bash

      pytest

3. **Lint**:

   .. code-block:: bash

      pip install pre-commit
      pre-commit run -av

Contributing
------------

1. Fork and branch from `master`.  
2. Add tests for any new syntax.  
3. Open a PR; reference relevant issue(s); follow SaltStack plugin guidelines.
