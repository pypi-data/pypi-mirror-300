from .tex_config import TexConfig
import json
class Document:
    def __init__(self):
        self.components = []
        
    def add_component(self, component):
        self.components.append(component)    
    
    def to_latex(self, config : TexConfig):
        return '\n'.join([c.to_latex(config) for c in self.components])
    
    def to_json(self):
        obj = {
            'type': 'document',
            'components': [c.to_json() for c in self.components]
        }
        json_str = json.dumps(obj, indent=4)
        return json_str
        

class Paragraph:
    def __init__(self):
        self.components = []
    
    def add_component(self, component):
        self.components.append(component)
        
    def to_latex(self, config : TexConfig):
        return ''.join([c.to_latex(config) for c in self.components]) + '\n\n'
    
    def to_json(self):
        return {
            'type': 'paragraph',
            'components': [c.to_json() for c in self.components]
        }
    
class Text:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return config.apply('text', content=self.text)
    
    def to_json(self):
        return {
            'type': 'text',
            'text': self.text
        }
    
class InlineBold:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return config.apply('bold', content=self.text)
    
    def to_json(self):
        return {
            'type': 'inline_bold',
            'text': self.text
        }
    
class InlineItalic:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return config.apply('italic', content=self.text)
    
    def to_json(self):
        return {
            'type': 'inline_italic',
            'text': self.text
        }
    
class InlineCode:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return config.apply('inline_code', content=self.text)
    
    def to_json(self):
        return {
            'type': 'inline_code',
            'text': self.text
        }
    
class InlineFormula:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return config.apply('inline_formula', content=self.text)
    
    def to_json(self):
        return {
            'type': 'inline_formula',
            'text': self.text
        }
        
class FormulaBlock:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return config.apply('formula_block', content=self.text)
    
    def to_json(self):
        return {
            'type': 'formula_block',
            'text': self.text
        }
    
class CodeBlock:
    def __init__(self, lang = None):
        self.lang = lang if lang else 'text'
        self.code = []
        
    def add_code(self, code):
        self.code.append(code)
        
    def to_latex(self, config : TexConfig):
        return config.apply('code_block', code='\n'.join(self.code), lang=self.lang)
    def to_json(self):
        return {
            'type': 'code_block',
            'code': self.code,
            'lang': self.lang
        }
    
class Image:
    def __init__(self, path, caption):
        self.path = path
        self.caption = caption
        
    def to_latex(self, config : TexConfig):
        return config.apply('image', src=self.path, alt=self.caption)
    
    def to_json(self):
        return {
            'type': 'image',
            'path': self.path,
            'caption': self.caption
        }
    
class Heading:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        
    def to_latex(self, config : TexConfig):
        if self.level == 1:
            return config.apply('heading1', content=self.title)
        elif self.level == 2:
            return config.apply('heading2', content=self.title)
        elif self.level == 3:
            return config.apply('heading3', content=self.title)
        elif self.level == 4:
            return config.apply('heading4', content=self.title)
        else:
            return config.apply('bold', content=self.title)
        
    def to_json(self):
        return {
            'type': 'heading',
            'title': self.title,
            'level': self.level,
        }
    
class OrderedList:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def to_latex(self, config : TexConfig):
        return config.apply('ordered_list', items='\n'.join([i.to_latex(config) for i in self.items]))
    
    def to_json(self):
        return {
            'type': 'ordered_list',
            'items': [i.to_json() for i in self.items]
        }
    
class UnorderedList:
    
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def to_latex(self, config : TexConfig):
        return config.apply('unordered_list', items='\n'.join([i.to_latex(config) for i in self.items]))
    
    def to_json(self):
        return {
            'type': 'unordered_list',
            'items': [i.to_json() for i in self.items]
        }
    
class ListItem:
    def __init__(self):
        self.components = []
        
    def add_component(self, component):
        self.components.append(component)
        
    def to_latex(self, config : TexConfig):
        return config.apply('list_item', content=''.join([c.to_latex(config) for c in self.components]))
    
    def to_json(self):
        return {
            'type': 'list_item',
            'components': [c.to_json() for c in self.components]
        }
