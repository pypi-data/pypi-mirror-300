import { c as create_ssr_component, a as createEventDispatcher, v as validate_component } from './ssr-Cz1f32Mr.js';
import { a as Tabs$1 } from './Tabs-FD1llnQO.js';
export { T as TABS } from './Tabs-FD1llnQO.js';
import './index4-D_FyJKAV.js';

const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  const dispatch = createEventDispatcher();
  let { visible = true } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { selected } = $$props;
  let { gradio } = $$props;
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.selected === void 0 && $$bindings.selected && selected !== void 0)
    $$bindings.selected(selected);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    {
      dispatch("prop_change", { selected });
    }
    $$rendered = `${validate_component(Tabs$1, "Tabs").$$render(
      $$result,
      { visible, elem_id, elem_classes, selected },
      {
        selected: ($$value) => {
          selected = $$value;
          $$settled = false;
        }
      },
      {
        default: () => {
          return `${slots.default ? slots.default({}) : ``}`;
        }
      }
    )}`;
  } while (!$$settled);
  return $$rendered;
});

export { Tabs$1 as BaseTabs, Index as default };
//# sourceMappingURL=Index14-DMlNBrMZ.js.map
