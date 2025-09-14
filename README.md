<div align="center">

# 📦 arc2ipa

<p align="center">
  <a href="https://github.com/medo-iq/arc2ipa/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/medo-iq/arc2ipa?style=for-the-badge" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/platform-macOS-lightgrey?style=for-the-badge&logo=apple" alt="Platform">
</p>

A modern, fast, and interactive CLI tool to efficiently convert Xcode Archives (.xcarchive) into iOS app packages (.ipa).

</div>

---

## 🌟 About The Project

This tool is designed for developers who need to automate the iOS app export process. Instead of dealing with the complex Xcode GUI every time, you can now run a simple terminal command to quickly export your apps, whether for development, Ad-Hoc testing, or App Store submission.

---

## ⚡ Key Features

* **Batch Processing:** Export multiple `.xcarchive` files at once.
* **Rich & Interactive UI:** A beautiful and informative terminal output with colors, spinners, and progress bars.
* **Time Tracking:** Accurately calculates and displays the duration for each export task.
* **Fully Customizable:** Choose the export method that suits your needs (`development`, `ad-hoc`, `app-store`, `enterprise`).
* **Automatic Organization:** Each exported `.ipa` is saved in its own dedicated folder to keep things tidy.
* **Clear Logging:** `xcodebuild` logs are streamed directly to your terminal for easy debugging.

---

## 📋 Requirements

Before you begin, ensure your system meets the following requirements:

* **OS:** macOS
* **Software:** Xcode and Xcode Command Line Tools must be installed.
* **Programming Language:** Python 3.10 or newer.
* **Dependencies:**
    * `rich`: For the interactive and colorful terminal UI.

---

## ⚙️ Installation & Setup

Follow these steps to get the tool set up and ready to run in seconds:

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/medo-iq/arc2ipa.git](https://github.com/medo-iq/arc2ipa.git)
    cd arc2ipa
    ```

2.  **Install dependencies:**
    ```sh
    pip install rich
    ```
    Or from a `requirements.txt` file (if you create one):
    ```sh
    pip install -r requirements.txt
    ```

3.  **Prepare the directories:**
    * Create a directory named `input` and place all your `.xcarchive` files inside it.
    * Create an empty directory named `output`. This is where the exported `.ipa` files will be saved.

---

## 📁 Project Structure

The project has a simple and intuitive folder structure.

````

arc2ipa/
├── input/          \# \<= Place your .xcarchive files here.
├── output/         \# \<= Exported .ipa files will be saved here.
├── export\_ipa.py   \# The main Python script to run.
├── LICENSE         \# Project's MIT License.
└── README.md       \# This file.

````

---

## 🚀 Usage

The tool is easy to use and supports several arguments to customize the export process.

**Basic Command:**
```sh
python3 export_ipa.py
````

**Arguments:**

| Argument            | Description                                                     | Default       |
| ------------------- | --------------------------------------------------------------- | ------------- |
| `-i`, `--input`     | The folder containing the `.xcarchive` files.                   | `input`       |
| `-o`, `--output`    | The folder where the exported `.ipa` files will be saved.         | `output`      |
| `-m`, `--method`    | The export method (`development`, `ad-hoc`, `app-store`, `enterprise`). | `development` |

**Example with custom arguments:**

```sh
python3 export_ipa.py -i ./archives_folder -o ./exported_ipas -m ad-hoc
```

-----

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

-----

## ⭐️ Show your support

Give a ⭐️ if this project helped you\!

-----

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

<br>

<div align="center"\>
<small\>Made with ❤️ by <a href="https://github.com/medo-iq"\>medo-iq</a\></small\>
</div\>

