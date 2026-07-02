from platform_core.generator.renderer import TemplateRenderer


def test_render():

    renderer = TemplateRenderer()

    output = renderer.render(
        "Hello {{NAME}}",
        {
            "NAME": "Platform",
        },
    )

    assert output == "Hello Platform"
