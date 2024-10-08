import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import ImagePreview from './ImagePreview-YcW5tcpn.js';
import { I as ImageUploader$1 } from './ImageUploader-CQO8PZgx.js';
export { W as Webcam } from './ImageUploader-CQO8PZgx.js';
import { B as Block, S as Static } from './2-B44WpJir.js';
import { I as Image } from './Image-DvwRtq0Q.js';
import { E as Empty } from './Empty-3_kIXlIW.js';
import { U as UploadText } from './UploadText-BJefVQ_A.js';
export { I as BaseImage } from './Image2-CC52XfmL.js';
export { default as BaseExample } from './Example4-CrKk4R0i.js';
import './Download-BYY54H3I.js';
import './Maximize-D0B3FhSj.js';
import './BlockLabel-BHjb1jyn.js';
import './ShareButton-B6RPHh-X.js';
import './Community-CFKRrddB.js';
import './IconButtonWrapper-B4nOVFkQ.js';
import './DownloadLink-Crj4dtQe.js';
import './file-url-D-K40zdU.js';
import './index4-D_FyJKAV.js';
import 'tty';
import 'path';
import 'url';
import 'fs';
import './SelectSource-ErVhAWbw.js';
import './Upload2-CQQNjaMs.js';
import './StreamingBar-DxPqW8tq.js';
import './Upload3-HqK6dEl_.js';

