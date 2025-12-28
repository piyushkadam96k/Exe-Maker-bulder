# 🐍 Kadam Exe Maker

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Kadam Exe Maker** is a modern, beautiful GUI wrapper for **PyInstaller**. Convert your Python scripts into standalone executable (`.exe`) files with just a few clicks, featuring a sleek dark-mode interface built with `CustomTkinter`.

---

## ✨ Features

*   **🎨 Modern Dark GUI**: A clean, professional interface that makes building apps easy.
*   **📂 Asset Bundling**: Easily include entire folders (images, data files) inside your EXE.
*   **🖼️ Custom Icons**: Give your app a professional look with custom `.ico` support.
*   **🛠️ Advanced Control**:
    *   **OneFile Mode**: Bundle everything into a single portable `.exe`.
    *   **No Console**: Perfect for GUI applications (hides the black command window).
    *   **Hidden Imports**: Manually fix missing module errors.
*   **⚡ Real-Time Logs**: View the build process live right in the application.

## 🚀 Installation

1.  **Clone the repository** (or download usage):
    ```bash
    git clone https://github.com/yourusername/kadam-exe-maker.git
    cd kadam-exe-maker
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 How to Use

1.  Run the application:
    ```bash
    python main.py
    ```
2.  **Select Script**: Browse for your `.py` file.
3.  **Customize**:
    *   Name your app.
    *   Add an Icon.
    *   (Optional) Add an **Asset Folder** if your script uses images/data.
4.  **Build**: Click **BUILD EXECUTABLE** and watch it go! 🚀
5.  Find your new app in the `dist` folder.

## 📦 Requirements

*   Python 3.x
*   `customtkinter`
*   `pyinstaller`
*   `pillow`

## 🤝 Contributing

Feel free to fork this project and submit Pull Requests. Ideas and improvements are welcome!

---
*Made with ❤️ by Kadam*
