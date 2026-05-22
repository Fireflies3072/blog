import re
import argparse
from pathlib import Path

class MarkdownConverter:
    """
    Simplified Python implementation of the MarkdownConverter logic.
    Converts regular markdown text into Hexo-friendly markdown.
    """

    def __init__(self):
        # Regex for math spans
        self.display_math_re = re.compile(r'\$\$(?P<content>[\s\S]*?)\$\$(\s*)')
        self.inline_math_re = re.compile(r'(?<!\$)\$(?P<content>[^\n$]*?)\$(?!\$)')
        
        # Regex for protected segments (code blocks and math)
        self.protected_segments_re = re.compile(
            r'```[\s\S]*?```|\$\$[\s\S]*?\$\$|(?<!\$)\$[^\n$]*?\$(?!\$)'
        )

    def _rule_backslash(self, text: str) -> str:
        """Convert double backslash to quadruple backslash."""
        return text.replace('\\\\', '\\\\\\\\')

    def _rule_brace(self, text: str) -> str:
        """Escape curly braces."""
        return text.replace('\\{', '\\\\{').replace('\\}', '\\\\}')

    def _rule_asterisk(self, text: str) -> str:
        """Escape asterisks, unless align* is present."""
        if "align*" in text:
            return text
        return text.replace('*', '{\\*}')

    def _rule_pipe(self, text: str) -> str:
        """Escape pipe characters."""
        return text.replace('|', '\\|')

    def _rule_underscore(self, text: str) -> str:
        """Escape all underscores."""
        return text.replace('_', '\\_')

    def apply_math_rules(self, text: str) -> str:
        """Apply math-specific escaping rules using separate functions."""
        text = self._rule_backslash(text)
        text = self._rule_brace(text)
        text = self._rule_asterisk(text)
        text = self._rule_pipe(text)
        text = self._rule_underscore(text)
        return text

    def apostrophe_global_rule(self, text: str) -> str:
        """Replace apostrophes with HTML entity &#39;, protecting code and math."""
        if not text:
            return ""
        
        parts = []
        last_idx = 0
        for m in self.protected_segments_re.finditer(text):
            parts.append(text[last_idx:m.start()].replace("'", "&#39;"))
            parts.append(m.group())
            last_idx = m.end()
        parts.append(text[last_idx:].replace("'", "&#39;"))
        return "".join(parts)

    def _replace_display_math(self, m: re.Match) -> str:
        """Helper to process display math and ensure trailing newlines."""
        content = self.apply_math_rules(m.group('content'))
        trailing = m.group(2)
        if trailing.count('\n') < 2:
            return f"$${content}$$\n\n"
        return f"$${content}$${trailing}"

    def _replace_inline_math(self, m: re.Match) -> str:
        """Helper to process inline math."""
        content = self.apply_math_rules(m.group('content'))
        return f"${content}$"

    def process_body(self, text: str) -> str:
        """Processes only the body content of a Markdown file."""
        if not text:
            return ""

        # 1. Apply global apostrophe rule
        text = self.apostrophe_global_rule(text)

        # 2. Process display math ($$ ... $$)
        text = self.display_math_re.sub(self._replace_display_math, text)

        # 3. Process inline math ($ ... $)
        text = self.inline_math_re.sub(self._replace_inline_math, text)

        return text

    def process_file_content(self, content: str) -> str:
        """Splits Front Matter from Body, processes Body, and recombines."""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return f"---{parts[1]}---{self.process_body(parts[2])}"
        return self.process_body(content)

def process_file(file_path: Path, converter: MarkdownConverter, base_dir: Path = None):
    try:
        display_path = file_path.relative_to(base_dir) if base_dir else file_path
        print(f"Processing: {display_path}")
        content = file_path.read_text(encoding='utf-8')
        processed_content = converter.process_file_content(content)
        file_path.write_text(processed_content, encoding='utf-8')
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory_path: str):
    converter = MarkdownConverter()
    base_dir = Path(directory_path)
    if not base_dir.exists():
        print(f"Error: Path '{directory_path}' does not exist.")
        return
    
    files = [base_dir] if base_dir.is_file() else list(base_dir.rglob("*.md"))
    for file_path in files:
        if file_path.suffix.lower() == '.md':
            process_file(file_path, converter, base_dir if base_dir.is_dir() else None)

def main():
    parser = argparse.ArgumentParser(description="Batch process Hexo Markdown files.")
    parser.add_argument("path", type=str, nargs="?", default="source/_posts")
    args = parser.parse_args()
    process_directory(args.path)

if __name__ == "__main__":
    main()
