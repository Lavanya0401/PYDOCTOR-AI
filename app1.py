import google.generativeai as genai
import os
import streamlit as st

# ðŸ”¹ Load API Key Securely (Replace with your actual key or set as an environment variable)
API_KEY = os.getenv("GEMINI_API_KEY")



# System Prompt for AI
SYSTEM_PROMPT = """
You are a Python code reviewer. Your task is to analyze submitted code, identify potential bugs or errors, suggest optimizations or improvements, and provide a corrected version.

### 🛠 Bug/Error Identification
- Explain errors or bugs in the provided code.
- If the code is not Python, compare it with Python syntax and explain mistakes.

### ⚡ Suggested Fixes/Optimizations
- Provide fixes and optimizations with explanations.

### ✅ Corrected Code
- Output the fully functional, corrected Python code.
"""
# Initialize Google Gemini AI Model
model = genai.GenerativeModel("gemini-2.0-flash-exp",system_instructions=SYSTEM_PROMPT)
def review_code(code):
    try:
        prompt = f"Review this Python code:\npython\n{code}\n"
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else response.parts[0].text
    except Exception as e:
        return f"⚠ Error: {str(e)}"

def extract_fixed_code(review_text):
    try:
        start = review_text.find("python") + len("python")
        end = review_text.find("```", start)
        return review_text[start:end].strip() if start > -1 and end > -1 else "⚠ No corrected code found!"
    except Exception as e:
        return f"⚠ Error extracting fixed code: {str(e)}"

import base64

# âœ… Define image path
image_path = "AI_PyDoctor_logo.png"

def main():
    st.set_page_config(page_title="AI PyDoctor", layout="wide")

    # âœ… Display logo inline with title
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()

        # âœ… Improved Logo and Title Alignment
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src='data:image/png;base64,{img_base64}' style="width: 100px; height: 100px;">
                <h1 style='margin: 0; font-size: 32px;'>AI PyDoctor - Python Code Reviewer</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"âš ï¸ Image not found at {image_path}. Please check the file path.")
    # Code Input Block
    st.markdown("### Enter your Python code below:")
    code = st.text_area("✍ Code Input", height=200)
    
    if st.button("🔍 Review Code"):
        if code.strip():
            with st.spinner("Analyzing your code... 💡"):
                review = review_code(code)
                fixed_code = extract_fixed_code(review)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔴 Before (Original Code)")
                st.code(code, language="python")
            with col2:
                st.subheader("🟢 After (Fixed Code)")
                st.code(fixed_code, language="python")
            
            st.subheader("📝 AI Review Feedback:")
            st.markdown(review, unsafe_allow_html=True)
            
            st.download_button("💽 Download Fixed Code", fixed_code, file_name="fixed_code.py")
            
            if st.button("🚀 Run Fixed Code"):
                with st.spinner("Executing corrected code..."):
                    try:
                        exec(fixed_code)
                        st.success("✅ Execution Completed Successfully!")
                    except Exception as e:
                        st.error(f"⚠ Error in execution: {str(e)}")
        else:
            st.warning("⚠ Please enter some Python code to review.")

if __name__ == "__main__":
    main()
