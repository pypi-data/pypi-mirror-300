
import gradio as gr
from app import demo as app
import os

_docs = {'buttontip_component': {'description': 'Creates a button that can be assigned arbitrary .click() events. The value (label) of the button can be used as an input to the function (rarely used) or set via the output of a function.', 'members': {'__init__': {'value': {'type': 'str | Callable', 'default': '"Run"', 'description': 'Default text for the button to display. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.'}, 'variant': {'type': 'Literal["primary", "secondary", "stop"]', 'default': '"secondary"', 'description': "'primary' for main call-to-action, 'secondary' for a more subdued style, 'stop' for a stop button."}, 'size': {'type': 'Literal["sm", "lg"] | None', 'default': 'None', 'description': 'Size of the button. Can be "sm" or "lg".'}, 'icon': {'type': 'str | None', 'default': 'None', 'description': 'URL or path to the icon file to display within the button. If None, no icon will be displayed.'}, 'link': {'type': 'str | None', 'default': 'None', 'description': 'URL to open when the button is clicked. If None, no link will be used.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'interactive': {'type': 'bool', 'default': 'True', 'description': 'If False, the ButtonTip will be in a disabled state.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int | None', 'default': 'None', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'tooltip': {'type': 'str', 'default': 'None', 'description': None}, 'tooltip_color': {'type': 'str', 'default': '"#fff"', 'description': None}, 'tooltip_background_color': {'type': 'str', 'default': '"#000"', 'description': None}, 'x': {'type': 'int', 'default': 'None', 'description': 'Horizontal offset of the tooltip from the button.'}, 'y': {'type': 'int', 'default': 'None', 'description': 'Vertical offset of the tooltip from the button.'}}, 'postprocess': {'value': {'type': 'str | None', 'description': 'string corresponding to the button label'}}, 'preprocess': {'return': {'type': 'str | None', 'description': '(Rarely used) the `str` corresponding to the button label when the button is clicked'}, 'value': None}}, 'events': {'click': {'type': None, 'default': None, 'description': 'Triggered when the buttontip_component is clicked.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'buttontip_component': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_buttontip_component`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_buttontip_component/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_buttontip_component"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_buttontip_component
```

## Usage

```python

import gradio as gr
from gradio_buttontip_component import buttontip_component


def button_click(a,b):
    return "Button clicked!"

demo = gr.Interface(
    title="Button with Tooltip",
    description="This interface showcases a button with a tooltip.",
    fn=button_click,
    inputs=[
        # If X and Y are not set, the tip will be center-top aligned with the button
        buttontip_component(
            tooltip="Tooltip Text",
            tooltip_color="white",  # Custom color
            tooltip_background_color="red",
            value="Top Button"
        ),
        # Change X, Y values to position the tooltip
        buttontip_component(
            tooltip="Tooltip Text",
            tooltip_color="white",  # Custom color
            tooltip_background_color="green",
            x=50,  # No horizontal offset
            y=-20,  # Below the button
            value="Bottom Button"
        )
    ],
    outputs="text",
)


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `buttontip_component`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["buttontip_component"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["buttontip_component"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, (Rarely used) the `str` corresponding to the button label when the button is clicked.
- **As output:** Should return, string corresponding to the button label.

 ```python
def predict(
    value: str | None
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "buttontip_component-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          buttontip_component: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
