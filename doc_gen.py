import os
from pathlib import Path

package_name = "wame"
output_dir = Path("docs/api")

output_dir.mkdir(parents=True, exist_ok=True)

def walk_modules(package):
    package_path = Path(package.replace(".", "/"))
    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                full_path = Path(root) / file
                module_rel_path = full_path.with_suffix("").as_posix().replace("/", ".")
                yield module_rel_path

def create_md(module_name):
    parts = module_name.split(".")[1:]
    file_path = output_dir.joinpath(*parts).with_suffix(".md")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# {module_name}
    
```{{automodule}} {module_name}
:members:
:undoc-members:
:show-inheritance:
```"""

    file_path.write_text(content)

for mod in walk_modules(package_name):
    create_md(mod)