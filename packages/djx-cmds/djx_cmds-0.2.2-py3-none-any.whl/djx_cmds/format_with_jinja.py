import os
import pathlib
import inflection
from jinja2 import Environment, FileSystemLoader


def format_with_jinja(data, template_src):
    base_folder = pathlib.Path(__file__).resolve().parent
    env = Environment(loader=FileSystemLoader(base_folder))
    env.filters['underscore'] = inflection.underscore
    env.filters['camelize'] = inflection.camelize
    env.filters['dasherize'] = inflection.dasherize
    env.filters['pluralize'] = inflection.pluralize
    env.filters['singularize'] = inflection.singularize
    env.filters['str'] = str

    with open(os.path.join(base_folder, 'templates', template_src), "r", encoding="utf-8") as f:
        template = env.from_string(f.read())

    result = template.render(**data)
    return result
