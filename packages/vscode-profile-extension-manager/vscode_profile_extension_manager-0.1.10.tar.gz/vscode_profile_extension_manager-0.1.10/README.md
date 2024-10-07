# VS Code Profile Extension Manager (VPEM)

VS Code Profile Extension Manager (VPEM) is a powerful command-line tool designed to help you manage your Visual Studio Code extensions across different profiles. It allows you to dump, categorize, and apply extensions with ease, streamlining your VS Code setup process.

## Status

This project has been developed strictly on Linux, though it should work everywhere.  If you find an issue, please report it in the [GitHub issue tracker](https://github.com/drmikecrowe/vscode-profile-extension-manager/issues).

Executables are built using [pyinstaller](https://github.com/pyinstaller/pyinstaller) and are available for Linux, Windows and MacOS.  Again, if any issues are found, please report them in the [GitHub issue tracker](https://github.com/drmikecrowe/vscode-profile-extension-manager/issues).

## Why?

I tend to use a lot of extensions.  Further, I find my self swithing frequently between TypeScript, Python and now C#.  Sometimes I work in Azure.  Othertimes in AWS.

I realized that multiple profiles might make more sense than tons of extensions in a single profile.  However, it's also really easy to experiment with extensions and leave unused ones polluting the profile.  This tool helps me keep things organized.

For example, here's how to apply a group of extensions to a profile:

![Apply Extensions](https://github.com/drmikecrowe/vscode-profile-extension-manager/blob/main/assets/VPEM-apply-example.png)

## Process

- First, dump your extensions for all your profiles

![Dump Extensions](https://github.com/drmikecrowe/vscode-profile-extension-manager/blob/main/assets/VPEM-dump.gif)

- Next, categorizing extensions by searching for common strings and assign to categories

![Categorize Extensions](https://github.com/drmikecrowe/vscode-profile-extension-manager/blob/main/assets/VPEM-categorize.gif)

- Finally, apply extensions to a profile

![Apply Extensions](https://github.com/drmikecrowe/vscode-profile-extension-manager/blob/main/assets/VPEM-apply.gif)

## Installation

To install VPEM, you can use pip:

```sh
TBD
```

## Usage

Here are some basic usage examples:

- Dump extensions from a profile:

```sh
   poetry run vpem.py dump --profile "Default"
```

- Apply extensions to a profile:

```sh
   poetry run vpem.py apply --profile "Work" --category "Python Development"
```

- List all categories:

```sh
   poetry run vpem.py list-categories
```

## Contributing

We welcome contributions to VPEM! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with a clear message
4. Push your changes to your fork
5. Create a pull request

Please make sure to update tests as appropriate and adhere to the project's coding standards.

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE.md) file for details.

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub issue tracker](https://github.com/drmikecrowe/vscode-profile-extension-manager/issues).
