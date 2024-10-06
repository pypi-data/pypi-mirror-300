# mascii

`mascii` is a command-line tool to convert images and videos to ASCII art.

## Features

- Convert images to ASCII art
- Convert videos to ASCII art
- Adjustable playback speed for videos
- Option to invert the ASCII character set

## Installation

To install `mascii`, clone the repository and install it using `pip`:

```
pip install mascii
```

or

```
git  clone  https://github.com/joelcrasta/mascii.git
cd  mascii
pip  install  -e  .
```

## Usage

### Convert image to ASCII art

To display an ASCII art, use the `-p` or `--path` option to specify the output file name (without extension):

```
mascii  -p  path/to/image.jpg
```

### Convert a Video to ASCII Art

To convert a video to ASCII art, use the `-p` or `--path` option to specify the path to the input video, and the `-s` or `--speed` option to specify the playback speed (1-10):

```
mascii  -p  path/to/video.mp4  -s  5
```

### Save ASCII art

To convert an image to ASCII art and save it, use the `-o` or `--out` option to specify the output file name (without extension):

```
mascii  -p  path/to/image.jpg  -o  output_filename
```

### Full Command-Line Options

```
usage:  mascii  [-h]  [-p PATH]  [-o OUT]  [-s SPEED]  [-i]
```

## Future Updates

- Save your own characters sets and use them to make art.
- Coloured ASCII art.
- Save videos as ASCII arts and play them anytime.
