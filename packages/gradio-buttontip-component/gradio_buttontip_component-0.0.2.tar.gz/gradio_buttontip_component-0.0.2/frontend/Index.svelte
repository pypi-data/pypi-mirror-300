<script context="module" lang="ts">
  export { default as BaseButton } from "./shared/Button.svelte";
</script>

<script lang="ts">
  import type { Gradio } from "@gradio/utils";
  import { type FileData } from "@gradio/client";

  import Button from "./shared/Button.svelte";

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let value: string | null;
  export let variant: "primary" | "secondary" | "stop" = "secondary";
  export let interactive: boolean;
  export let size: "sm" | "lg" = "lg";
  export let scale: number | null = null;
  export let icon: FileData | null = null;
  export let link: string | null = null;
  export let min_width: number | undefined = undefined;
  export let tooltip;
  export let tooltip_color = "white"; // Default color
  export let tooltip_background_color = "black"; // Default color
  export let x = null; // Default horizontal offset
  export let y = null; // Default vertical offset
  export let gradio: Gradio<{
    click: never;
  }>;

function calculateTooltipPosition(event) {
    const button = event.currentTarget;
    const tooltipElement = button.querySelector(".tooltip-text") as HTMLElement;

    if (button && tooltipElement) {
      if (x !== null && y !== null) {
        tooltipElement.style.left = `${x}px`;
        tooltipElement.style.top = `${y}px`;
      } else {
        // Center the tooltip above the button
        const buttonRect = button.getBoundingClientRect();
        const tooltipRect = tooltipElement.getBoundingClientRect();

        // Center horizontally (already handled by CSS transform)
        tooltipElement.style.left = '50%';

        // Position above the button with some spacing
        const spacing = 5; // Pixels above the button
        tooltipElement.style.bottom = `${buttonRect.height + spacing}px`;

        // Reset top position
        tooltipElement.style.top = 'auto';
      }
    }
  }
  window.addEventListener("resize", () => {
    const tooltips = document.querySelectorAll(".tooltip-text");
    tooltips.forEach((tooltip) => {
      const button = tooltip.parentElement; // Get the parent button
      calculateTooltipPosition({ currentTarget: button });
    });
  });

  // Attach event listeners to buttons on mount
  function attachEventListeners() {
    const buttons = document.querySelectorAll(".tooltip-container button");
    buttons.forEach((button) => {
      button.addEventListener("mouseenter", calculateTooltipPosition);
      button.addEventListener("mouseleave", () => {
        const tooltipElement = button.querySelector(
          ".tooltip-text"
        ) as HTMLElement;
        tooltipElement.style.visibility = "hidden"; // Hide tooltip on mouse leave
      });
    });
  }

  // Call attachEventListeners on component mount
  window.addEventListener("load", attachEventListeners);
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="tooltip-container"
  style={`--tooltip-color: ${tooltip_color}; --tooltip-background-color: ${tooltip_background_color}`}
  on:mouseenter={calculateTooltipPosition}
>
  <Button
    {value}
    {variant}
    {elem_id}
    {elem_classes}
    {size}
    {scale}
    {link}
    {icon}
    {min_width}
    {visible}
    disabled={!interactive}
    on:click={() => gradio.dispatch("click")}
  >
    {value ? gradio.i18n(value) : ""}
  </Button>
  <span class="tooltip-text">{tooltip}</span>
</div>

<style>
  .tooltip-container {
    position: relative;
    display: inline-block;
    max-width: fit-content;
    min-width: auto;
  }

  .tooltip-text {
    visibility: hidden;
    color: var(--tooltip-color); /* Use the custom color */
    text-align: center;
    border-radius: 5px;
    padding: 5px 10px;
    position: absolute;
    z-index: 1;
    opacity: 0;
    transition: opacity 0.3s;
    background-color: var(
      --tooltip-background-color
    ); /* Use the custom color */
    white-space: nowrap; /* Prevent line breaks */
    transform: translateX(-50%);
  }

  /* Tooltip positioning */
  .tooltip-container:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
  }

  .tooltip-text::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: var(--tooltip-background-color) transparent transparent
      transparent;
  }
</style>
