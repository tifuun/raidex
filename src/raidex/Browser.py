"""
Module browser.

makes it easy to look through existing modules
"""
from typing import List, Dict
from importlib.resources import read_text
from importlib.resources import files as package_files
import inspect
from pathlib import Path
from dataclasses import dataclass, field
import shutil
from io import StringIO

import jinja2

import raimad as rai

from raidex.themes import FirstLight

from raidex.exporter import export_compo_as_inline
from raidex.contexts import (
    CTXBrowser,
    CTXOption,
    CTXLayer,
    CTXInterface,
    CTXMark,
    CTXMethod,
    CTXCompo
    )

@dataclass
class compoEntry(object):
    """
    Entry for a compo in the modulebrowser database.
    """

    #interfaces: List[compo] = field(
    #    default_factory=lambda: [],
    #    )

    layer_image_strings: Dict[str, str] = field(
        default_factory=lambda: {}
        )

class Browser(object):
    def __init__(self):
        self.compos = {}
        self.ctx_browser = CTXBrowser()

    def register_compo(self, new_compo):
        """
        Add new compo to database
        """
        new_entry = compoEntry()
        #for existing_compo, existing_entry in self.compos.items():

            #if existing_compo.is_interface(new_compo):
            #    new_entry.interfaces.append(existing_compo)

            #elif new_compo.is_interface(existing_compo):
            #    existing_entry.interfaces.append(new_compo)

        self.compos[new_compo] = new_entry

    #def register_package(self, package):
    #    """
    #    Add new package into database
    #    """
    #    # TODO if not defined, export all compos and throw warning.
    #    for compo in package.PC_EXPORT_compoS:
    #        self.register_compo(compo)

    def _generate_compo_context(self, compo):
        """
        Generate jinja2 context for one compo
        """
        entry = self.compos[compo]
        module = inspect.getmodule(compo)
        instance = compo(**{
            option.name: option.browser_default
            for option in compo.Options.values()
            if option.browser_default is not rai.Empty
            })

        package_name = module.__name__.split('.')[0]
        compo_docstring = rai.split_docstring(compo.__doc__)
        tags = getattr(instance, 'browser_tags', [])

        self.ctx_browser.all_tags.update(tags)
        self.ctx_browser.all_packages.add(package_name)

        self.ctx_browser.compos.append(CTXCompo(
            name=compo.__name__,
            fancy_name=compo_docstring.heading or compo.__name__,
            module_name=module.__name__,
            package_name=package_name,
            #author=sys.modules[module.__package__].__author__,
            author='John Doe',
            description=compo_docstring.description,
            interfaces=[],
            marks=[],
            methods=[],
            options=[
                CTXOption(
                    name=opt.name,
                    default=str(opt.default),
                    desc=opt.desc,
                    annot=str(opt.annot),
                    )
                for opt in compo.Options.values()
                ],
            layers=[
                CTXLayer(
                    index=i,
                    name=(
                        instance.Layers[i]
                        if i in instance.Layers.keys()
                        else ""
                        ),
                    image_string=image_string,
                    )
                for i, image_string
                in enumerate(entry.layer_image_strings)
                ],  # TODO everything is broken
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
        for compo in self.compos.keys():
            self._generate_compo_context(compo)
        return self.ctx_browser.__dict__
        #return {
        #    'compos': [
        #        self._generate_compo_context(compo)
        #        for compo in self.compos.keys()
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
        Generate preview images for compo
        """

        # TODO this is copy-pasted
        instance = compo(**{
            option.name: option.browser_default
            for option in compo.Options.values()
            if option.browser_default is not rai.Empty
            })

        compo_path = path / 'compos' / compo.__name__
        compo_path.mkdir(parents=True)

        layer_image_strings = export_compo_as_inline(instance)
        return layer_image_strings
        #svg_path = compo_path / 'preview.svg'

        #with svg_path.open('w') as svgfile:
        #    svgexport(svgfile, instance)

    def _generate_inline_preview_image(self, instance):
        """
        Generate preview images for compo
        """

        io = StringIO()
        svgexport(io, instance)
        svgstring = io.getvalue()
        io.close()
        return svgstring


    def _generate_preview_images(self, path: Path):
        """
        Generate preview images for all compos in database
        """
        (path / 'compos').mkdir()
        for compo, entry in self.compos.items():
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

