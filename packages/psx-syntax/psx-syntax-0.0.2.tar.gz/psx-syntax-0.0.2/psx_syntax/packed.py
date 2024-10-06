from __future__ import unicode_literals, print_function
import inspect
import re
import sys
import os
import functools
from pypeg2 import parse, compose, List, name, maybe_some, attr, optional, ignore, Symbol, some

whitespace = re.compile(r'\s+')
text = re.compile(r'[^<]+')

def snake_to_kebab(name):
    """Convert snake_case to kebab-case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '-', name).replace('_', '-').lower()

class Whitespace(object):
    """Matches one or more whitespace characters"""
    grammar = attr('value', whitespace)

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return "{indent}' '".format(indent=indent_str)

class Text(object):
    """Matches text between tags and/or inline code sections."""
    # Use re.DOTALL to allow newlines in text content
    grammar = attr('whitespace', optional(whitespace)), attr('value', re.compile(r'[^<{]+', re.DOTALL))

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        # Combine whitespace and value
        text_content = f"{self.whitespace or ''}{self.value}"
        # Use repr to generate a valid Python string literal
        text_literal = repr(text_content)
        return f"{indent_str}{text_literal}"

class DoubleString(object):
    """Matches a double-quote delimited string."""
    grammar = '"', attr('value', re.compile(r'[^"]*')), '"'

    def compose(self, parser):
        return "'%s'" % self.value
    
class SingleString(object):
    """Matches a single-quote delimited string."""
    grammar = "'", attr('value', re.compile(r"[^']*")), "'"

    def compose(self, parser):
        return "'%s'" % self.value

class InlineCode(object):
    """Matches arbitrary Python code within a curly braces."""
    grammar = '{', attr('code', re.compile(r'[^}]*')), '}'

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return "{indent}{code}".format(
            indent=indent_str,
            code=self.code
        )
    
class StyleAttribute(object):
    """Matches inline styles and converts them to kebab-case CSS strings."""
    grammar = '{', '{', attr('styles', maybe_some(name(), ':', optional(whitespace), [SingleString, DoubleString, InlineCode], optional(whitespace), optional(','), optional(whitespace))), '}', '}'

    def compose(self, parser, indent=0):
        
        styles_str = []

        for i in range(len(self.styles)):
            if i % 4 == 0:

                style_name = self.styles[i].thing
                style_name_kebab = snake_to_kebab(style_name)
                style_value = self.styles[i + 2].value

                parsed_result = f"{style_name_kebab}: {style_value};"

                styles_str.append(parsed_result)

        composed_styles = ''.join(styles_str)

        return composed_styles

class Attribute(object):
    """Matches an attribute formatted as either: key="value" or key={value} to handle strings and
    inline code in a similar style to JSX.
    """
    grammar = name(), '=', attr('value', [StyleAttribute, SingleString, DoubleString, InlineCode])

    def compose(self, parser, indent=0):
        indent_str = indent * "    "

        if isinstance(self.value, SingleString):
            quote = "'"
        elif isinstance(self.value, DoubleString):
            quote = '"'
        else:
            quote = "'"

        value = self.value.compose(parser)

        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            value = value[1:-1]

        result_string = f"{indent_str}{quote}{self.name}{quote}: {quote}{value}{quote},"

        return result_string

class Attributes(List):
    """Matches zero or more attributes"""
    grammar = maybe_some(optional(whitespace), [StyleAttribute, Attribute])

    def compose(self, parser, followed_by_children, indent):
        indent_str = indent * "    "

        if not len(self):
            indented_paren = '{indent}{{}},\n'.format(indent=indent_str)
            return indented_paren if followed_by_children else ''

        text = []
        text.append('{indent}{{\n'.format(indent=indent_str))
        for entry in self:
            if not isinstance(entry, str):
                text.append(entry.compose(parser, indent=indent+1))
                text.append('\n')
        text.append('{indent}}},\n'.format(indent=indent_str))
        composed_text = ''.join(text)
        
        return composed_text

class ComponentName(object):
    """A standard name or symbol beginning with an uppercase letter."""
    grammar = attr('first_letter', re.compile(r'[A-Z]')), attr('rest', optional(Symbol))

    def compose(self):
        return self.first_letter + (self.rest if self.rest else '')
    
class SelfClosingTag(object):
    """Matches a self-closing tag and all of its attributes."""
    
    SELF_CLOSING_TAGS = [
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    ]

    grammar = '<', attr('name', re.compile('|'.join(SELF_CLOSING_TAGS))), attr('attributes', Attributes), optional(whitespace), '>'

    def get_name(self):
        return "'%s'" % self.name

    def compose(self, parser, indent=0, first=False):

        text = []

        indent = int(indent)
        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_contents = bool(self.attributes)
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        name = self.get_name()

        text.append(
            "{indent}Elem({paren_sep}{indent_plus}{name}{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=name,
                paren_sep=paren_sep,
                contents_sep=contents_sep,
            )
        )

        composed_attributes = self.attributes.compose(parser, followed_by_children=False, indent=indent + 1)
        text.append(composed_attributes)

        text.append(f"{end_indent_str})")  # Close the 'Elem' for self-closing tag

        return ''.join(text)
    
class PsxTag(object):
    """Matches a PSX tag and all of its attributes."""

    grammar = '<', name(), attr('attributes', Attributes), ignore(whitespace), '/>'

    def get_name(self):
        return "'%s'" % self.name

    def compose(self, parser, indent=0, first=False):
        text = []

        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_contents = bool(self.attributes)
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        text.append(
            "{indent}Elem({paren_sep}{indent_plus}{name}{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=self.get_name(),
                paren_sep=paren_sep,
                contents_sep=contents_sep,
            )
        )
        text.append(self.attributes.compose(parser, followed_by_children=False, indent=indent+1))
        text.append(
            "{indent})".format(
                indent=end_indent_str if has_contents else '',
            )
        )

        return ''.join(text)

class ComponentTag(PsxTag):
    """Matches a self-closing tag with a name that starts with an uppercase letter."""
    grammar = ('<', attr('name', ComponentName), attr('attributes', Attributes), ignore(whitespace), '/>')

    def get_name(self):
        return self.name.compose()

class PairedTag(object):
    """Matches an open/close tag pair and all of its attributes and children."""
    @staticmethod
    def parse(parser, text, pos):
        try:
            result = PairedTag()
            text, _ = parser.parse(text, '<')
            text, tag = parser.parse(text, Symbol)
            result.name = tag
            text, attributes = parser.parse(text, Attributes)
            result.attributes = attributes
            text, _ = parser.parse(text, '>')
            text, children = parser.parse(text, TagChildren)
            result.children = children
            text, _ = parser.parse(text, '</')
            text, _ = parser.parse(text, result.name)
            text, _ = parser.parse(text, '>')
            return text, result
        except SyntaxError as e:
            return text, e

        return text, result

    def compose(self, parser, indent=0, first=False):

        text = []

        indent = int(indent)
        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_children = bool(self.children)
        has_attributes = bool(self.attributes)
        has_contents = has_children or has_attributes
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        text.append(
            "{indent}Elem({paren_sep}{indent_plus}'{name}'{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=self.name,
                paren_sep=paren_sep,
                contents_sep=contents_sep
            )
        )
        text.append(
            self.attributes.compose(parser, followed_by_children=has_children, indent=indent+1)
        )
        text.append(self.children.compose(parser, indent=indent+1))
        text.append(
            "{indent})".format(
                indent=end_indent_str if has_contents else '',
                )
            )

        return ''.join(text)

tags = [ComponentTag, SelfClosingTag, PsxTag, PairedTag]

class TagChildren(List):
    """Matches valid tag children which can be other tags, plain text, {values} or a mix of all three."""
    grammar = maybe_some(tags + [Text, InlineCode, Whitespace])

    def compose(self, parser, indent=0):
        text = []
        for entry in self:
            text.append(entry.compose(parser, indent=indent))
            text.append(',\n')

        return ''.join(text)

class PackedBlock(List):
    """Matches multi-line block of Packed syntax where the syntax starts on the first line"""
    grammar = attr('line_start', re.compile(r'[^#<\n]+')), tags

    def compose(self, parser, attr_of=None):
        text = [self.line_start]
        indent_text = re.match(r' *', self.line_start).group(0)
        indent = len(indent_text) / 4
        for entry in self:
            if isinstance(entry, str):
                text.append(entry)
            else:
                text.append(entry.compose(parser, indent=indent, first=True))

        return ''.join(text)

class NonPackedLine(List):
    """Matches a line without Packed syntax."""
    grammar = attr('content', re.compile('.*')), '\n'

    def compose(self, parser, attr_of=None):
        return '%s\n' % self.content

line_without_newline = re.compile(r'.+')

class CodeBlock(List):
    """Top level grammar representing a block of code with packed syntax and non-packed lines."""
    grammar = maybe_some([PackedBlock, NonPackedLine, line_without_newline])

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            if isinstance(entry, str):
                text.append(entry)
            else:
                text.append(entry.compose(parser))

        return ''.join(text)

def format_attribute(key, value):
    """Handles the output format for an attribute to the final html"""
    return '{name}="{value}"'.format(name=key, value=value)

def to_html(entity):
    """Converts entity to output HTML."""
    if isinstance(entity, list):
        return ''.join(map(to_html, entity))

    if hasattr(entity, 'to_html'):
        return entity.to_html()
    else:
        return str(entity)

class Elem(object):
    """Represents an HTML element."""
    def __init__(self, name, attributes=None, *children):
        self.name = name
        self.children = children

        # Ensure that attributes are composed if they are not already
        if isinstance(attributes, Attributes):
            # Compose the attributes if they are passed as an Attributes object
            self.attributes = attributes.compose(None, followed_by_children=False, indent=0)
        else:
            # Assume attributes are already composed
            self.attributes = attributes or {}

    def to_html(self):

        # Ensure attributes are being processed
        if inspect.isclass(self.name):
            assert not self.children
            instance = self.name(**self.attributes)
            output = instance.render()
            return to_html(output)

        # Check how attributes are being formatted
        if self.attributes:
            attribute_text = ' '.join(
                map(
                    lambda item: format_attribute(item[0], item[1]),
                    self.attributes.items()
                )
            )
        else:
            attribute_text = ''

        if attribute_text:
            attribute_text = ' ' + attribute_text

        # Handle children elements
        children_text = ''
        if self.children:
            children_text = ''.join(map(to_html, self.children))

        html = "<{name}{attributes}>{children}</{name}>".format(
            name=self.name,
            attributes=attribute_text,
            children=children_text
        )
        return html

class Component(object):
    """Component base class similar to React components."""
    def __init__(self, **props):
        # Provide default style prop if not already specified
        self.props = props
        if 'style' not in self.props:
            self.props['style'] = ''  # Default to an empty string

    def apply_styles(self, elem):
        """Recursively apply the component's style prop to all Elem instances."""
        if isinstance(elem, Elem):

            if 'style' in self.props and self.props['style']:
                existing_style = elem.attributes.get('style', '')
                new_style = f"{existing_style} {self.props['style']}".strip()
                elem.attributes['style'] = new_style
        
        # Recursively apply styles to child elements
        if hasattr(elem, 'children'):
            for child in elem.children:
                self.apply_styles(child)

    def render(self):
        elem = self.psx_render()
        self.apply_styles(elem)
        return elem
    
    def psx_render(self):
        raise NotImplementedError
    
