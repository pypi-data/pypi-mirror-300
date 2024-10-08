import { c as create_ssr_component, v as validate_component, e as escape } from './ssr-Cz1f32Mr.js';
import { d as Button } from './2-B44WpJir.js';
import './index4-D_FyJKAV.js';
import 'tty';
import 'path';
import 'url';
import 'fs';

const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value } = $$props;
  let { variant = "secondary" } = $$props;
  let { interactive } = $$props;
  let { size = "lg" } = $$props;
  let { scale = null } = $$props;
  let { icon = null } = $$props;
  let { link = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { gradio } = $$props;
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.variant === void 0 && $$bindings.variant && variant !== void 0)
    $$bindings.variant(variant);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  if ($$props.size === void 0 && $$bindings.size && size !== void 0)
    $$bindings.size(size);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.icon === void 0 && $$bindings.icon && icon !== void 0)
    $$bindings.icon(icon);
  if ($$props.link === void 0 && $$bindings.link && link !== void 0)
    $$bindings.link(link);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  return `${validate_component(Button, "Button").$$render(
    $$result,
    {
      value,
      variant,
      elem_id,
      elem_classes,
      size,
      scale,
      link,
      icon,
      min_width,
      visible,
      disabled: !interactive
    },
    {},
    {
      default: () => {
        return `${escape(value ? gradio.i18n(value) : "")}`;
      }
    }
  )}`;
});

export { Button as BaseButton, Index as default };
//# sourceMappingURL=Index7-BhhoXQZs.js.map
