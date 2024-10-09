# standard library
from os import path

# pypi/conda library
from slugify import slugify

# plugins
from splashgen import Component


class Input(Component):
    def __init__(
        self, id: str, label: str = "", required: bool = False, placeholder: str = ""
    ) -> None:
        self.tag_name = "input"
        self.type = "text"
        self.id = id
        self.label = label
        self.required = required
        self.placeholder = placeholder

    def render(self) -> str:
        template_file = path.join(
            path.dirname(__file__), "..", "templates", "input.html.jinja"
        )
        return self.into_template(template_file=template_file)


class TextInput(Input):
    pass


class EmailInput(Input):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = "email"


class SelectInput(Input):
    def __init__(self, *args, options: list[str] = [], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tag_name = "select"
        self.options = options

    def render(self) -> str:
        self.opt_value_tuples = [
            o if type(o) is tuple else (o, slugify(o)) for o in self.options
        ]
        return super().render()


class Form(Component):
    def __init__(
        self,
        endpoint: str,
        inputs: list[str | tuple[str, str]] | None = None,
        submit_text: str = "Submit",
    ) -> None:
        super().__init__()
        self.endpoint = endpoint
        self.inputs = inputs if inputs is not None else {}
        self.submit_text = submit_text

    def render(self) -> str:
        template_file = path.join(
            path.dirname(__file__), "..", "templates", "form.html.jinja"
        )
        return self.into_template(template_file=template_file)
