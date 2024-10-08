import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import { F as File, B as BaseFileUpload } from './FileUpload-D7XcGgxi.js';
export { a as FilePreview } from './FileUpload-D7XcGgxi.js';
import { B as Block, S as Static } from './2-B44WpJir.js';
import { U as UploadText } from './UploadText-BJefVQ_A.js';
export { default as BaseExample } from './Example3-Ih0PKwgI.js';
import './File-B4mYSrEc.js';
import './BlockLabel-BHjb1jyn.js';
import './Empty-3_kIXlIW.js';
import './Upload3-HqK6dEl_.js';
import './ModifyUpload-BHGwr096.js';
import './Download-BYY54H3I.js';
import './Undo-CbHQvbEr.js';
import './IconButtonWrapper-B4nOVFkQ.js';
import './DownloadLink-Crj4dtQe.js';
import './file-url-D-K40zdU.js';
import './index4-D_FyJKAV.js';
import 'tty';
import 'path';
import 'url';
import 'fs';
import './Upload2-CQQNjaMs.js';

const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value } = $$props;
  let { interactive } = $$props;
  let { root } = $$props;
  let { label } = $$props;
  let { show_label } = $$props;
  let { height = void 0 } = $$props;
  let { _selectable = false } = $$props;
  let { loading_status } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { gradio } = $$props;
  let { file_count } = $$props;
  let { file_types = ["file"] } = $$props;
  let { input_ready } = $$props;
  let uploading = false;
  let old_value = value;
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.height === void 0 && $$bindings.height && height !== void 0)
    $$bindings.height(height);
  if ($$props._selectable === void 0 && $$bindings._selectable && _selectable !== void 0)
    $$bindings._selectable(_selectable);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.file_count === void 0 && $$bindings.file_count && file_count !== void 0)
    $$bindings.file_count(file_count);
  if ($$props.file_types === void 0 && $$bindings.file_types && file_types !== void 0)
    $$bindings.file_types(file_types);
  if ($$props.input_ready === void 0 && $$bindings.input_ready && input_ready !== void 0)
    $$bindings.input_ready(input_ready);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    input_ready = !uploading;
    {
      if (JSON.stringify(old_value) !== JSON.stringify(value)) {
        gradio.dispatch("change");
        old_value = value;
      }
    }
    $$rendered = `   ${validate_component(Block, "Block").$$render(
      $$result,
      {
        visible,
        variant: value ? "solid" : "dashed",
        border_mode: "base",
        padding: false,
        elem_id,
        elem_classes,
        container,
        scale,
        min_width,
        allow_overflow: false
      },
      {},
      {
        default: () => {
          return `${validate_component(Static, "StatusTracker").$$render(
            $$result,
            Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status, {
              status: loading_status?.status || "complete"
            }),
            {},
            {}
          )} ${!interactive ? `${validate_component(File, "File").$$render(
            $$result,
            {
              selectable: _selectable,
              value,
              label,
              show_label,
              height,
              i18n: gradio.i18n
            },
            {},
            {}
          )}` : `${validate_component(BaseFileUpload, "FileUpload").$$render(
            $$result,
            {
              upload: (...args) => gradio.client.upload(...args),
              stream_handler: (...args) => gradio.client.stream(...args),
              label,
              show_label,
              value,
              file_count,
              file_types,
              selectable: _selectable,
              root,
              height,
              max_file_size: gradio.max_file_size,
              i18n: gradio.i18n,
              uploading
            },
            {
              uploading: ($$value) => {
                uploading = $$value;
                $$settled = false;
              }
            },
            {
              default: () => {
                return `${validate_component(UploadText, "UploadText").$$render($$result, { i18n: gradio.i18n, type: "file" }, {}, {})}`;
              }
            }
          )}`}`;
        }
      }
    )}`;
  } while (!$$settled);
  return $$rendered;
});

export { File as BaseFile, BaseFileUpload, Index as default };
//# sourceMappingURL=Index9-ByE6fl_G.js.map
