import { c as create_ssr_component, a as createEventDispatcher, v as validate_component } from './ssr-Cz1f32Mr.js';
import { c as IconButton, l as Clear } from './2-B44WpJir.js';
import { D as Download } from './Download-BYY54H3I.js';
import { U as Undo } from './Undo-CbHQvbEr.js';
import { I as IconButtonWrapper } from './IconButtonWrapper-B4nOVFkQ.js';
import { D as DownloadLink } from './DownloadLink-Crj4dtQe.js';

const Edit = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>`;
});
const ModifyUpload = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { editable = false } = $$props;
  let { undoable = false } = $$props;
  let { download = null } = $$props;
  let { i18n } = $$props;
  createEventDispatcher();
  if ($$props.editable === void 0 && $$bindings.editable && editable !== void 0)
    $$bindings.editable(editable);
  if ($$props.undoable === void 0 && $$bindings.undoable && undoable !== void 0)
    $$bindings.undoable(undoable);
  if ($$props.download === void 0 && $$bindings.download && download !== void 0)
    $$bindings.download(download);
  if ($$props.i18n === void 0 && $$bindings.i18n && i18n !== void 0)
    $$bindings.i18n(i18n);
  return `${validate_component(IconButtonWrapper, "IconButtonWrapper").$$render($$result, {}, {}, {
    default: () => {
      return `${editable ? `${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Edit, label: i18n("common.edit") }, {}, {})}` : ``} ${undoable ? `${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Undo, label: i18n("common.undo") }, {}, {})}` : ``} ${download ? `${validate_component(DownloadLink, "DownloadLink").$$render($$result, { href: download, download: true }, {}, {
        default: () => {
          return `${validate_component(IconButton, "IconButton").$$render(
            $$result,
            {
              Icon: Download,
              label: i18n("common.download")
            },
            {},
            {}
          )}`;
        }
      })}` : ``} ${slots.default ? slots.default({}) : ``} ${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Clear, label: i18n("common.clear") }, {}, {})}`;
    }
  })}`;
});

export { ModifyUpload as M };
//# sourceMappingURL=ModifyUpload-BHGwr096.js.map
