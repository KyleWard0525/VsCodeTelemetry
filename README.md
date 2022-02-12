# VsCodeTelemetry
A small python app I'm working on to measure total time spent in VS Code and possibly other metrics. 
This app runs as a background process external to VS Code and is NOT a VS Code extension. 

**NOTE:** The app must be run as an administrator to work properly

## Setup

- Download/Clone the repository
- Add `/bin` to your system %PATH% environment variables (for using `vsct` from cmd or powershell)

## Usage
- To start the telemetry monitor, navigate to `/dist` and run `VsCodeTelemetry.exe` as Administrator

- To see your telemetry, open CMD or Powershell and type `vsct` (**NOTE: This only works if you have added `/bin` to your system path**)