def packed(func):
    """Decorator function for packed functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        text = to_html(result)
        return text
    return wrapper

def translate(code):
    
    result = parse(code, CodeBlock, whitespace=None)
    composed_code = compose(result)
    print(composed_code)
    return composed_code

def translate_file(pyx_file, py_path):
    """Reads & translates the provided .pyx file and writes the result to the provided .py file path."""
    pkd_contents = open(pyx_file, 'r').read()

    try:
        py_contents = translate(pkd_contents)
    except SyntaxError:
        sys.stderr.write('Failed to convert: %s' % pyx_file)
        return

    open(py_path, 'w').write(py_contents)

def translate_file_in_memory(pyx_file):
    """Reads & translates the provided .pyx file and returns the translated Python code."""
    pkd_contents = open(pyx_file, 'r').read()

    try:
        py_contents = translate(pkd_contents)
    except SyntaxError:
        sys.stderr.write('Failed to convert: %s' % pyx_file)
        return None

    return py_contents

def main(args):
    target_directory = args[0]
    
    for root, dirs, files in os.walk(target_directory):
        for filename in files:
            if filename.endswith('.pyx'):
                py_filename = '{}.py'.format(filename[:-4])
                
                full_pkd_path = os.path.join(root, filename)
                full_py_path = os.path.join(root, py_filename)
                
                translate_file(full_pkd_path, full_py_path)
    return 0

def psx_import(psx_file_path, component_to_import):

    psx_dir = os.path.dirname(psx_file_path) or os.getcwd()

    original_dir = os.getcwd()
    original_sys_path = sys.path.copy()

    os.chdir(psx_dir)

    sys.path.insert(0, psx_dir)

    translated_code = translate_file_in_memory(psx_file_path)

    exec_context = {
        'Elem': Elem,
        'Component': Component,
    }

    exec(translated_code, exec_context)

    imported_component = exec_context.get(component_to_import)

    os.chdir(original_dir)
    sys.path = original_sys_path

    return imported_component

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))