class TemplateRenderer:

    def render(
        self,
        template: str,
        variables: dict[str, str],
    ) -> str:

        rendered = template

        for key, value in variables.items():

            rendered = rendered.replace(

                "{{" + key + "}}",

                value,

            )

        return rendered
