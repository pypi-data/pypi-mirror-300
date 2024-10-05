import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import { P as Plot$2, a as Plot } from './Plot-CgJX0SMu.js';
import { B as Block, S as Static } from './2-DZ7yOGfp.js';
import { B as BlockLabel } from './BlockLabel-AhkrKupZ.js';
import './Empty-DI3_iAt8.js';
import './index4-D_FyJKAV.js';

const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value = null } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { loading_status } = $$props;
  let { label } = $$props;
  let { show_label } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { theme_mode } = $$props;
  let { caption } = $$props;
  let { bokeh_version } = $$props;
  let { gradio } = $$props;
  let { show_actions_button = false } = $$props;
  let { _selectable = false } = $$props;
  let { x_lim = null } = $$props;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.theme_mode === void 0 && $$bindings.theme_mode && theme_mode !== void 0)
    $$bindings.theme_mode(theme_mode);
  if ($$props.caption === void 0 && $$bindings.caption && caption !== void 0)
    $$bindings.caption(caption);
  if ($$props.bokeh_version === void 0 && $$bindings.bokeh_version && bokeh_version !== void 0)
    $$bindings.bokeh_version(bokeh_version);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.show_actions_button === void 0 && $$bindings.show_actions_button && show_actions_button !== void 0)
    $$bindings.show_actions_button(show_actions_button);
  if ($$props._selectable === void 0 && $$bindings._selectable && _selectable !== void 0)
    $$bindings._selectable(_selectable);
  if ($$props.x_lim === void 0 && $$bindings.x_lim && x_lim !== void 0)
    $$bindings.x_lim(x_lim);
  return `${validate_component(Block, "Block").$$render(
    $$result,
    {
      padding: false,
      elem_id,
      elem_classes,
      visible,
      container,
      scale,
      min_width,
      allow_overflow: false
    },
    {},
    {
      default: () => {
        return `${validate_component(BlockLabel, "BlockLabel").$$render(
          $$result,
          {
            show_label,
            label: label || gradio.i18n("plot.plot"),
            Icon: Plot$2
          },
          {},
          {}
        )} ${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} ${validate_component(Plot, "Plot").$$render(
          $$result,
          {
            value,
            theme_mode,
            caption,
            bokeh_version,
            show_actions_button,
            gradio,
            _selectable,
            x_lim
          },
          {},
          {}
        )}`;
      }
    }
  )}`;
});

export { Plot as BasePlot, Index as default };
//# sourceMappingURL=Index13-CE1H5K8p.js.map
