import sys
import subprocess
import os
from openai import OpenAI

# Your Server IP
LM_STUDIO_URL = "http://10.140.112.242:1234/v1"

# Path to Cppcheck

CPPCHECK_CMD_PATH = r"C:\Program Files\Cppcheck\cppcheck.exe"

client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")

# static analysis tool cpp
def run_cppcheck(file_path):
    """Runs cppcheck and returns the stderr output as a string."""
    print(f"🔍 [1/3] Running Static Analysis on {file_path}...")

    # Check if cppcheck exists at the path
    if not os.path.exists(CPPCHECK_CMD_PATH) and "C:" in CPPCHECK_CMD_PATH:
        return f"Error: Cppcheck not found at {CPPCHECK_CMD_PATH}. Check your path configuration."

    cmd = [
        CPPCHECK_CMD_PATH if os.path.exists(CPPCHECK_CMD_PATH) else "cppcheck",
        "--enable=all",
        "--inconclusive",
        "--template={line}: {severity}: {message}",
        file_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stderr
    except FileNotFoundError:
        return "Error: Cppcheck not installed or not found in PATH."


def analyze_with_llm(file_path, code_content, static_errors):
    """Sends code + static errors to LM Studio."""
    print(f"🧠 [2/3] Sending to AI Model...")

    system_prompt = """
    You are a Senior MISRA C Compliance Officer. 
    Output your review in structured Markdown format.

    Use the following structure:
    # Code Review Report: [Filename]

    ## 1. Executive Summary
    (Brief overview of code quality)

    ## 2. Static Analysis Findings
    (Explain the errors found by the tool below)

    ## 3. MISRA & Style Violations
    (List violations found by you, cite Rule numbers)

    ## 4. Refactored Code
    (Provide the corrected code block)
    """

    user_message = f"""
    FILE NAME: {file_path}

    ### SOURCE CODE:
    ```c
    {code_content}
    ```

    ### STATIC ANALYSIS TOOL OUTPUT:
    {static_errors}
    """

    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.1,
    )

    return completion.choices[0].message.content


def save_report(original_file, report_content):
    """Saves the report to a Markdown file."""
    base_name = os.path.splitext(original_file)[0]
    output_filename = f"{base_name}_review.md"

    print(f"💾 [3/3] Saving report to {output_filename}...")

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report_content)

    return output_filename


def main():
    if len(sys.argv) < 2:
        print("Usage: python smart_reviewer.py <path_to_c_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        code_content = f.read()

    # Step 1: Static Analysis
    cppcheck_errors = run_cppcheck(file_path)

    # Step 2: AI Analysis
    ai_report = analyze_with_llm(file_path, code_content, cppcheck_errors)

    # Step 3: Save to File
    saved_file = save_report(file_path, ai_report)

    print("\n" + "=" * 40)
    print(f"✅ SUCCESS! Report saved: {saved_file}")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    main()