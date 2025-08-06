# OpenAI Agents Project - Code Debugging Assistant

# 🛠️ Code Debugging Assistant

Code Debugging Assistant is an AI-powered tool designed to simplify code analysis, debugging, optimization, and security reviews across multiple programming languages. It uses OpenAI's GPT models and provides a clean Gradio-based interface for effortless interaction.

---

## 🧭 Introduction

This project enables developers to paste code, select an analysis type (explanation, bug fix, optimization, or security review), and instantly receive GPT-powered insights and improvements. It saves time, improves code quality, and enhances developer productivity — especially for beginners and rapid prototyping.

---

## 🚀 Features

- ✅ **Multi-language support**: Python, JavaScript, Java, C++, C, C#, SQL, PHP, and more.
- 🔐 **OpenAI API Key Input**: Set securely at runtime.
- 🔎 **4 Smart Analysis Modes**:
  - **Explain Code** – Understand what the code does in simple terms.
  - **Debug & Fix** – Detect and correct bugs and issues.
  - **Optimize Code** – Suggest code improvements for performance and readability.
  - **Security Review** – Identify potential vulnerabilities and safer alternatives.
- 🤖 **Model Flexibility**: Supports `gpt-3.5-turbo` and `gpt-4`.
- 🧠 **Language Auto-Detection**: Determines the programming language automatically.
- 🧾 **Simple Interface**: Built with Gradio for fast, intuitive usage.

---

## ⚙️ How It Works

1. 🔑 **Set API Key**  
   → Enter your OpenAI API key securely using the provided textbox.

2. 🧾 **Paste Your Code**  
   → Paste or write any code snippet you want to analyze.

3. 📌 **Choose Analysis Type**  
   → Select one of the following:
   - Explain Code
   - Debug & Fix
   - Optimize Code
   - Security Review

4. 🤖 **Select GPT Model**  
   → Choose between `gpt-3.5-turbo` or `gpt-4`.

5. 🔍 **Click Analyze or Get Suggestions**  
   → The assistant detects the code language, builds a custom prompt, and uses GPT to process the request.

6. 📤 **Receive Results**  
   → Results are shown in clear, structured Markdown including:
   - Detected language
   - Errors found
   - Corrected code
   - Performance/security improvements

---


