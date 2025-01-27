from typing import Tuple
import google.generativeai as genai
import json
from langchain_core.prompts import ChatPromptTemplate
from key import api_key

genai.configure(api_key=api_key)  # Replace with your Google API key

MODEL_NAME = "gemini-1.5-flash"
llm = genai.GenerativeModel(MODEL_NAME)

def prepare_chat_prompt(context: str, prompt: str):
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    ).format(context=context)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    return prompt_template.format(input=prompt)

def llm_invoke(prompt: str):
    print("LLM thinking...")
    try:
        response = llm.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error invoking Gemini: {e}")
        return "Sorry, I couldn't generate a response. Please try again."


def generate_notes(documents: list) -> Tuple[str, str]:
    """
    Generate both human-readable notes and structured markdown version.
    Returns a tuple of (readable_notes, markdown_notes)
    """
    context = "\n\n".join(documents)
    
    readable_prompt = """
    Generate detailed, well-structured educational notes from the following content. 
    The notes should be easy to read and understand. Include:

    1. A clear title for the overall notes
    2. A brief summary or overview at the start
    3. Main topics with clear headings
    4. Important concepts clearly explained
    5. Key points and takeaways
    6. Examples where relevant
    7. Definitions of important terms
    
    Format the notes in a clean, readable style with:
    - Clear headings and subheadings
    - Proper spacing between sections
    - Bullet points for lists
    - Emphasized important terms
    - Clear organization of ideas

    Make it engaging and easy to follow for students/readers.
    """
    
    markdown_prompt = """
    Generate the same content but in structured markdown format:
    
    1. Use # for title
    2. Use ## for main sections
    3. Use ### for subsections
    4. Use - for bullet points
    5. Use * for emphasis
    6. Use > for key points
    7. Use proper markdown formatting
    """
    
    try:
        readable_response = llm.generate_content(readable_prompt + "\n\nContext:\n" + context)
        readable_notes = readable_response.text
        
        markdown_response = llm.generate_content(markdown_prompt + "\n\nContent to convert:\n" + readable_notes)
        markdown_notes = markdown_response.text
        
        return readable_notes, markdown_notes
    except Exception as e:
        print(f"Error generating notes: {e}")
        return None, None

def format_notes_for_display(notes: str) -> str:
    """
    Format the readable notes for better display in Streamlit.
    """
    formatted_notes = notes.replace("**", "").replace("__", "")  
    return formatted_notes

def convert_to_latex(notes: str) -> str:
    """
    Convert notes to properly formatted LaTeX with academic styling.
    """
    latex_preamble = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{setspace}
\usepackage{parskip}

% Format settings
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\onehalfspacing

% Section formatting
\titleformat{\section}
{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}
{\normalsize\bfseries}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}
{\normalsize\bfseries}{\thesubsubsection.}{0.5em}{}

% Title page settings
\title{Nepali Cultural Videos VQA:\\Dataset Creation and Model Fine-tuning}
\author{Generated Notes}
\date{\today}

\begin{document}
\maketitle
"""

    latex_content = ""
    in_itemize = False
    
    lines = notes.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('Generated Notes'):
            continue
            
        line = (line.replace('&', '\\&')
                   .replace('%', '\\%')
                   .replace('$', '\\$')
                   .replace('_', '\\_'))
        
        if line.startswith('# '):
            continue  
        elif line.startswith('## '):
            if in_itemize:
                latex_content += "\\end{itemize}\n"
                in_itemize = False
            section_name = line[3:].strip()
            latex_content += f"\n\\section{{{section_name}}}\n"
            current_section = 'section'
        elif line.startswith('### '):
            if in_itemize:
                latex_content += "\\end{itemize}\n"
                in_itemize = False
            subsection_name = line[4:].strip()
            latex_content += f"\n\\subsection{{{subsection_name}}}\n"
            current_section = 'subsection'
        
        # Handle bullet points
        elif line.startswith('• '):
            if not in_itemize:
                latex_content += "\\begin{itemize}[leftmargin=*]\n"
                in_itemize = True
            item_text = line[2:].strip()
            item_text = item_text.replace('*', '\\textbf{', 1).replace('*', '}', 1)
            latex_content += f"  \\item {item_text}\n"
            
        # Handle bold text with **
        elif '**' in line:
            if in_itemize:
                latex_content += "\\end{itemize}\n"
                in_itemize = False
            line = line.replace('**', '\\textbf{', 1).replace('**', '}', 1)
            latex_content += line + "\n\n"
            
        # Regular paragraphs
        else:
            if in_itemize:
                latex_content += "\\end{itemize}\n"
                in_itemize = False
            latex_content += line + "\n\n"
    
    if in_itemize:
        latex_content += "\\end{itemize}\n"
    
    latex_footer = "\n\\end{document}"
    
    return latex_preamble + latex_content + latex_footer
