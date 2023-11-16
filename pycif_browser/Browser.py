"""
Module browser.

makes it easy to look through existing modules
"""
from typing import List
from importlib.resources import read_text
from importlib.resources import files as package_files
from importlib.resources import as_file as traversable_as_file
import inspect
from pathlib import Path
from dataclasses import dataclass, field
import sys
import shutil
from io import StringIO

import jinja2

from pycif.draw.Component import Component

from pycif_browser.themes import FirstLight
from pycif.helpers.docparse import split_docstring

from pycif_browser.exporter import export_compo_as_inline
from pycif_browser.contexts import (
    CTXBrowser,
    CTXOption,
    CTXLayer,
    CTXInterface,
    CTXMark,
    CTXMethod,
    CTXComponent
    )

@dataclass
class ComponentEntry(object):
    """
    Entry for a component in the modulebrowser database.
    """

    interfaces: List[Component] = field(
        default_factory=lambda: [],
        )

    layer_image_strings: List[str] = field(
        default_factory=lambda: [],
        )

class Browser(object):
    def __init__(self):
        self.components = {}
        self.ctx_browser = CTXBrowser()

    def register_component(self, new_compo):
        """
        Add new component to database
        """
        new_entry = ComponentEntry()
        #for existing_compo, existing_entry in self.components.items():

            #if existing_compo.is_interface(new_compo):
            #    new_entry.interfaces.append(existing_compo)

            #elif new_compo.is_interface(existing_compo):
            #    existing_entry.interfaces.append(new_compo)

        self.components[new_compo] = new_entry

    def register_package(self, package):
        """
        Add new package into database
        """
        # TODO if not defined, export all components and throw warning.
        for compo in package.PC_EXPORT_COMPONENTS:
            self.register_component(compo)

    def _generate_component_context(self, compo):
        """
        Generate jinja2 context for one component
        """
        entry = self.components[compo]
        module = inspect.getmodule(compo)
        instance = compo()

        package_name = module.__name__.split('.')[0]
        compo_docstring = split_docstring(compo.__doc__)
        tags = getattr(instance, 'browser_tags', [])

        self.ctx_browser.all_tags.update(tags)
        self.ctx_browser.all_packages.add(package_name)

        self.ctx_browser.components.append(CTXComponent(
            name=compo.__name__,
            fancy_name=compo_docstring.heading,
            module_name=module.__name__,
            package_name=package_name,
            #author=sys.modules[module.__package__].__author__,
            author='John Doe',
            description=compo_docstring.description,
            options=[],
            interfaces=[],
            marks=[],
            methods=[],
            #options=[
            #    CTXOption(
            #        name=name,
            #        default_value=optspec.default,
            #        description=optspec.desc,
            #        shadow=optspec.shadow,
            #        )
            #    for name, optspec in compo.optspecs.items()
            #    ],
            layers=[
                CTXLayer(
                    index=i,
                    name=name,
                    image_string=image_string,
                    )
                for i, (name, image_string)
                in enumerate(
                    zip(
                        list(instance.layers),
                        entry.layer_image_strings,
                        strict=True,
                        )
                    )
                ],  # TODO
            #interfaces=[
            #    CTXInterface(
            #        name=interface.__name__,
            #        )
            #    for interface in entry.interfaces
            #    ],
            #marks=[
            #    CTXMark(
            #        name=mark_name,
            #        )
            #    for mark_name in instance.marks.keys()
            #    ],
            #methods=[
            #    CTXMethod(
            #        name=method_name,
            #        short_description=(s:=split_docstring(method.__doc__))[0],
            #        long_description=s[1],
            #        )
            #    for method_name, method in compo.get_custom_methods().items()
            #    ],
            #preview_image=self._generate_inline_preview_image(instance),
            tags=tags,
            ))

    def _generate_context(self):
        """
        Generate jinja2 context from database
        """
        for compo in self.components.keys():
            self._generate_component_context(compo)
        return self.ctx_browser.__dict__
        #return {
        #    'components': [
        #        self._generate_component_context(compo)
        #        for compo in self.components.keys()
        #        ],
        #    }

    def _copy_basedir(self, path: Path):
        """
        Move static files (basedir) from theme into target path
        """
        # FIXME this won't work if the package is installed as a zip,
        # it think.
        theme = FirstLight
        shutil.rmtree(path, ignore_errors=True)
        shutil.copytree(
            package_files(theme) / 'basedir',
            path,
            )

    def _generate_preview_image(self, path: Path, compo):
        """
        Generate preview images for component
        """
        instance = compo()


        compo_path = path / 'components' / compo.__name__
        compo_path.mkdir(parents=True)

        layer_image_strings = export_compo_as_inline(instance)
        return layer_image_strings
        #svg_path = compo_path / 'preview.svg'

        #with svg_path.open('w') as svgfile:
        #    svgexport(svgfile, instance)

    def _generate_inline_preview_image(self, instance):
        """
        Generate preview images for component
        """

        io = StringIO()
        svgexport(io, instance)
        svgstring = io.getvalue()
        io.close()
        return svgstring


    def _generate_preview_images(self, path: Path):
        """
        Generate preview images for all components in database
        """
        (path / 'components').mkdir()
        for compo, entry in self.components.items():
            layer_image_strings = self._generate_preview_image(path, compo)
            entry.layer_image_strings = layer_image_strings


    def generate_html(self, path: Path):
        self._copy_basedir(path)
        self._generate_preview_images(path)

        context = self._generate_context()
        theme = FirstLight
        env = jinja2.Environment(
            autoescape=False,
            undefined=jinja2.StrictUndefined,
            )
        template = env.from_string(read_text(theme, 'index.html'))
        (path / 'index.html').write_text(template.render(context))

