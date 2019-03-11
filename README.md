# Missing SwiftLint runner

Missing Xcode project aware **SwiftLint runner** with support for different targets.

## Motivation

The original SwiftLint tool is Xcode project agnostic. This can be problematic. Imagine you want to use different SwiftLint config for production and test targets and you have a directory structure where tests (specs) are mixed up with production code:

```
UI /
│
└── Controllers /
    │
    ├── ViewController.swift
    ├── ViewControllerSpec.swift
    └── Doubles
        └── APIClientDouble.swift
```

As of now, SwiftLint does not support recursive glob patterns, so you can't exclude the directory like `**Doubles`. 

## SwiftLint runner

**SwiftLint runner** lists all of the Swift files under a specific target, appends it to the specified config file and performs linting on those files.

Given the directory structure:

```
Project /
│
├── .swiftlint_sources.yml
├── .swiftlint_specs.yml
├── Project.xcodeproj
└── Controllers /
    ├── ViewController.swift
    └── ViewControllerSpec.swift
```

and the two targets called `Production` & `Specs` you can use SwiftLint runner as follows:

```
slrunner Project.xcodeproj Production .swiftlint_sources.yml
slrunner Project.xcodeproj Specs .swiftlint_specs.yml
```

And forget about glob patterns at all!

## Installation

**SwiftLint runner** requires Python 3.7. To install it, simply run:

```
pip install swiftlint-runner
```