const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let stream_state = "closed";
  let _modify_stream = () => {
  };
  function modify_stream_state(state) {
    stream_state = state;
    _modify_stream(state);
  }
  const get_stream_state = () => stream_state;
  let { set_time_limit } = $$props;
  let { value_is_output = false } = $$props;
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value = null } = $$props;
  let old_value = null;
  let { label } = $$props;
  let { show_label } = $$props;
  let { show_download_button } = $$props;
  let { root } = $$props;
  let { height } = $$props;
  let { width } = $$props;
  let { stream_every } = $$props;
  let { _selectable = false } = $$props;
  let { container = true } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { loading_status } = $$props;
  let { show_share_button = false } = $$props;
  let { sources = ["upload", "clipboard", "webcam"] } = $$props;
  let { interactive } = $$props;
  let { streaming } = $$props;
  let { pending } = $$props;
  let { mirror_webcam } = $$props;
  let { placeholder = void 0 } = $$props;
  let { show_fullscreen_button } = $$props;
  let { input_ready } = $$props;
  let uploading = false;
  let { gradio } = $$props;
  let dragging;
  let active_source = null;
  let upload_component;
  if ($$props.modify_stream_state === void 0 && $$bindings.modify_stream_state && modify_stream_state !== void 0)
    $$bindings.modify_stream_state(modify_stream_state);
  if ($$props.get_stream_state === void 0 && $$bindings.get_stream_state && get_stream_state !== void 0)
    $$bindings.get_stream_state(get_stream_state);
  if ($$props.set_time_limit === void 0 && $$bindings.set_time_limit && set_time_limit !== void 0)
    $$bindings.set_time_limit(set_time_limit);
  if ($$props.value_is_output === void 0 && $$bindings.value_is_output && value_is_output !== void 0)
    $$bindings.value_is_output(value_is_output);
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.show_download_button === void 0 && $$bindings.show_download_button && show_download_button !== void 0)
    $$bindings.show_download_button(show_download_button);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  if ($$props.height === void 0 && $$bindings.height && height !== void 0)
    $$bindings.height(height);
  if ($$props.width === void 0 && $$bindings.width && width !== void 0)
    $$bindings.width(width);
  if ($$props.stream_every === void 0 && $$bindings.stream_every && stream_every !== void 0)
    $$bindings.stream_every(stream_every);
  if ($$props._selectable === void 0 && $$bindings._selectable && _selectable !== void 0)
    $$bindings._selectable(_selectable);
  if ($$props.container === void 0 && $$bindings.container && container !== void 0)
    $$bindings.container(container);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.show_share_button === void 0 && $$bindings.show_share_button && show_share_button !== void 0)
    $$bindings.show_share_button(show_share_button);
  if ($$props.sources === void 0 && $$bindings.sources && sources !== void 0)
    $$bindings.sources(sources);
  if ($$props.interactive === void 0 && $$bindings.interactive && interactive !== void 0)
    $$bindings.interactive(interactive);
  if ($$props.streaming === void 0 && $$bindings.streaming && streaming !== void 0)
    $$bindings.streaming(streaming);
  if ($$props.pending === void 0 && $$bindings.pending && pending !== void 0)
    $$bindings.pending(pending);
  if ($$props.mirror_webcam === void 0 && $$bindings.mirror_webcam && mirror_webcam !== void 0)
    $$bindings.mirror_webcam(mirror_webcam);
  if ($$props.placeholder === void 0 && $$bindings.placeholder && placeholder !== void 0)
    $$bindings.placeholder(placeholder);
  if ($$props.show_fullscreen_button === void 0 && $$bindings.show_fullscreen_button && show_fullscreen_button !== void 0)
    $$bindings.show_fullscreen_button(show_fullscreen_button);
  if ($$props.input_ready === void 0 && $$bindings.input_ready && input_ready !== void 0)
    $$bindings.input_ready(input_ready);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    input_ready = !uploading;
    {
      {
        if (JSON.stringify(value) !== JSON.stringify(old_value)) {
          old_value = value;
          gradio.dispatch("change");
          if (!value_is_output) {
            gradio.dispatch("input");
          }
        }
      }
    }
    $$rendered = `   ${!interactive ? `${validate_component(Block, "Block").$$render(
      $$result,
      {
        visible,
        variant: "solid",
        border_mode: dragging ? "focus" : "base",
        padding: false,
        elem_id,
        elem_classes,
        height: height || void 0,
        width,
        allow_overflow: false,
        container,
        scale,
        min_width
      },
      {},
      {
        default: () => {
          return `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} ${validate_component(ImagePreview, "StaticImage").$$render(
            $$result,
            {
              value,
              label,
              show_label,
              show_download_button,
              selectable: _selectable,
              show_share_button,
              i18n: gradio.i18n,
              show_fullscreen_button
            },
            {},
            {}
          )}`;
        }
      }
    )}` : `${validate_component(Block, "Block").$$render(
      $$result,
      {
        visible,
        variant: value === null ? "dashed" : "solid",
        border_mode: dragging ? "focus" : "base",
        padding: false,
        elem_id,
        elem_classes,
        height: height || void 0,
        width,
        allow_overflow: false,
        container,
        scale,
        min_width
      },
      {},
      {
        default: () => {
          return `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} ${validate_component(ImageUploader$1, "ImageUploader").$$render(
            $$result,
            {
              selectable: _selectable,
              root,
              sources,
              label,
              show_label,
              pending,
              streaming,
              mirror_webcam,
              stream_every,
              max_file_size: gradio.max_file_size,
              i18n: gradio.i18n,
              upload: (...args) => gradio.client.upload(...args),
              stream_handler: gradio.client?.stream,
              this: upload_component,
              uploading,
              active_source,
              value,
              dragging,
              modify_stream: _modify_stream,
              set_time_limit
            },
            {
              this: ($$value) => {
                upload_component = $$value;
                $$settled = false;
              },
              uploading: ($$value) => {
                uploading = $$value;
                $$settled = false;
              },
              active_source: ($$value) => {
                active_source = $$value;
                $$settled = false;
              },
              value: ($$value) => {
                value = $$value;
                $$settled = false;
              },
              dragging: ($$value) => {
                dragging = $$value;
                $$settled = false;
              },
              modify_stream: ($$value) => {
                _modify_stream = $$value;
                $$settled = false;
              },
              set_time_limit: ($$value) => {
                set_time_limit = $$value;
                $$settled = false;
              }
            },
            {
              default: () => {
                return `${active_source === "upload" || !active_source ? `${validate_component(UploadText, "UploadText").$$render(
                  $$result,
                  {
                    i18n: gradio.i18n,
                    type: "image",
                    placeholder
                  },
                  {},
                  {}
                )}` : `${active_source === "clipboard" ? `${validate_component(UploadText, "UploadText").$$render(
                  $$result,
                  {
                    i18n: gradio.i18n,
                    type: "clipboard",
                    mode: "short"
                  },
                  {},
                  {}
                )}` : `${validate_component(Empty, "Empty").$$render($$result, { unpadded_box: true, size: "large" }, {}, {
                  default: () => {
                    return `${validate_component(Image, "Image").$$render($$result, {}, {}, {})}`;
                  }
                })}`}`}`;
              }
            }
          )}`;
        }
      }
    )}`}`;
  } while (!$$settled);
  return $$rendered;
});

export { ImageUploader$1 as BaseImageUploader, ImagePreview as BaseStaticImage, Index as default };
//# sourceMappingURL=Index11-C2FwuH2N.js.map
