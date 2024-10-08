import { c as create_ssr_component, a as createEventDispatcher, v as validate_component } from './ssr-Cz1f32Mr.js';
import { c as IconButton } from './2-B44WpJir.js';
import { C as Community } from './Community-CFKRrddB.js';

const ShareButton = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  createEventDispatcher();
  let { formatter } = $$props;
  let { value } = $$props;
  let { i18n } = $$props;
  let pending = false;
  if ($$props.formatter === void 0 && $$bindings.formatter && formatter !== void 0)
    $$bindings.formatter(formatter);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.i18n === void 0 && $$bindings.i18n && i18n !== void 0)
    $$bindings.i18n(i18n);
  return `${validate_component(IconButton, "IconButton").$$render(
    $$result,
    {
      Icon: Community,
      label: i18n("common.share"),
      pending
    },
    {},
    {}
  )}`;
});

export { ShareButton as S };
//# sourceMappingURL=ShareButton-B6RPHh-X.js.map
