import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import { B as Block, S as Static, y as Textbox } from './2-B44WpJir.js';
export { default as BaseExample } from './Example2-BI1FX5Tw.js';
import './index4-D_FyJKAV.js';
import 'tty';
import 'path';
import 'url';
import 'fs';

const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { gradio } = $$props;
  let { label = "Textbox" } = $$props;
  let { info = void 0 } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value = "" } = $$props;
  let { lines } = $$props;
  let { placeholder = "" } = $$props;
  let { show_label } = $$props;
  let { max_lines } = $$props;
  let { type = "text" } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { submit_btn = null } = $$props;
  let { stop_btn = null } = $$props;
  let { show_copy_button = false } = $$props;
  let { loading_status = void 0 } = $$props;
  let { value_is_output = false } = $$props;
  let { rtl = false } = $$props;
  let { text_align = void 0 } = $$props;
  let { autofocus = false } = $$props;
  let { autoscroll = true } = $$props;
  let { interactive } = $$props;
  let { root } = $$props;
  let { max_length = void 0 } = $$props;
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
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
  if ($$props.lines === void 0 && $$bindings.lines && lines !== void 0)
    $$bindings.lines(lines);
  if ($$props.placeholder === void 0 && $$bindings.placeholder && placeholder !== void 0)
    $$bindings.placeholder(placeholder);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.max_lines === void 0 && $$bindings.max_lines && max_lines !== void 0)
    $$bindings.max_lines(max_lines);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.submit_btn === void 0 && $$bindings.submit_btn && submit_btn !== void 0)
    $$bindings.submit_btn(submit_btn);
  if ($$props.stop_btn === void 0 && $$bindings.stop_btn && stop_btn !== void 0)
    $$bindings.stop_btn(stop_btn);
  if ($$props.show_copy_button === void 0 && $$bindings.show_copy_button && show_copy_button !== void 0)
    $$bindings.show_copy_button(show_copy_button);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.value_is_output === void 0 && $$bindings.value_is_output && value_is_output !== void 0)
    $$bindings.value_is_output(value_is_output);
  if ($$props.rtl === void 0 && $$bindings.rtl && rtl !== void 0)
    $$bindings.rtl(rtl);
  if ($$props.text_align === void 0 && $$bindings.text_align && text_align !== void 0)
    $$bindings.text_align(text_align);
  if ($$props.autofocus === void 0 && $$bindings.autofocus && autofocus !== void 0)
    $$bindings.autofocus(autofocus);
  if ($$props.autoscroll === void 0 && $$bindings.autoscroll && autoscroll !== void 0)
    $$bindings.autoscroll(autoscroll);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  if ($$props.max_length === void 0 && $$bindings.max_length && max_length !== void 0)
    $$bindings.max_length(max_length);
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
        scale,
        min_width,
        allow_overflow: false,
        padding: container
      },
      {},
      {
        default: () => {
          return `${loading_status ? `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})}` : ``} ${validate_component(Textbox, "TextBox").$$render(
            $$result,
            {
              label,
              info,
              root,
              show_label,
              lines,
              type,
              rtl,
              text_align,
              max_lines: !max_lines ? lines + 1 : max_lines,
              placeholder,
              submit_btn,
              stop_btn,
              show_copy_button,
              autofocus,
              container,
              autoscroll,
              max_length,
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

export { Textbox as BaseTextbox, Index as default };
//# sourceMappingURL=Index15-Dj4Upexy.js.map
