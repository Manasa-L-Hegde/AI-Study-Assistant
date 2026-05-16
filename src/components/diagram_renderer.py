"""
Diagram rendering utilities for AI Study Assistant.
Supports Mermaid diagrams and other visualizations.
"""

import streamlit as st
from typing import Optional, Dict, Any
import base64


class DiagramRenderer:
    """Renderer for various diagram types."""
    
    @staticmethod
    def render_mermaid(mermaid_code: str, description: Optional[str] = None) -> None:
        """
        Render a Mermaid diagram.
        
        Args:
            mermaid_code: Mermaid diagram code
            description: Optional description of the diagram
        """
        try:
            if description:
                st.markdown(f"**{description}**")
            
            # Use streamlit-mermaid or HTML rendering
            mermaid_html = f"""
            <div class="mermaid-container" style="background: white; padding: 20px; border-radius: 12px; margin: 16px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <pre class="mermaid">
{mermaid_code}
                </pre>
            </div>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default',
                    securityLevel: 'loose',
                    flowchart: {{
                        useMaxWidth: true,
                        htmlLabels: true,
                        curve: 'basis'
                    }}
                }});
            </script>
            """
            st.markdown(mermaid_html, unsafe_allow_html=True)
            
        except Exception as e:
            st.warning(f"Could not render diagram: {e}")
            with st.expander("Show diagram code"):
                st.code(mermaid_code, language="mermaid")
    
    @staticmethod
    def render_diagram_from_data(diagram_data: Dict[str, Any]) -> None:
        """
        Render diagram from structured data.
        
        Args:
            diagram_data: Dictionary containing diagram information
        """
        if not diagram_data:
            return
        
        diagram_type = diagram_data.get("type", "flowchart")
        mermaid_code = diagram_data.get("mermaid_code", "")
        description = diagram_data.get("description", "")
        
        if mermaid_code:
            st.markdown("### 📊 Visual Diagram")
            DiagramRenderer.render_mermaid(mermaid_code, description)
        else:
            st.info("💡 No diagram available for this topic")
    
    @staticmethod
    def create_simple_flowchart(steps: list) -> str:
        """
        Create a simple flowchart from a list of steps.
        
        Args:
            steps: List of step descriptions
        
        Returns:
            Mermaid flowchart code
        """
        mermaid_code = "flowchart TD\n"
        for i, step in enumerate(steps):
            node_id = f"A{i}"
            next_node = f"A{i+1}" if i < len(steps) - 1 else None
            mermaid_code += f'    {node_id}["{step}"]\n'
            if next_node:
                mermaid_code += f"    {node_id} --> {next_node}\n"
        return mermaid_code
    
    @staticmethod
    def create_mindmap(central_topic: str, branches: Dict[str, list]) -> str:
        """
        Create a mindmap diagram.
        
        Args:
            central_topic: Central topic
            branches: Dictionary of branch topics and their sub-topics
        
        Returns:
            Mermaid mindmap code
        """
        mermaid_code = f"mindmap\n  root(({central_topic}))\n"
        for branch, sub_topics in branches.items():
            mermaid_code += f"    {branch}\n"
            for sub in sub_topics:
                mermaid_code += f"      {sub}\n"
        return mermaid_code


class CodeRenderer:
    """Renderer for code blocks with syntax highlighting."""
    
    @staticmethod
    def render_code_block(code: str, language: str = "python", title: Optional[str] = None) -> None:
        """
        Render a code block with syntax highlighting.
        
        Args:
            code: Code content
            language: Programming language
            title: Optional title for the code block
        """
        if title:
            st.markdown(f"**{title}**")
        st.code(code, language=language)
    
    @staticmethod
    def render_formula(formula: str, explanation: Optional[str] = None) -> None:
        """
        Render a mathematical formula.
        
        Args:
            formula: LaTeX formula
            explanation: Optional explanation
        """
        st.latex(formula)
        if explanation:
            st.caption(explanation)


class TableRenderer:
    """Renderer for tables and comparisons."""
    
    @staticmethod
    def render_comparison_table(data: Dict[str, Dict[str, str]]) -> None:
        """
        Render a comparison table.
        
        Args:
            data: Dictionary of items to compare
        """
        import pandas as pd
        
        df = pd.DataFrame(data).T
        st.table(df)
    
    @staticmethod
    def render_key_value_table(data: Dict[str, str], title: Optional[str] = None) -> None:
        """
        Render a key-value table.
        
        Args:
            data: Dictionary of key-value pairs
            title: Optional title
        """
        if title:
            st.markdown(f"**{title}**")
        
        for key, value in data.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{key}:**")
            with col2:
                st.markdown(value)


# Made with Bob