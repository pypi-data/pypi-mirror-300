# imgease - A Collection of Command-Line Tools for Image Processing

## Command-Line Tool: imgease-grayscale
Converts one or multiple images, or all images in a specified directory, to grayscale and saves them in the designated output directory. The script supports recursive processing of subdirectories within the specified directory.

### Features
- **Batch processing**:Can process one or multiple images, or all images in a directory.
- **Recursive processing**:Supports recursive processing of subdirectories within a directory.

### Installation
```bash
pipx install imgease
```

### Usage
#### Processing a single image
```bash
imgease-grayscale -i <input image path> -o <output directory>
```

#### Processing multiple images
```bash
imgease-grayscale -i <input image path> <input image path> -o <output directory>
```

#### Processing all images in a directory
```bash
imgease-grayscale -i <input directory path> -o <output directory>
```

#### Recursively processing subdirectories
```bash
imgease-grayscale -r -i <input directory path> -o <output directory>
```

##### Notes
- This script only processes image files in the following formats: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.tiff`.
- Each converted image will have the `_grayscale` suffix added to its filename.

## Command-Line Tool: imgease-convert
converts common image formats (such as `.png`, `.bmp`, `.tiff`) to `.jpeg` format.

### Features
- **Batch processing**:Can process one or multiple images, or all images in a directory.
- **Recursive processing**:Supports recursive processing of subdirectories within a directory.

### Installation
```bash
pipx install imgease
```

### Usage
#### Processing a single image
```bash
imgease-convert -i <input image path> -o <output directory>
```

#### Processing multiple images
```bash
imgease-convert -i <input image path> <input image path> -o <output directory>
```

#### Processing all images in a directory
```bash
imgease-convert -i <input directory path> -o <output directory>
```

#### Recursively processing subdirectories
```bash
imgease-convert -r -i <input directory path> -o <output directory>
```

##### Notes
- This script only processes image files in the following formats: `.png`, `.bmp`, `.tiff`.
- Each converted image will have the `_converted` suffix added to its filename.

## License
This project is licensed under the GPL-3.0 License.
