# Local MISRA C Code Reviewer 🛡️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

A privacy-first code review tool that utilizes Local Large Language Models (LLMs) via **LM Studio** to audit C code for **MISRA C:2012 compliance**, **security vulnerabilities**, and **coding standards**.

## 🚀 Why This Project?

In embedded systems development, proprietary source code cannot be sent to public cloud APIs (like ChatGPT or Claude) due to IP protection and privacy risks.

This tool solves that problem by:
1.  **Running 100% Offline:** Interfacing with a local inference server (LM Studio).
2.  **Automating Compliance:** Checking against MISRA guidelines automatically.
3.  **Zero Data Leakage:** No code ever leaves the local network.

## ✨ Features

* **Local Inference:** Uses the OpenAI API standard to talk to local models running on port `1234`.
* **Structured Reporting:** Automatically generates a `_REPORT.md` file for every analyzed source file.
* **Customizable Prompts:** Easily adjustable system prompts to enforce specific company guidelines or strictness levels.
* **Lightweight:** Requires only Python and the standard `openai` client library.

## 🛠️ Prerequisites

1.  **Python 3.8+** installed.
2.  **[LM Studio](https://lmstudio.ai/)** installed and running.
3.  A capable LLM loaded in LM Studio (Recommended: `Llama-3-8B-Instruct`, `Mistral-7B`, or `Qwen-2.5-Coder`).

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/Local-MISRA-Reviewer.git](https://github.com/yourusername/Local-MISRA-Reviewer.git)
    cd Local-MISRA-Reviewer
    ```

2.  **Create a virtual environment (Optional but recommended)**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install openai
    ```

## ⚙️ Configuration (LM Studio)

1.  Open **LM Studio**.
2.  Go to the **"Local Server"** tab (double-headed arrow icon).
3.  Load your preferred model.
4.  Click **"Start Server"**.
5.  Ensure the server is running on `http://localhost:1234`.

## 💻 Usage

Run the script pointing to any C source file:

```bash
python reviewer.py path/to/your_file.c