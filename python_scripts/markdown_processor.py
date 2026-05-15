import re
import argparse
from pathlib import Path
import sys

class MarkdownConverter:
    """
    Python implementation of the MarkdownConverter logic.
    Converts regular markdown text into Hexo-friendly markdown, focusing on math spans.

    Maintainer notes (important rule design intent):
    1) One pass should convert "original source" style content into "publish-ready" style content.
       Validation rule: after one pass, the result should match the intended converted style
       (ignoring metadata-only differences such as front matter/title).

    2) The converter MUST be idempotent:
       process_body(process_body(x)) == process_body(x)
       In practice, running the script a second time on an already converted file should not
       introduce any additional escaping or formatting changes.

    3) When adding a new math rule, always preserve already-converted forms.
       Each rule should only transform the "raw/original" pattern and leave the
       "already-processed" pattern untouched.

    4) Backslash handling is especially sensitive:
       - We still need to convert standalone LaTeX line-break \\ as required.
       - We must NOT keep re-escaping sequences such as \\{ and \\} on later runs.

    If a new rule breaks idempotency, prefer tightening the match pattern so the rule
    distinguishes raw input from already-processed output.
    """

    def __init__(self):
        # Math rules in order (from MainWindowViewModel.cs)
        self.math_rules = [
            self.backslash_escape_rule,
            self.brace_escape_rule,
            self.asterisk_escape_rule,
            self.pipe_escape_rule
        ]
        
        # Regex for math spans (from ConversionService.cs)
        self.display_math_re = re.compile(r'\$\$(?P<content>[\s\S]*?)\$\$')
        self.inline_math_re = re.compile(r'(?<!\$)\$(?P<content>[^\n$]*?)\$(?!\$)')
        
        # Regex for protected segments (from ApostropheGlobalRule.cs)
        self.protected_segments_re = re.compile(
            r'```[\s\S]*?```|\$\$[\s\S]*?\$\$|(?<!\$)\$[^\n$]*?\$(?!\$)'
        )

    def backslash_escape_rule(self, text: str) -> str:
        """In math, convert standalone double backslash to quadruple backslash."""
        # Only convert exactly two backslashes that are not part of:
        # - a longer sequence of backslashes (already converted/intentional)
        # - escaped braces (\{, \}) produced by brace_escape_rule
        # This keeps the transform idempotent across multiple runs.
        pattern = re.compile(r'(?<!\\)\\\\(?!\\|[{}])')
        return pattern.sub(lambda _m: '\\\\\\\\', text)

    def brace_escape_rule(self, text: str) -> str:
        """In math, escape curly braces, avoiding double-escaping."""
        # C# input.Replace("\\{", "\\\\{")
        # Idempotent: match \\{ OR \{
        def replace_brace(match):
            found = match.group(0)
            # If it starts with exactly two backslashes (\\{), it's already processed.
            if found.startswith('\\\\'):
                return found
            # If it starts with one backslash (\{), convert to two (\\{).
            # found[1:] is the brace ({ or })
            return '\\\\' + found[1:]
            
        # Match \\{ or \{ (and \} or \})
        # We use raw strings to make the backslashes clearer.
        text = re.sub(r'\\\\\{|\\\{', replace_brace, text)
        text = re.sub(r'\\\\\}|\\\}', replace_brace, text)
        return text

    def asterisk_escape_rule(self, text: str) -> str:
        """In math, escape asterisks: * -> {\\*}, avoiding double-escaping."""
        # Idempotent: match {\*} OR *
        def replace_asterisk(match):
            found = match.group(0)
            if found == '{\\*}':
                return found
            return '{\\*}'
            
        return re.sub(r'\{\\\*\}|\*', replace_asterisk, text)

    def pipe_escape_rule(self, text: str) -> str:
        """In math, escape pipe characters: | -> \\|, avoiding double-escaping."""
        # Idempotent: match \| OR |
        def replace_pipe(match):
            found = match.group(0)
            if found == '\\|':
                return found
            return '\\|'
            
        return re.sub(r'\\\||\|', replace_pipe, text)

    def apostrophe_global_rule(self, text: str) -> str:
        """Global: replace apostrophes with HTML entity &#39;, avoiding double-escaping."""
        if not text:
            return ""
            
        # Note: &#39; is already protected by not matching '
        # So we just need to protect existing &#39; if we were replacing something else,
        # but here we just replace ' with &#39;. If ' is gone, nothing happens.
        
        result = []
        last_index = 0
        for match in self.protected_segments_re.finditer(text):
            if match.start() > last_index:
                plain = text[last_index:match.start()]
                result.append(plain.replace("'", "&#39;"))
            
            result.append(match.group(0))
            last_index = match.end()
            
        if last_index < len(text):
            tail = text[last_index:]
            result.append(tail.replace("'", "&#39;"))
            
        return "".join(result)

    def apply_math_rules(self, text: str) -> str:
        """Apply all math rules to a segment of text."""
        for rule in self.math_rules:
            text = rule(text)
        return text

    def process_body(self, text: str) -> str:
        """
        Processes only the body content of a Markdown file.
        """
        if not text:
            return ""

        # 1. Apply global rules
        text = self.apostrophe_global_rule(text)

        # 2. Process display math ($$ ... $$)
        def replace_display(match):
            content = match.group('content')
            converted = self.apply_math_rules(content)
            return f"$${converted}$$"

        text = self.display_math_re.sub(replace_display, text)

        # 3. Process inline math ($ ... $)
        def replace_inline(match):
            content = match.group('content')
            converted = self.apply_math_rules(content)
            return f"${converted}$"

        text = self.inline_math_re.sub(replace_inline, text)

        return text

    def process_file_content(self, content: str) -> str:
        """
        Splits Front Matter from Body, processes Body, and recombines.
        """
        # Hexo Front Matter is between two --- at the start of the file
        parts = content.split('---', 2)
        
        # parts[0] is usually empty if file starts with ---
        # parts[1] is the YAML front matter
        # parts[2] is the body content
        
        if len(parts) >= 3 and content.startswith('---'):
            front_matter = parts[1]
            body = parts[2]
            processed_body = self.process_body(body)
            return f"---{front_matter}---{processed_body}"
        else:
            # No front matter found or not at start, process entire text
            return self.process_body(content)

