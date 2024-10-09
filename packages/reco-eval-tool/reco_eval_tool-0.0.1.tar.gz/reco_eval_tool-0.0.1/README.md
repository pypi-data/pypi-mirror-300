# TODO

# Caer - Modern Computer Vision on the Fly

Caer is a *lightweight, high-performance* Vision library for high-performance AI research. We wrote this framework to simplify your approach towards Computer Vision by abstracting away unnecessary boilerplate code giving you the **flexibility** to quickly prototype deep learning models and research ideas. The end result is a library quite different in its design, that’s easy to understand, plays well with others, and is a lot of fun to use.

Our elegant, *type-checked* API and design philosophy makes Caer ideal for students, researchers, hobbyists and even experts in the fields of Deep Learning and Computer Vision.



## Overview

Caer is a Python library that consists of the following components:


| Component                                                                                 | Description                                                                            |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [**caer**](https://github.com/jasmcaus/caer/)                                             | A lightweight GPU-accelerated Computer Vision library for high-performance AI research |
| [**caer.color**](https://github.com/jasmcaus/caer/tree/master/caer/color)                 | Colorspace operations                                                                  |
| [**caer.data**](https://github.com/jasmcaus/caer/tree/master/caer/data)                   | Standard high-quality test images and example data                                     |
| [**caer.path**](https://github.com/jasmcaus/caer/tree/master/caer/path)                   | OS-specific path manipulations                                                         |
| [**caer.preprocessing**](https://github.com/jasmcaus/caer/tree/master/caer/preprocessing) | Image preprocessing utilities.                                                         |
| [**caer.transforms**](https://github.com/jasmcaus/caer/tree/master/caer/transforms)       | Powerful image transformations and augmentations                                       |
| [**caer.video**](https://github.com/jasmcaus/caer/tree/master/caer/video)                 | Video processing utilities                                                             |

<!-- | [**caer.utils**](https://github.com/jasmcaus/caer/tree/master/caer/utils) | Generic utilities  | -->

<!-- | [**caer.filters**](https://github.com/jasmcaus/caer/tree/master/caer/filters) | Sharpening, edge finding, rank filters, thresholding, etc | -->

Usually, Caer is used either as:

- a replacement for OpenCV to use the power of GPUs.
- a Computer Vision research platform that provides maximum flexibility and speed.

# Installation

See the Caer **[Installation][install]** guide for detailed installation instructions (including building from source).

Currently, `caer` supports releases of Python 3.6 onwards; Python 2 is not supported (nor recommended).
To install the current release:

```shell
$ pip install --upgrade caer
```

# Getting Started

## Minimal Example

```python
import caer

# Load a standard 640x427 test image that ships out-of-the-box with caer
sunrise = caer.data.sunrise(rgb=True)

# Resize the image to 400x400 while MAINTAINING aspect ratio
resized = caer.resize(sunrise, target_size=(400,400), preserve_aspect_ratio=True)
```

<img src="examples/thumbs/resize-with-ratio.png" alt="caer.resize()" />

For more examples, see the [Caer demos](https://github.com/jasmcaus/caer/blob/master/examples/) or [Read the documentation](http://caer.rtfd.io)
