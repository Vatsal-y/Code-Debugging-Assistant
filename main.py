import gradio as gr
import openai
import os
from typing import Tuple, Optional
import json
import re

class CodeDebuggingAssistant:
    def __init__(self):
        """Initialize the Code Debugging Assistant"""
        self.client = None
        self.setup_openai_client()

    def setup_openai_client(self):
        """Setup OpenAI client with API key"""
        try:
            # Try to get API key from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
            else:
                self.client = None
        except Exception as e:
            print(f"Error setting up OpenAI client: {e}")
            self.client = None

    def set_api_key(self, api_key: str) -> str:
        """Set the OpenAI API key"""
        if not api_key or not api_key.strip():
            return "❌ Please enter a valid API key"

        try:
            self.client = openai.OpenAI(api_key=api_key.strip())
            # Test the API key with a simple request
            test_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return "✅ API Key set successfully!"
        except Exception as e:
            self.client = None
            return f"❌ Invalid API key or error: {str(e)}"

    def detect_language(self, code: str) -> str:
        """Detect the programming language of the code"""
        code_lower = code.lower()

        # Common language indicators
        if 'def ' in code or 'import ' in code or 'print(' in code:
            return 'Python'
        elif 'function ' in code or 'console.log' in code or 'let ' in code or 'const ' in code:
            return 'JavaScript'
        elif 'public class' in code or 'System.out' in code or 'public static void main' in code:
            return 'Java'
        elif '#include' in code or 'cout <<' in code or 'int main()' in code:
            return 'C++'
        elif '#include' in code and 'printf' in code:
            return 'C'
        elif 'using System' in code or 'Console.WriteLine' in code:
            return 'C#'
        elif '<?php' in code or '$' in code:
            return 'PHP'
        elif 'SELECT' in code.upper() or 'INSERT' in code.upper() or 'UPDATE' in code.upper():
            return 'SQL'
        else:
            return 'Unknown'

    def analyze_code(self, code: str, analysis_type: str, model: str) -> str:
        """Analyze code using OpenAI API"""
        if not self.client:
            return "❌ Please set your OpenAI API key first!"

        if not code.strip():
            return "❌ Please enter some code to analyze!"

        language = self.detect_language(code)

        # Define prompts for different analysis types
        prompts = {
            "Explain Code": f"""
            Please explain this {language} code in simple, human-readable terms:

            ```{language.lower()}
            {code}
            ```

            Provide:
            1. A clear explanation of what the code does
            2. Break down the main components
            3. Explain the logic flow
            4. Mention any important concepts or patterns used
            """,

            "Debug & Fix": f"""
            Please analyze this {language} code for bugs and issues:

            ```{language.lower()}
            {code}
            ```

            Provide:
            1. Identify any syntax errors, logical errors, or potential runtime issues
            2. Explain why these issues occur
            3. Provide corrected code with explanations
            4. Suggest best practices to avoid similar issues
            """,

            "Optimize Code": f"""
            Please analyze this {language} code for optimization opportunities:

            ```{language.lower()}
            {code}
            ```

            Provide:
            1. Performance improvements
            2. Code readability enhancements
            3. Better coding practices
            4. Optimized version of the code with explanations
            """,

            "Security Review": f"""
            Please review this {language} code for security vulnerabilities:

            ```{language.lower()}
            {code}
            ```

            Provide:
            1. Identify potential security issues
            2. Explain the risks
            3. Suggest secure alternatives
            4. Best practices for secure coding
            """
        }

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer and debugging assistant. Provide clear, detailed, and helpful analysis."},
                    {"role": "user", "content": prompts[analysis_type]}
                ],
                max_tokens=2000,
                temperature=0.3
            )

            result = response.choices[0].message.content
            return f"🔍 **Analysis Type:** {analysis_type}\n🌐 **Detected Language:** {language}\n\n{result}"

        except Exception as e:
            return f"❌ Error analyzing code: {str(e)}"

    def get_code_suggestions(self, code: str, model: str) -> str:
        """Get general suggestions for improving the code"""
        if not self.client:
            return "❌ Please set your OpenAI API key first!"

        if not code.strip():
            return "❌ Please enter some code to get suggestions!"

        language = self.detect_language(code)

        prompt = f"""
        Please provide comprehensive suggestions for this {language} code:

        ```{language.lower()}
        {code}
        ```

        Include:
        1. Code style and formatting improvements
        2. Documentation suggestions
        3. Error handling recommendations
        4. Performance considerations
        5. Maintainability improvements
        6. Any modern language features that could be used
        """

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a senior software engineer providing code review feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.4
            )

            result = response.choices[0].message.content
            return f"💡 **Suggestions for {language} Code:**\n\n{result}"

        except Exception as e:
            return f"❌ Error getting suggestions: {str(e)}"

def create_interface():
    assistant = CodeDebuggingAssistant()

    with gr.Blocks() as iface:
        gr.Markdown("## 🛠️ Code Debugging Assistant")

        with gr.Row():
            api_key_input = gr.Textbox(label="🔑 OpenAI API Key", type="password", placeholder="Enter your OpenAI API key")
            set_key_button = gr.Button("Set API Key")

        with gr.Row():
            code_input = gr.Textbox(label="🧾 Code Input", lines=15, placeholder="Paste your code here...")
            analysis_output = gr.Markdown(label="💬 Output")

        analysis_type = gr.Radio(choices=["Explain Code", "Debug & Fix", "Optimize Code", "Security Review"],
                                 label="📌 Select Analysis Type", value="Debug & Fix")

        model_choice = gr.Radio(choices=["gpt-3.5-turbo", "gpt-4"], label="🤖 Choose OpenAI Model", value="gpt-3.5-turbo")

        analyze_button = gr.Button("🔍 Analyze Code")
        suggest_button = gr.Button("💡 Get Suggestions")

        def handle_set_key(key):
            return assistant.set_api_key(key)

        def handle_analysis(code, analysis_type, model):
            return assistant.analyze_code(code, analysis_type, model)

        def handle_suggestions(code, model):
            return assistant.get_code_suggestions(code, model)

        set_key_button.click(fn=handle_set_key, inputs=api_key_input, outputs=analysis_output)
        analyze_button.click(fn=handle_analysis, inputs=[code_input, analysis_type, model_choice], outputs=analysis_output)
        suggest_button.click(fn=handle_suggestions, inputs=[code_input, model_choice], outputs=analysis_output)

    return iface

if __name__ == "__main__":
    ui = create_interface()
    ui.launch(share=True)