def process_file(file_path: Path, converter: MarkdownConverter, base_dir: Path = None):
    """
    Processes a single file and handles logging/errors.
    """
    try:
        if base_dir:
            display_path = file_path.relative_to(base_dir)
        else:
            display_path = file_path
            
        print(f"Processing: {display_path}")
        
        # Read file with utf-8
        content = file_path.read_text(encoding='utf-8')
        
        # Process content
        processed_content = converter.process_file_content(content)
        
        # Write back to file with utf-8
        file_path.write_text(processed_content, encoding='utf-8')
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory_path: str):
    converter = MarkdownConverter()
    base_dir = Path(directory_path)
    
    if not base_dir.exists():
        print(f"Error: Path '{directory_path}' does not exist.")
        return

    if base_dir.is_file():
        if base_dir.suffix.lower() == '.md':
            process_file(base_dir, converter)
        else:
            print(f"Error: '{directory_path}' is not a Markdown file.")
        return

    if not base_dir.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        return

    # Recursively find all .md files
    md_files = list(base_dir.rglob("*.md"))
    print(f"Found {len(md_files)} Markdown files in {base_dir}")

    for file_path in md_files:
        process_file(file_path, converter, base_dir)

def main():
    parser = argparse.ArgumentParser(description="Batch process Hexo Markdown files for math and apostrophe safety.")
    parser.add_argument(
        "path", 
        type=str, 
        nargs="?",
        default="source/_posts", 
        help="Directory or single file containing Hexo Markdown files (default: source/_posts)"
    )
    
    args = parser.parse_args()
    process_directory(args.path)

if __name__ == "__main__":
    main()
