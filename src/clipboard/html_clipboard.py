import re
from typing import Optional
from typing import TypeVar


ENCODING = 'UTF-8'
HTML_ENCODING = ENCODING


A = TypeVar('A', str, bytes)


class HTMLClipboard:
    """Windows HTML Clipboard"""

    version = 0.9
    template = """
    Version:{version}
    StartHTML:{start_html_byte}
    EndHTML:{end_html_byte}
    StartFragment:{start_fragment_byte}
    EndFragment:{end_fragment_byte}
    SourceURL:{source_url}
    <html>
    <body>
    <!--StartFragment-->
    {fragment}
    <!--EndFragment-->
    </body>
    </html>
    """
    template = '\n'.join(
        [i for i in map(str.strip, template.splitlines()) if i]
    )

    def __init__(self, content: str = ''):

        self.fragments: list[str] = []

        self.start_html: int = -1
        self.end_html: int = -1

        self.start_fragment: int = -1
        self.end_fragment: int = -1

        # Optional
        self.start_selection: Optional[str] = None
        self.end_selection: Optional[str] = None

        # WIP
        self.content: str = content
        self.raw: bytes = content.encode(encoding=HTML_ENCODING)

    def generate_template(self) -> str:

        fragments: list[str] = (
            self.fragments if self.fragments else [self.content]
        )

        # Generate Fragments
        result: str = self.generate_fragments(fragments)
        # Generate HTML
        result = self.generate_html(result)
        # Add Header
        result = self.generate_header(result)
        # Get Byte Counts
        result = self.add_byte_counts(result)

        return result

    def generate_fragments(self, fragments: list) -> str:

        results: list[str] = []
        for fragment in fragments:
            results.append('<!--StartFragment-->')
            results.append(f'{fragment}')
            results.append('<!--EndFragment-->')

        # Clean
        result: str = '\n'.join(results)

        return result

    def generate_html(self, string: str) -> str:

        lines = string.splitlines()
        body = ['<body>'] + lines + ['</body>']
        html = ['<html>'] + body + ['</html>']

        return '\n'.join(html)

    def generate_header(self, string: str) -> str:

        lines = string.splitlines()

        version = self.version
        start_html_byte = self.start_html
        end_html_byte = self.end_html
        start_fragment_byte = self.start_fragment
        end_fragment_byte = self.end_fragment
        source_url = None

        if source_url is not None:
            lines.insert(0, f'SourceURL:{source_url}')
        lines.insert(0, f'EndFragment:{end_fragment_byte}')
        lines.insert(0, f'StartFragment:{start_fragment_byte}')
        lines.insert(0, f'EndHTML:{end_html_byte}')
        lines.insert(0, f'StartHTML:{start_html_byte}')
        lines.insert(0, f'Version:{version}')

        return '\n'.join(lines)

    def add_byte_counts(self, content: str) -> str:

        # Check
        current_values = self.get_byte_values(content)
        if all((i is not None and i != -1) for i in current_values.values()):
            content = self.update_byte_counts(content)
            return content

        # Setup
        content_bytes: bytes = content.encode(encoding=HTML_ENCODING)

        # Blocks to find
        html_start = '<html>'.encode(encoding=HTML_ENCODING)
        html_end = '</html>'.encode(encoding=HTML_ENCODING)
        fragment_start = '<!--StartFragment-->'.encode(encoding=HTML_ENCODING)
        fragment_end = '<!--EndFragment-->'.encode(encoding=HTML_ENCODING)

        # Find Values
        found_html_start = content_bytes.find(html_start)
        found_html_end = content_bytes.find(html_end)
        found_fragment_start = content_bytes.find(fragment_start)
        found_fragment_end = content_bytes.find(fragment_end)

        # Fix Values
        if HTML_ENCODING == 'UTF-8':
            found_html_end += len(html_end)
            found_fragment_start += len(fragment_start)

        # Set Values
        self.start_html = found_html_start
        self.end_html = found_html_end
        self.start_fragment = found_fragment_start
        self.end_fragment = found_fragment_end

        # Update
        content_bytes = self.update_byte_counts(content_bytes)

        # Clean Up
        result = content_bytes.decode(encoding=HTML_ENCODING)

        return self.add_byte_counts(result)

    def get_byte_values(self, content: str) -> dict:

        re_StartHTML = re.compile(r'StartHTML:(\d+)', flags=re.MULTILINE)
        StartHTML = int(
            re_StartHTML.findall(content)[0]
            if re_StartHTML.findall(content)
            else -1
        )

        re_EndHTML = re.compile(r'EndHTML:(\d+)', flags=re.MULTILINE)
        EndHTML = int(
            re_EndHTML.findall(content)[0]
            if re_EndHTML.findall(content)
            else -1
        )

        re_StartFragment = re.compile(
            r'StartFragment:(\d+)', flags=re.MULTILINE
        )
        StartFragment = int(
            re_StartFragment.findall(content)[0]
            if re_StartFragment.findall(content)
            else -1
        )

        re_EndFragment = re.compile(r'EndFragment:(\d+)', flags=re.MULTILINE)
        EndFragment = int(
            re_EndFragment.findall(content)[0]
            if re_EndFragment.findall(content)
            else -1
        )

        return {
            'StartHTML': StartHTML,
            'EndHTML': EndHTML,
            'StartFragment': StartFragment,
            'EndFragment': EndFragment,
        }

    def update_byte_counts(self, content: A) -> A:

        data: str
        if isinstance(content, bytes):
            data = content.decode(encoding=HTML_ENCODING)
        elif isinstance(content, str):
            data = content
        else:
            raise TypeError(f'{type(content)} is not a valid type')

        re_value = r'(None|-?\d+)'

        re_StartHTML = re.compile(fr'StartHTML:{re_value}', flags=re.MULTILINE)
        re_EndHTML = re.compile(fr'EndHTML:{re_value}', flags=re.MULTILINE)
        re_StartFragment = re.compile(
            fr'StartFragment:{re_value}', flags=re.MULTILINE
        )
        re_EndFragment = re.compile(
            fr'EndFragment:{re_value}', flags=re.MULTILINE
        )

        data = re.sub(re_StartHTML, fr'StartHTML:{self.start_html}', data)
        data = re.sub(re_EndHTML, fr'EndHTML:{self.end_html}', data)
        data = re.sub(
            re_StartFragment, fr'StartFragment:{self.start_fragment}', data
        )
        data = re.sub(
            re_EndFragment, fr'EndFragment:{self.end_fragment}', data
        )

        if isinstance(content, bytes):
            return data.encode(encoding=HTML_ENCODING)
        elif isinstance(content, str):
            return data
        else:
            raise TypeError(f'{type(content)} is not a valid type')
