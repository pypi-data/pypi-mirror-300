
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
