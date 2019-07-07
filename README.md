[![Build Status](https://travis-ci.com/Sencudra/svg2swift.svg?token=HJY9g7GV3JgmsxHL3fqK&branch=master)](https://travis-ci.com/Sencudra/svg2swift)
[![codebeat badge](https://codebeat.co/badges/d6c77aa8-44a9-4969-8648-c3540ee82b32)](https://codebeat.co/projects/github-com-sencudra-svg2swift-master)

## SVG-to-Swift converter

### Overview
Simple and light script to convert svg ```d``` attribute
path to ```UIBezierPath``` Swift code description. See example 
below for more details.

### Usage

Execute command:

```shell
svg2swift.py [-h] --input_file INPUT_FILE [--output_file OUTPUT_FILE]
```

### Example

Suppose we have following svg image of github:

![](media/github.svg)

This masterpiece of design has following xml description:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<svg xmlns="http://www.w3.org/2000/svg" width="197.3" height="197.3" 
viewBox="0 0 148 148" version="1.1">
<path d="M74 0C33.1 0 0 34 0 75.9 0 109.4 21.2 137.8 50.6 147.9 54.3 
148.6 55.7 146.2 55.7 144.2 55.7 142.4 55.6 137.6 55.6 131.3 35 135.9 
30.6 121.1 30.6 121.1 27.3 112.4 22.4 110 22.4 110 15.7 105.3 22.9 
105.4 22.9 105.4 30.4 106 34.3 113.2 34.3 113.2 40.9 124.8 51.6 121.5
55.8 119.5 56.5 114.6 58.4 111.3 60.5 109.4 44.1 107.5 26.8 101 26.8
71.9 26.8 63.6 29.7 56.9 34.4 51.5 33.6 49.6 31.1 41.9 35.1 31.5 35.1
31.5 41.3 29.4 55.5 39.2 61.4 37.6 67.7 36.7 74 36.7 80.3 36.7 86.6
37.6 92.5 39.2 106.7 29.4 112.9 31.5 112.9 31.5 116.9 41.9 114.4 49.6
113.6 51.5 118.3 56.9 121.2 63.6 121.2 71.9 121.2 101.1 103.9 107.5 87.4
109.3 90.1 111.7 92.4 116.3 92.4 123.4 92.4 133.5 92.3 141.7 92.3
144.2 92.3 146.2 93.7 148.6 97.4 147.9 126.8 137.8 148 109.4 148 75.9
148 34 114.9 0 74 0"
style="stroke:none;fill:rgb(10.588235%,9.411765%,9.019608%)"/></svg>
```

To run script execute following command in project folder: 

```shell
    python svg2swift.py --input_file github.svg
```

The script will 'parse' xml and get following path commands:

```txt
[('M', (74.0, 0.0)),
 ('C', (33.1, 0.0, 0.0, 34.0, 0.0, 75.9)),
 ('C', (0.0, 109.4, 21.2, 137.8, 50.6, 147.9)),
 ('C', (54.3, 148.6, 55.7, 146.2, 55.7, 144.2)),
 ('C', (55.7, 142.4, 55.6, 137.6, 55.6, 131.3)),
 ('C', (35.0, 135.9, 30.6, 121.1, 30.6, 121.1)),
 ('C', (27.3, 112.4, 22.4, 110.0, 22.4, 110.0)), 
 ('C', (15.7, 105.3, 22.9, 105.4, 22.9, 105.4)), 
 ('C', (30.4, 106.0, 34.3, 113.2, 34.3, 113.2)), 
 ('C', (40.9, 124.8, 51.6, 121.5, 55.8, 119.5)),
 ('C', (56.5, 114.6, 58.4, 111.3, 60.5, 109.4)),
 ('C', (44.1, 107.5, 26.8, 101.0, 26.8, 71.9)), 
 ('C', (26.8, 63.6, 29.7, 56.9, 34.4, 51.5)), 
 ('C', (33.6, 49.6, 31.1, 41.9, 35.1, 31.5)), 
 ('C', (35.1, 31.5, 41.3, 29.4, 55.5, 39.2)), 
 ('C', (61.4, 37.6, 67.7, 36.7, 74.0, 36.7)), 
 ('C', (80.3, 36.7, 86.6, 37.6, 92.5, 39.2)), 
 ('C', (106.7, 29.4, 112.9, 31.5, 112.9, 31.5)), 
 ('C', (116.9, 41.9, 114.4, 49.6, 113.6, 51.5)), 
 ('C', (118.3, 56.9, 121.2, 63.6, 121.2, 71.9)), 
 ('C', (121.2, 101.1, 103.9, 107.5, 87.4, 109.3)), 
 ('C', (90.1, 111.7, 92.4, 116.3, 92.4, 123.4)), 
 ('C', (92.4, 133.5, 92.3, 141.7, 92.3, 144.2)), 
 ('C', (92.3, 146.2, 93.7, 148.6, 97.4, 147.9)), 
 ('C', (126.8, 137.8, 148.0, 109.4, 148.0, 75.9)), 
 ('C', (148.0, 34.0, 114.9, 0.0, 74.0, 0.0))]
```

And the result code will be by default in svg.swift file:

```swift
path = UIBezierPath()
path.move(to: CGPoint(x: 74.0, y: 0.0))
path.addCurve(to: CGPoint(x: 0.0, y: 75.9), controlPoint1: CGPoint(x: 33.1, y: 0.0), controlPoint2: CGPoint(x: 0.0, y: 34.0))
path.addCurve(to: CGPoint(x: 50.6, y: 147.9), controlPoint1: CGPoint(x: 0.0, y: 109.4), controlPoint2: CGPoint(x: 21.2, y: 137.8))
path.addCurve(to: CGPoint(x: 55.7, y: 144.2), controlPoint1: CGPoint(x: 54.3, y: 148.6), controlPoint2: CGPoint(x: 55.7, y: 146.2))
path.addCurve(to: CGPoint(x: 55.6, y: 131.3), controlPoint1: CGPoint(x: 55.7, y: 142.4), controlPoint2: CGPoint(x: 55.6, y: 137.6))
path.addCurve(to: CGPoint(x: 30.6, y: 121.1), controlPoint1: CGPoint(x: 35.0, y: 135.9), controlPoint2: CGPoint(x: 30.6, y: 121.1))
path.addCurve(to: CGPoint(x: 22.4, y: 110.0), controlPoint1: CGPoint(x: 27.3, y: 112.4), controlPoint2: CGPoint(x: 22.4, y: 110.0))
path.addCurve(to: CGPoint(x: 22.9, y: 105.4), controlPoint1: CGPoint(x: 15.7, y: 105.3), controlPoint2: CGPoint(x: 22.9, y: 105.4))
path.addCurve(to: CGPoint(x: 34.3, y: 113.2), controlPoint1: CGPoint(x: 30.4, y: 106.0), controlPoint2: CGPoint(x: 34.3, y: 113.2))
path.addCurve(to: CGPoint(x: 55.8, y: 119.5), controlPoint1: CGPoint(x: 40.9, y: 124.8), controlPoint2: CGPoint(x: 51.6, y: 121.5))
path.addCurve(to: CGPoint(x: 60.5, y: 109.4), controlPoint1: CGPoint(x: 56.5, y: 114.6), controlPoint2: CGPoint(x: 58.4, y: 111.3))
path.addCurve(to: CGPoint(x: 26.8, y: 71.9), controlPoint1: CGPoint(x: 44.1, y: 107.5), controlPoint2: CGPoint(x: 26.8, y: 101.0))
path.addCurve(to: CGPoint(x: 34.4, y: 51.5), controlPoint1: CGPoint(x: 26.8, y: 63.6), controlPoint2: CGPoint(x: 29.7, y: 56.9))
path.addCurve(to: CGPoint(x: 35.1, y: 31.5), controlPoint1: CGPoint(x: 33.6, y: 49.6), controlPoint2: CGPoint(x: 31.1, y: 41.9))
path.addCurve(to: CGPoint(x: 55.5, y: 39.2), controlPoint1: CGPoint(x: 35.1, y: 31.5), controlPoint2: CGPoint(x: 41.3, y: 29.4))
path.addCurve(to: CGPoint(x: 74.0, y: 36.7), controlPoint1: CGPoint(x: 61.4, y: 37.6), controlPoint2: CGPoint(x: 67.7, y: 36.7))
path.addCurve(to: CGPoint(x: 92.5, y: 39.2), controlPoint1: CGPoint(x: 80.3, y: 36.7), controlPoint2: CGPoint(x: 86.6, y: 37.6))
path.addCurve(to: CGPoint(x: 112.9, y: 31.5), controlPoint1: CGPoint(x: 106.7, y: 29.4), controlPoint2: CGPoint(x: 112.9, y: 31.5))
path.addCurve(to: CGPoint(x: 113.6, y: 51.5), controlPoint1: CGPoint(x: 116.9, y: 41.9), controlPoint2: CGPoint(x: 114.4, y: 49.6))
path.addCurve(to: CGPoint(x: 121.2, y: 71.9), controlPoint1: CGPoint(x: 118.3, y: 56.9), controlPoint2: CGPoint(x: 121.2, y: 63.6))
path.addCurve(to: CGPoint(x: 87.4, y: 109.3), controlPoint1: CGPoint(x: 121.2, y: 101.1), controlPoint2: CGPoint(x: 103.9, y: 107.5))
path.addCurve(to: CGPoint(x: 92.4, y: 123.4), controlPoint1: CGPoint(x: 90.1, y: 111.7), controlPoint2: CGPoint(x: 92.4, y: 116.3))
path.addCurve(to: CGPoint(x: 92.3, y: 144.2), controlPoint1: CGPoint(x: 92.4, y: 133.5), controlPoint2: CGPoint(x: 92.3, y: 141.7))
path.addCurve(to: CGPoint(x: 97.4, y: 147.9), controlPoint1: CGPoint(x: 92.3, y: 146.2), controlPoint2: CGPoint(x: 93.7, y: 148.6))
path.addCurve(to: CGPoint(x: 148.0, y: 75.9), controlPoint1: CGPoint(x: 126.8, y: 137.8), controlPoint2: CGPoint(x: 148.0, y: 109.4))
path.addCurve(to: CGPoint(x: 74.0, y: 0.0), controlPoint1: CGPoint(x: 148.0, y: 34.0), controlPoint2: CGPoint(x: 114.9, y: 0.0))
```

Yes, it's rather messy and complicated. Otherwise, it's perfect for rare im-app usage instead of importing
large library.

<img src="Media/github.png" width="400">


Copyright © 2019, Vlad Tarasevich




