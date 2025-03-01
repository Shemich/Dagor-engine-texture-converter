# Dagor Engine Textures Converter

A Python-based tool to convert `.dds` textures into various maps (Albedo, AO, Normal, Roughness, Metal) for games powered by the Dagor Engine (e.g., War Thunder, Enlisted). 

## Features

- **Customizable Postfixes**: Define your own postfixes

## Installation

1. Clone the repository:
```git clone https://github.com/yourusername/dagor-texture-converter.git```
2. Install dependencies:
```pip install -r requirements.txt```
3. Run the script:
```python main.py```

## Usage
1. Launch the application.
2. Select a folder containing .dds textures.
3. Customize postfixes.
4. Click ```"Select Folder"``` to start the conversion process.
5. Converted textures will be saved in a ```converted_textures``` subfolder.

## Building the Executable
To create a standalone .exe file:

```pyinstaller --onefile --windowed --icon=ui/logo.ico --add-data "ui/logo.ico;ui" --add-data "ui/MyFont.ttf;." --name "DagorTexturesConverter" --clean  main.py```

## Contributing
Contributions are welcome! If you encounter bugs or have feature requests, please open an issue. For contributions, fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See LICENSE for details.
