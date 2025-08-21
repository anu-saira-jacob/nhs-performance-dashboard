from dash import html
import dash_mantine_components as dmc
from utils.help_text import HELP_PAGE_CONTENT


def _section_block(key: str, section: dict):
    def _render_body(body):
        from dash import dcc
        return dcc.Markdown(body, mathjax=False) if isinstance(body, str) else body

    return dmc.Stack(
        [
            # keep your H2 for the section title
            html.H2(section["title"], id=section["anchor"]),

            dmc.Text(section.get("overview", ""), size="sm"),

            *(
                dmc.Stack(
                    [
                        dmc.Title(s["heading"], order=4),          
                        _render_body(s["body"]),
                    ],
                    gap="sm",
                )
                for s in section.get("sections", [])
            ),

            dmc.Text("Further reading", fw=600, size="sm"),
            dmc.Stack(
                [
                    dmc.Anchor(l["label"], href=l["url"], target="_blank", size="sm")
                    for l in section.get("links", [])
                ],
                gap=2,
            ),
            dmc.Divider(my="lg"),
        ],
        gap="md",
    )




help_layout = dmc.MantineProvider(       
    withCssVariables=True,
    children=[
        dmc.Container(
            [
                html.H1("Help & Documentation"),
                dmc.Text(
                    "Short guidance for each page. Use the table of contents below or open help drawers from within each page.",
                    size="sm",
                    c="dimmed",
                ),
                dmc.Space(h=12),
                # TOC
                dmc.List(
                    [
                        dmc.ListItem(
                            dmc.Anchor(sec["title"], href=f"#{sec['anchor']}")
                        )
                        for sec in HELP_PAGE_CONTENT.values()
                    ],
                    spacing="xs",
                ),
                dmc.Divider(my="md"),
                # Sections
                *[_section_block(k, v) for k, v in HELP_PAGE_CONTENT.items()],
            ],
            fluid=True,
            my="lg",
        )
    ],
)
