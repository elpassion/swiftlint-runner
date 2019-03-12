# SwiftLint config per target

Missing `.xcproj` aware SwiftLint runner with support for different configurations per target.

## The problem

Imagine you want to use two different rulesets for linting Swift files with SwiftLint. You have 2 config files:

* `.swiftlint_sources.yml` for the production target,
* `.swiftlint_tests.yml` for the test target.

Having the test directories separated from the source ones, it's quite easy to achieve. Given the directory structure:

```
Project /
├── Project.xcodeproj
└── Sources /
│   ├── .swiftlint.yml    # .swiftlint_sources.yml
│   └── Controllers /
│      └── Login /
│          └── LoginViewController.swift
└── Tests /
    ├── .swiftlint.yml    # .swiftlint_tests.yml
    └── Controllers /
        └── Login /
            └── LoginViewControllerSpec.swift
```

You can use a different build phase for the production target:

```
if which swiftlint >/dev/null; then
    cd Sources
    swiftlint
else
    echo "warning: SwiftLint not installed, run 'brew bundle' command"
fi
```

And for the test target:

```
if which swiftlint >/dev/null; then
    cd Tests
    swiftlint
else
    echo "warning: SwiftLint not installed, run 'brew bundle' command"
fi
```

However, keeping the two structures in sync becomes cumbersome in larger projects. That's why you might opt-in to use the same structure for both the production and the test targets:

```
Project /
├── Project.xcodeproj
└── Sources /
    ├── .swiftlint.yml
    └── Controllers /
       └── Login /
           ├── LoginViewController.swift
           └── LoginViewControllerSpec.swift
```

But what about SwiftLint then? 

SwiftLint supports glob patterns, but it's not recursive, so you can't have following in the config file:

```
excluded:
  - "**Spec.swift"
``` 

That's a bummer! You could have easily fixed that, if SwiftLint new about Xcode project and targets, but [the maintainers explicitly decided against that](https://github.com/realm/SwiftLint/issues/1611#issuecomment-316955688).

## SwiftLint runner

Here's where **SwiftLint runner** can help. **SwiftLint runner** is a script that lists all of the Swift files under a specific target, appends it to the specified config file and performs linting using the modified config.

Given the directory structure:

```
Project /
├── .swiftlint_sources.yml
├── .swiftlint_tests.yml
├── Project.xcodeproj
└── Sources /
    └── Controllers /
       └── Login /
           ├── LoginViewController.swift
           └── LoginViewControllerSpec.swift
```

and the two targets called `Production` & `Tests` you can add separate build phases for the `Production` scheme:

```
slrunner Project.xcodeproj Production .swiftlint_sources.yml
```

and for the `Tests` scheme:

```
slrunner Project.xcodeproj Tests .swiftlint_tests.yml
```

And forget about glob patterns exclusion/inclusion forever!

## Installation

**SwiftLint runner** requires Python 3.7. To install it, simply run:

```
pip install swiftlint-runner
```
