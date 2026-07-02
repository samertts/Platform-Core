from string import Template


class TemplateEngine:
    @staticmethod
    def render(template: str, values: dict):

        return Template(template).safe_substitute(values)
