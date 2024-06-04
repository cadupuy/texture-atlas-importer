# Texture Atlas Importer

`texture-atlas-importer` is a Blender addon that allows you to import texture atlases and automatically create planes with correctly mapped and positioned textures.

## Installation

1. **Download the addon:**

   - Clone this repository or download the `import_texture_atlas.py` file.

2. **Install the addon in Blender:**
   - Open Blender.
   - Go to `Edit` > `Preferences` > `Add-ons`.
   - Click `Install` and select the `import_texture_atlas.py` file.
   - Check the box to enable the addon.

## Usage

1. **Open the addon interface:**

   - In the 3D view, open the `Tool` tab on the right.
   - You will see a panel named `Texture Atlas Importer`.

2. **Select the files:**

   - Use the `PNG Path` field to select the PNG file of your texture atlas.
   - Use the `JSON Path` field to select the corresponding JSON configuration file.

3. **Import the textures:**
   - Click the `Confirm` button to start the import.
   - The planes will be created with correctly mapped and positioned textures.

## Requirements

- Blender 4.1 or higher

## Features

- Import texture atlases from PNG and JSON files.
- Automatically create planes with mapped textures.
- Correctly position planes based on trimming information.

## Contributing

Contributions are welcome! To propose changes, please follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add my feature'`).
4. Push your branch (`git push origin feature/my-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
