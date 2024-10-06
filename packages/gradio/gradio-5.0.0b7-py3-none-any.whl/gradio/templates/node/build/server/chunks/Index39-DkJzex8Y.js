import { c as create_ssr_component, v as validate_component, a as createEventDispatcher, e as escape, b as add_attribute } from './ssr-Cz1f32Mr.js';
import { B as Block, S as Static, h as BlockTitle } from './2-BZ3PdVP1.js';
export { default as BaseExample } from './Example11-sU8ETKvc.js';
import './index4-D_FyJKAV.js';

const css = {
  code: "input.svelte-56zyyb{display:block;position:relative;background:var(--background-fill-primary);line-height:var(--line-sm)}",
  map: '{"version":3,"file":"Colorpicker.svelte","sources":["Colorpicker.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { createEventDispatcher, afterUpdate } from \\"svelte\\";\\nimport { BlockTitle } from \\"@gradio/atoms\\";\\nexport let value = \\"#000000\\";\\nexport let value_is_output = false;\\nexport let label;\\nexport let info = void 0;\\nexport let disabled = false;\\nexport let show_label = true;\\nconst dispatch = createEventDispatcher();\\nfunction handle_change() {\\n    dispatch(\\"change\\", value);\\n    if (!value_is_output) {\\n        dispatch(\\"input\\");\\n    }\\n}\\nafterUpdate(() => {\\n    value_is_output = false;\\n});\\n$: value, handle_change();\\n<\/script>\\n\\n<label class=\\"block\\">\\n\\t<BlockTitle {show_label} {info}>{label}</BlockTitle>\\n\\t<input type=\\"color\\" bind:value on:focus on:blur {disabled} />\\n</label>\\n\\n<style>\\n\\tinput {\\n\\t\\tdisplay: block;\\n\\t\\tposition: relative;\\n\\t\\tbackground: var(--background-fill-primary);\\n\\t\\tline-height: var(--line-sm);\\n\\t}</style>\\n"],"names":[],"mappings":"AA2BC,mBAAM,CACL,OAAO,CAAE,KAAK,CACd,QAAQ,CAAE,QAAQ,CAClB,UAAU,CAAE,IAAI,yBAAyB,CAAC,CAC1C,WAAW,CAAE,IAAI,SAAS,CAC3B"}'
};
const Colorpicker = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value = "#000000" } = $$props;
  let { value_is_output = false } = $$props;
  let { label } = $$props;
  let { info = void 0 } = $$props;
  let { disabled = false } = $$props;
  let { show_label = true } = $$props;
  const dispatch = createEventDispatcher();
  function handle_change() {
    dispatch("change", value);
    if (!value_is_output) {
      dispatch("input");
    }
  }
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.value_is_output === void 0 && $$bindings.value_is_output && value_is_output !== void 0)
    $$bindings.value_is_output(value_is_output);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.info === void 0 && $$bindings.info && info !== void 0)
    $$bindings.info(info);
  if ($$props.disabled === void 0 && $$bindings.disabled && disabled !== void 0)
    $$bindings.disabled(disabled);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  $$result.css.add(css);
  {
    handle_change();
  }
  return `<label class="block">${validate_component(BlockTitle, "BlockTitle").$$render($$result, { show_label, info }, {}, {
    default: () => {
      return `${escape(label)}`;
    }
  })} <input type="color" ${disabled ? "disabled" : ""} class="svelte-56zyyb"${add_attribute("value", value, 0)}> </label>`;
});
const Colorpicker$1 = Colorpicker;
const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { label = "ColorPicker" } = $$props;
  let { info = void 0 } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value } = $$props;
  let { value_is_output = false } = $$props;
  let { show_label } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { loading_status } = $$props;
  let { gradio } = $$props;
  let { interactive } = $$props;
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.info === void 0 && $$bindings.info && info !== void 0)
    $$bindings.info(info);
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.value_is_output === void 0 && $$bindings.value_is_output && value_is_output !== void 0)
    $$bindings.value_is_output(value_is_output);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    $$rendered = `   ${validate_component(Block, "Block").$$render(
      $$result,
      {
        visible,
        elem_id,
        elem_classes,
        container,
        scale,
        min_width
      },
      {},
      {
        default: () => {
          return `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} ${validate_component(Colorpicker$1, "Colorpicker").$$render(
            $$result,
            {
              label,
              info,
              show_label,
              disabled: !interactive,
              value,
              value_is_output
            },
            {
              value: ($$value) => {
                value = $$value;
                $$settled = false;
              },
              value_is_output: ($$value) => {
                value_is_output = $$value;
                $$settled = false;
              }
            },
            {}
          )}`;
        }
      }
    )}`;
  } while (!$$settled);
  return $$rendered;
});

export { Colorpicker$1 as BaseColorPicker, Index as default };
//# sourceMappingURL=Index39-DkJzex8Y.js.map
