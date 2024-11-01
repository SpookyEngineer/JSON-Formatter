# JSON Formatter Application

## Overview

The JSON Formatter is a Python application that allows users to paste JSON text and format it into a more readable structure. 
It provides a graphical user interface (GUI) built with Tkinter, enabling users to easily input, format, search, and copy formatted JSON.

## Prepackaged Executables
There are artifacts available in the Actions tab, one for Windows and one for Linux (Ubuntu).
After your GitHub Actions workflow runs successfully and uploads the build artifacts, you can find the files in the following way:

1. **Access the Actions Tab**:
   - Click on the **"Actions"** tab located at the top of your repository page. This tab shows all the workflows that have run.

2. **Select the Latest Workflow Run**:
   - In the Actions tab, you will see a list of recent workflow runs. Click on the most recent one that corresponds to the push that triggered the build.

3. **View Workflow Details**:
   - Once you're in the specific run's details, you'll see a list of all the steps that were executed during that run. 

4. **Download Artifacts**:
   - Scroll down to the bottom of the page where you will find a section labeled **"Artifacts"**. This section lists the artifacts uploaded during the run, including your Windows and Linux executables.
   - Click on the artifact name (e.g., `windows-executable` or `linux-executable`) to download it as a zip file.

5. **Extract and Use the Files**:
   - Once downloaded, extract the zip file to access the executables you built.

### Further Instructions for Linux
**After downloading the Linux file:**

1. Open a terminal.
2. Change to the directory where the executable is located:
   ```bash
   cd ~/Downloads
   ```
3. Make the executable runnable:
   ```bash
   chmod +x my_app
   ```
4. Run the application:
   ```bash
   ./my_app
   ```


## Features

- **Input JSON:** Paste your JSON text in a scrollable text area.
- **Format JSON:** Convert unformatted JSON into a pretty-printed format for better readability.
- **Search Functionality:** Search for specific keys or values within the formatted JSON and navigate through results.
- **Copy to Clipboard:** Easily copy the formatted JSON to your clipboard for further use.
- **User-friendly Interface:** A simple and intuitive GUI built with Tkinter.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SpookyEngineer/JSON-Formatter.git

2. **Navigate to the project directory:**

   ```bash
   cd json-formatter
   ```

3. **Run the application:**

   ```bash
   python json_formatter.py
   ```

## Usage

1. **Paste your JSON:** Copy and paste your JSON text into the "Paste your JSON here" section.
2. **Format the JSON:** Click the "Format JSON" button to format your JSON.
3. **Search for Terms:** Use the search box to find specific terms within the formatted JSON. Navigate through the results using the "Previous" and "Next" buttons.
4. **Copy to Clipboard:** Click the "Copy to Clipboard" button to copy the formatted JSON for use elsewhere.

## Code Structure

The application consists of the following key components:

- **JsonFormatterApp:** The main class responsible for creating the GUI and handling user interactions.
- **format_json:** Parses the input JSON and formats it for better readability.
- **search_json:** Searches for terms in the formatted JSON and highlights them.
- **copy_to_clipboard:** Copies the formatted JSON to the clipboard.

## Example

To format a JSON object, paste the following example into the input section:

```json
{"name":"John","age":30,"city":"New York"}
```

After clicking "Format JSON," the output will be:

```json
{
    "name": "John",
    "age": 30,
    "city": "New York"
}
```

## Contributing

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request with your changes.
