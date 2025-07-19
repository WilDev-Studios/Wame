# Importing a Plugin

- In your program's directory, make a folder called `plugins`.
- Inside of this `plugins` folder, drag-and-drop the folder of the desired `Plugin` to install.

```yaml
project/
- plugins/
  - plugin_1_folder/
    - main.py # plugin entrypoint
    - ... # other files
  - plugin_2_folder/
    - image.png
    - main.py
  - plugin_3_folder/
    - asset.file
    - main.py
  - etc.
- main.py # engine entrypoint
- settings.json
- ... # other files
```

The `Engine` will not import plugins in the following conditions:

- If no `plugins` folder exists.
- If no subfolders inside of `plugins` exist.
- If an entrypoint `main.py` file doesn't exist inside of each subfolder.
- If the entrypoint file doesn't contain a `Plugin`-inherited class.
