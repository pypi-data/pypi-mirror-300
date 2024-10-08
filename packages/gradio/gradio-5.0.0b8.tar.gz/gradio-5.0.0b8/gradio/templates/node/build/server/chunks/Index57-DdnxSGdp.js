import { c as create_ssr_component, v as validate_component, a as createEventDispatcher, e as escape, n as null_to_empty, b as add_attribute, f as each, d as add_styles, m as missing_component, o as onDestroy } from './ssr-Cz1f32Mr.js';
import { B as Block, S as Static, c as IconButton, M as MarkdownCode, C as Copy } from './2-B44WpJir.js';
import { d as dequal } from './index8-sfNUnwRZ.js';
import { I as Image$1 } from './Image2-CC52XfmL.js';
import { C as Community } from './Community-CFKRrddB.js';
import { T as Trash } from './Trash-DBMUgMKL.js';
import { I as IconButtonWrapper } from './IconButtonWrapper-B4nOVFkQ.js';
import { D as DownloadLink } from './DownloadLink-Crj4dtQe.js';
import { U as Undo } from './Undo-CbHQvbEr.js';
import { B as BlockLabel } from './BlockLabel-BHjb1jyn.js';
import './index4-D_FyJKAV.js';
import 'tty';
import 'path';
import 'url';
import 'fs';
import './file-url-D-K40zdU.js';

const Chat = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--carbon" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path fill="currentColor" d="M17.74 30L16 29l4-7h6a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h9v2H6a4 4 0 0 1-4-4V8a4 4 0 0 1 4-4h20a4 4 0 0 1 4 4v12a4 4 0 0 1-4 4h-4.84Z"></path><path fill="currentColor" d="M8 10h16v2H8zm0 6h10v2H8z"></path></svg>`;
});
const Retry = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentColor"><path d="M19.1679 9C18.0247 6.46819 15.3006 4.5 11.9999 4.5C8.31459 4.5 5.05104 7.44668 4.54932 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M16 9H19.4C19.7314 9 20 8.73137 20 8.4V5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M4.88146 15C5.92458 17.5318 8.64874 19.5 12.0494 19.5C15.7347 19.5 18.9983 16.5533 19.5 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M8.04932 15H4.64932C4.31795 15 4.04932 15.2686 4.04932 15.6V19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>`;
});
const redirect_src_url = (src, root) => src.replace('src="/file', `src="${root}file`);
function get_component_for_mime_type(mime_type) {
  if (!mime_type)
    return "file";
  if (mime_type.includes("audio"))
    return "audio";
  if (mime_type.includes("video"))
    return "video";
  if (mime_type.includes("image"))
    return "image";
  return "file";
}
function convert_file_message_to_component_message(message) {
  const _file = Array.isArray(message.file) ? message.file[0] : message.file;
  return {
    component: get_component_for_mime_type(_file?.mime_type),
    value: message.file,
    alt_text: message.alt_text,
    constructor_args: {},
    props: {}
  };
}
function normalise_messages(messages, root) {
  if (messages === null)
    return messages;
  return messages.map((message, i) => {
    if (typeof message.content === "string") {
      return {
        role: message.role,
        metadata: message.metadata,
        content: redirect_src_url(message.content, root),
        type: "text",
        index: i
      };
    } else if ("file" in message.content) {
      return {
        content: convert_file_message_to_component_message(message.content),
        metadata: message.metadata,
        role: message.role,
        type: "component",
        index: i
      };
    }
    return { type: "component", ...message };
  });
}
function normalise_tuples(messages, root) {
  if (messages === null)
    return messages;
  const msg = messages.flatMap((message_pair, i) => {
    return message_pair.map((message, index) => {
      if (message == null)
        return null;
      const role = index == 0 ? "user" : "assistant";
      if (typeof message === "string") {
        return {
          role,
          type: "text",
          content: redirect_src_url(message, root),
          metadata: { title: null },
          index: [i, index]
        };
      }
      if ("file" in message) {
        return {
          content: convert_file_message_to_component_message(message),
          role,
          type: "component",
          index: [i, index]
        };
      }
      return {
        role,
        content: message,
        type: "component",
        index: [i, index]
      };
    });
  });
  return msg.filter((message) => message != null);
}
function is_component_message(message) {
  return message.type === "component";
}
const css$4 = {
  code: ".pending.svelte-1gpwetz{background:var(--color-accent-soft);display:flex;flex-direction:row;justify-content:center;align-items:center;align-self:center;gap:2px;width:100%;height:var(--size-16)}.dot-flashing.svelte-1gpwetz{animation:svelte-1gpwetz-flash 1s infinite ease-in-out;border-radius:5px;background-color:var(--body-text-color);width:7px;height:7px;color:var(--body-text-color)}@keyframes svelte-1gpwetz-flash{0%,100%{opacity:0}50%{opacity:1}}.dot-flashing.svelte-1gpwetz:nth-child(1){animation-delay:0s}.dot-flashing.svelte-1gpwetz:nth-child(2){animation-delay:0.33s}.dot-flashing.svelte-1gpwetz:nth-child(3){animation-delay:0.66s}",
  map: '{"version":3,"file":"Pending.svelte","sources":["Pending.svelte"],"sourcesContent":["<script lang=\\"ts\\">export let layout = \\"bubble\\";\\n<\/script>\\n\\n<div\\n\\tclass=\\"message pending\\"\\n\\trole=\\"status\\"\\n\\taria-label=\\"Loading response\\"\\n\\taria-live=\\"polite\\"\\n\\tstyle:border-radius={layout === \\"bubble\\" ? \\"var(--radius-xxl)\\" : \\"none\\"}\\n>\\n\\t<span class=\\"sr-only\\">Loading content</span>\\n\\t<div class=\\"dot-flashing\\" />\\n\\t&nbsp;\\n\\t<div class=\\"dot-flashing\\" />\\n\\t&nbsp;\\n\\t<div class=\\"dot-flashing\\" />\\n</div>\\n\\n<style>\\n\\t.pending {\\n\\t\\tbackground: var(--color-accent-soft);\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: row;\\n\\t\\tjustify-content: center;\\n\\t\\talign-items: center;\\n\\t\\talign-self: center;\\n\\t\\tgap: 2px;\\n\\t\\twidth: 100%;\\n\\t\\theight: var(--size-16);\\n\\t}\\n\\t.dot-flashing {\\n\\t\\tanimation: flash 1s infinite ease-in-out;\\n\\t\\tborder-radius: 5px;\\n\\t\\tbackground-color: var(--body-text-color);\\n\\t\\twidth: 7px;\\n\\t\\theight: 7px;\\n\\t\\tcolor: var(--body-text-color);\\n\\t}\\n\\t@keyframes flash {\\n\\t\\t0%,\\n\\t\\t100% {\\n\\t\\t\\topacity: 0;\\n\\t\\t}\\n\\t\\t50% {\\n\\t\\t\\topacity: 1;\\n\\t\\t}\\n\\t}\\n\\n\\t.dot-flashing:nth-child(1) {\\n\\t\\tanimation-delay: 0s;\\n\\t}\\n\\n\\t.dot-flashing:nth-child(2) {\\n\\t\\tanimation-delay: 0.33s;\\n\\t}\\n\\t.dot-flashing:nth-child(3) {\\n\\t\\tanimation-delay: 0.66s;\\n\\t}</style>\\n"],"names":[],"mappings":"AAmBC,uBAAS,CACR,UAAU,CAAE,IAAI,mBAAmB,CAAC,CACpC,OAAO,CAAE,IAAI,CACb,cAAc,CAAE,GAAG,CACnB,eAAe,CAAE,MAAM,CACvB,WAAW,CAAE,MAAM,CACnB,UAAU,CAAE,MAAM,CAClB,GAAG,CAAE,GAAG,CACR,KAAK,CAAE,IAAI,CACX,MAAM,CAAE,IAAI,SAAS,CACtB,CACA,4BAAc,CACb,SAAS,CAAE,oBAAK,CAAC,EAAE,CAAC,QAAQ,CAAC,WAAW,CACxC,aAAa,CAAE,GAAG,CAClB,gBAAgB,CAAE,IAAI,iBAAiB,CAAC,CACxC,KAAK,CAAE,GAAG,CACV,MAAM,CAAE,GAAG,CACX,KAAK,CAAE,IAAI,iBAAiB,CAC7B,CACA,WAAW,oBAAM,CAChB,EAAE,CACF,IAAK,CACJ,OAAO,CAAE,CACV,CACA,GAAI,CACH,OAAO,CAAE,CACV,CACD,CAEA,4BAAa,WAAW,CAAC,CAAE,CAC1B,eAAe,CAAE,EAClB,CAEA,4BAAa,WAAW,CAAC,CAAE,CAC1B,eAAe,CAAE,KAClB,CACA,4BAAa,WAAW,CAAC,CAAE,CAC1B,eAAe,CAAE,KAClB"}'
};
const Pending = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { layout = "bubble" } = $$props;
  if ($$props.layout === void 0 && $$bindings.layout && layout !== void 0)
    $$bindings.layout(layout);
  $$result.css.add(css$4);
  return `<div class="message pending svelte-1gpwetz" role="status" aria-label="Loading response" aria-live="polite"${add_styles({
    "border-radius": layout === "bubble" ? "var(--radius-xxl)" : "none"
  })} data-svelte-h="svelte-exuub1"><span class="sr-only">Loading content</span> <div class="dot-flashing svelte-1gpwetz"></div>
	 
	<div class="dot-flashing svelte-1gpwetz"></div>
	 
	<div class="dot-flashing svelte-1gpwetz"></div> </div>`;
});
const css$3 = {
  code: ".box.svelte-1e60bn1{border-radius:4px;cursor:pointer;max-width:max-content;background:var(--color-accent-soft);border:1px solid var(--border-color-accent-subdued);font-size:0.8em}.title.svelte-1e60bn1{display:flex;align-items:center;padding:3px 6px;color:var(--body-text-color);opacity:0.8}.content.svelte-1e60bn1{padding:4px 8px}.content.svelte-1e60bn1 *{font-size:0.8em}.title-text.svelte-1e60bn1{padding-right:var(--spacing-lg)}.arrow.svelte-1e60bn1{margin-left:auto;opacity:0.8}",
  map: '{"version":3,"file":"MessageBox.svelte","sources":["MessageBox.svelte"],"sourcesContent":["<script lang=\\"ts\\">export let expanded = false;\\nexport let title;\\nfunction toggleExpanded() {\\n    expanded = !expanded;\\n}\\n<\/script>\\n\\n<button class=\\"box\\" on:click={toggleExpanded}>\\n\\t<div class=\\"title\\">\\n\\t\\t<span class=\\"title-text\\">{title}</span>\\n\\t\\t<span\\n\\t\\t\\tstyle:transform={expanded ? \\"rotate(0)\\" : \\"rotate(90deg)\\"}\\n\\t\\t\\tclass=\\"arrow\\"\\n\\t\\t>\\n\\t\\t\\t▼\\n\\t\\t</span>\\n\\t</div>\\n\\t{#if expanded}\\n\\t\\t<div class=\\"content\\">\\n\\t\\t\\t<slot></slot>\\n\\t\\t</div>\\n\\t{/if}\\n</button>\\n\\n<style>\\n\\t.box {\\n\\t\\tborder-radius: 4px;\\n\\t\\tcursor: pointer;\\n\\t\\tmax-width: max-content;\\n\\t\\tbackground: var(--color-accent-soft);\\n\\t\\tborder: 1px solid var(--border-color-accent-subdued);\\n\\t\\tfont-size: 0.8em;\\n\\t}\\n\\n\\t.title {\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tpadding: 3px 6px;\\n\\t\\tcolor: var(--body-text-color);\\n\\t\\topacity: 0.8;\\n\\t}\\n\\n\\t.content {\\n\\t\\tpadding: 4px 8px;\\n\\t}\\n\\n\\t.content :global(*) {\\n\\t\\tfont-size: 0.8em;\\n\\t}\\n\\n\\t.title-text {\\n\\t\\tpadding-right: var(--spacing-lg);\\n\\t}\\n\\n\\t.arrow {\\n\\t\\tmargin-left: auto;\\n\\t\\topacity: 0.8;\\n\\t}</style>\\n"],"names":[],"mappings":"AAyBC,mBAAK,CACJ,aAAa,CAAE,GAAG,CAClB,MAAM,CAAE,OAAO,CACf,SAAS,CAAE,WAAW,CACtB,UAAU,CAAE,IAAI,mBAAmB,CAAC,CACpC,MAAM,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,6BAA6B,CAAC,CACpD,SAAS,CAAE,KACZ,CAEA,qBAAO,CACN,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,OAAO,CAAE,GAAG,CAAC,GAAG,CAChB,KAAK,CAAE,IAAI,iBAAiB,CAAC,CAC7B,OAAO,CAAE,GACV,CAEA,uBAAS,CACR,OAAO,CAAE,GAAG,CAAC,GACd,CAEA,uBAAQ,CAAS,CAAG,CACnB,SAAS,CAAE,KACZ,CAEA,0BAAY,CACX,aAAa,CAAE,IAAI,YAAY,CAChC,CAEA,qBAAO,CACN,WAAW,CAAE,IAAI,CACjB,OAAO,CAAE,GACV"}'
};
const MessageBox = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { expanded = false } = $$props;
  let { title } = $$props;
  if ($$props.expanded === void 0 && $$bindings.expanded && expanded !== void 0)
    $$bindings.expanded(expanded);
  if ($$props.title === void 0 && $$bindings.title && title !== void 0)
    $$bindings.title(title);
  $$result.css.add(css$3);
  return `<button class="box svelte-1e60bn1"><div class="title svelte-1e60bn1"><span class="title-text svelte-1e60bn1">${escape(title)}</span> <span class="arrow svelte-1e60bn1"${add_styles({
    "transform": expanded ? "rotate(0)" : "rotate(90deg)"
  })} data-svelte-h="svelte-15ydlzc">▼</span></div> ${expanded ? `<div class="content svelte-1e60bn1">${slots.default ? slots.default({}) : ``}</div>` : ``} </button>`;
});
const Component = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { type } = $$props;
  let { components } = $$props;
  let { value } = $$props;
  let { target } = $$props;
  let { theme_mode } = $$props;
  let { props } = $$props;
  let { i18n } = $$props;
  let { upload } = $$props;
  let { _fetch } = $$props;
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.components === void 0 && $$bindings.components && components !== void 0)
    $$bindings.components(components);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.target === void 0 && $$bindings.target && target !== void 0)
    $$bindings.target(target);
  if ($$props.theme_mode === void 0 && $$bindings.theme_mode && theme_mode !== void 0)
    $$bindings.theme_mode(theme_mode);
  if ($$props.props === void 0 && $$bindings.props && props !== void 0)
    $$bindings.props(props);
  if ($$props.i18n === void 0 && $$bindings.i18n && i18n !== void 0)
    $$bindings.i18n(i18n);
  if ($$props.upload === void 0 && $$bindings.upload && upload !== void 0)
    $$bindings.upload(upload);
  if ($$props._fetch === void 0 && $$bindings._fetch && _fetch !== void 0)
    $$bindings._fetch(_fetch);
  return `${type === "gallery" ? `${validate_component(components[type] || missing_component, "svelte:component").$$render(
    $$result,
    {
      value,
      show_label: false,
      i18n,
      label: "",
      _fetch,
      allow_preview: false,
      interactive: false,
      mode: "minimal",
      fixed_height: 1
    },
    {},
    {}
  )}` : `${type === "plot" ? `${validate_component(components[type] || missing_component, "svelte:component").$$render(
    $$result,
    {
      value,
      target,
      theme_mode,
      bokeh_version: props.bokeh_version,
      caption: "",
      show_actions_button: true
    },
    {},
    {}
  )}` : `${type === "audio" ? `${validate_component(components[type] || missing_component, "svelte:component").$$render(
    $$result,
    {
      value,
      show_label: false,
      show_share_button: true,
      i18n,
      label: "",
      waveform_settings: {},
      waveform_options: {},
      show_download_button: false
    },
    {},
    {}
  )}` : `${type === "video" ? `${validate_component(components[type] || missing_component, "svelte:component").$$render(
    $$result,
    {
      autoplay: true,
      value: value.video || value,
      show_label: false,
      show_share_button: true,
      i18n,
      upload,
      show_download_button: false
    },
    {},
    {
      default: () => {
        return `<track kind="captions">`;
      }
    }
  )}` : `${type === "image" ? `${validate_component(components[type] || missing_component, "svelte:component").$$render(
    $$result,
    {
      value,
      show_label: false,
      label: "chatbot-image",
      show_download_button: false,
      i18n
    },
    {},
    {}
  )}` : `${type === "html" ? `${validate_component(components[type] || missing_component, "svelte:component").$$render(
    $$result,
    {
      value,
      show_label: false,
      label: "chatbot-image",
      show_share_button: true,
      i18n,
      gradio: {
        dispatch: () => {
        }
      }
    },
    {},
    {}
  )}` : ``}`}`}`}`}`}`;
});
const ThumbDownDefault = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg width="100%" height="100%" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.25 8.11523H4.5V10.3652C4.5003 10.6635 4.61892 10.9495 4.82983 11.1604C5.04075 11.3713 5.32672 11.4899 5.625 11.4902H6.42488C6.60519 11.4895 6.77926 11.4241 6.91549 11.3059C7.05172 11.1878 7.14109 11.0248 7.16737 10.8464L7.48425 8.62748L8.82562 6.61523H11.25V1.36523H3.375C2.67911 1.36623 2.01201 1.64311 1.51994 2.13517C1.02787 2.62724 0.750992 3.29435 0.75 3.99023V6.61523C0.750496 7.01291 0.908691 7.39415 1.18989 7.67535C1.47109 7.95654 1.85233 8.11474 2.25 8.11523ZM9 2.11523H10.5V5.86523H9V2.11523ZM1.5 3.99023C1.5006 3.49314 1.69833 3.01657 2.04983 2.66507C2.40133 2.31356 2.8779 2.11583 3.375 2.11523H8.25V6.12661L6.76575 8.35298L6.4245 10.7402H5.625C5.52554 10.7402 5.43016 10.7007 5.35983 10.6304C5.28951 10.5601 5.25 10.4647 5.25 10.3652V7.36523H2.25C2.05118 7.36494 1.86059 7.28582 1.72 7.14524C1.57941 7.00465 1.5003 6.81406 1.5 6.61523V3.99023Z" fill="currentColor"></path></svg>`;
});
const ThumbUpDefault = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg width="100%" height="100%" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.75 4.74023H7.5V2.49023C7.4997 2.19196 7.38108 1.90598 7.17017 1.69507C6.95925 1.48415 6.67328 1.36553 6.375 1.36523H5.57512C5.39481 1.366 5.22074 1.43138 5.08451 1.54952C4.94828 1.66766 4.85891 1.83072 4.83262 2.00911L4.51575 4.22798L3.17438 6.24023H0.75V11.4902H8.625C9.32089 11.4892 9.98799 11.2124 10.4801 10.7203C10.9721 10.2282 11.249 9.56112 11.25 8.86523V6.24023C11.2495 5.84256 11.0913 5.46132 10.8101 5.18012C10.5289 4.89893 10.1477 4.74073 9.75 4.74023ZM3 10.7402H1.5V6.99023H3V10.7402ZM10.5 8.86523C10.4994 9.36233 10.3017 9.8389 9.95017 10.1904C9.59867 10.5419 9.1221 10.7396 8.625 10.7402H3.75V6.72886L5.23425 4.50248L5.5755 2.11523H6.375C6.47446 2.11523 6.56984 2.15474 6.64017 2.22507C6.71049 2.2954 6.75 2.39078 6.75 2.49023V5.49023H9.75C9.94882 5.49053 10.1394 5.56965 10.28 5.71023C10.4206 5.85082 10.4997 6.04141 10.5 6.24023V8.86523Z" fill="currentColor"></path></svg>`;
});
const LikeDislike = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { handle_action } = $$props;
  if ($$props.handle_action === void 0 && $$bindings.handle_action && handle_action !== void 0)
    $$bindings.handle_action(handle_action);
  return `${validate_component(IconButton, "IconButton").$$render(
    $$result,
    {
      Icon: ThumbDownDefault,
      label: "dislike",
      color: "var(--block-label-text-color)"
    },
    {},
    {}
  )} ${validate_component(IconButton, "IconButton").$$render(
    $$result,
    {
      Icon: ThumbUpDefault,
      label: "like",
      color: "var(--block-label-text-color)"
    },
    {},
    {}
  )}`;
});
const Copy_1 = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  onDestroy(() => {
  });
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  return `${validate_component(IconButton, "IconButton").$$render(
    $$result,
    {
      label: "Copy message",
      Icon: Copy
    },
    {},
    {}
  )}`;
});
const Download = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg width="16" height="16" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.27701 8.253C6.24187 8.29143 6.19912 8.32212 6.15147 8.34311C6.10383 8.36411 6.05233 8.37495 6.00026 8.37495C5.94819 8.37495 5.89669 8.36411 5.84905 8.34311C5.8014 8.32212 5.75865 8.29143 5.72351 8.253L3.72351 6.0655C3.65798 5.99185 3.62408 5.89536 3.62916 5.79691C3.63424 5.69846 3.67788 5.60596 3.75064 5.53945C3.8234 5.47293 3.91943 5.43774 4.01794 5.44149C4.11645 5.44525 4.20952 5.48764 4.27701 5.5595L5.62501 7.0345V1.5C5.62501 1.40054 5.66452 1.30516 5.73485 1.23483C5.80517 1.16451 5.90055 1.125 6.00001 1.125C6.09947 1.125 6.19485 1.16451 6.26517 1.23483C6.3355 1.30516 6.37501 1.40054 6.37501 1.5V7.034L7.72351 5.559C7.79068 5.4856 7.88425 5.44189 7.98364 5.43748C8.08304 5.43308 8.18011 5.46833 8.25351 5.5355C8.32691 5.60267 8.37062 5.69624 8.37503 5.79563C8.37943 5.89503 8.34418 5.9921 8.27701 6.0655L6.27701 8.253Z" fill="currentColor"></path><path d="M1.875 7.39258C1.875 7.29312 1.83549 7.19774 1.76517 7.12741C1.69484 7.05709 1.59946 7.01758 1.5 7.01758C1.40054 7.01758 1.30516 7.05709 1.23483 7.12741C1.16451 7.19774 1.125 7.29312 1.125 7.39258V7.42008C1.125 8.10358 1.125 8.65508 1.1835 9.08858C1.2435 9.53858 1.3735 9.91758 1.674 10.2186C1.975 10.5196 2.354 10.6486 2.804 10.7096C3.2375 10.7676 3.789 10.7676 4.4725 10.7676H7.5275C8.211 10.7676 8.7625 10.7676 9.196 10.7096C9.646 10.6486 10.025 10.5196 10.326 10.2186C10.627 9.91758 10.756 9.53858 10.817 9.08858C10.875 8.65508 10.875 8.10358 10.875 7.42008V7.39258C10.875 7.29312 10.8355 7.19774 10.7652 7.12741C10.6948 7.05709 10.5995 7.01758 10.5 7.01758C10.4005 7.01758 10.3052 7.05709 10.2348 7.12741C10.1645 7.19774 10.125 7.29312 10.125 7.39258C10.125 8.11008 10.124 8.61058 10.0735 8.98858C10.024 9.35558 9.9335 9.54958 9.7955 9.68808C9.657 9.82658 9.463 9.91658 9.0955 9.96608C8.718 10.0166 8.2175 10.0176 7.5 10.0176H4.5C3.7825 10.0176 3.2815 10.0166 2.904 9.96608C2.537 9.91658 2.343 9.82608 2.2045 9.68808C2.066 9.54958 1.976 9.35558 1.9265 8.98808C1.876 8.61058 1.875 8.11008 1.875 7.39258Z" fill="currentColor"></path></svg>`;
});
const css$2 = {
  code: ".icon-button-wrapper{margin:0px calc(var(--spacing-xl) * 2)}.message-buttons-left.svelte-12mfpe8{align-self:flex-start}.message-buttons-right.svelte-12mfpe8{align-self:flex-end}.message-buttons-right.svelte-12mfpe8 .icon-button-wrapper{margin-left:auto}.with-avatar.svelte-12mfpe8{margin-left:calc(var(--spacing-xl) * 4 + 31px)}",
  map: `{"version":3,"file":"ButtonPanel.svelte","sources":["ButtonPanel.svelte"],"sourcesContent":["<script lang=\\"ts\\">import LikeDislike from \\"./LikeDislike.svelte\\";\\nimport Copy from \\"./Copy.svelte\\";\\nimport DownloadIcon from \\"./Download.svelte\\";\\nimport { DownloadLink } from \\"@gradio/wasm/svelte\\";\\nimport { is_component_message } from \\"./utils\\";\\nimport { Retry, Undo } from \\"@gradio/icons\\";\\nimport { IconButtonWrapper, IconButton } from \\"@gradio/atoms\\";\\nexport let likeable;\\nexport let _retryable;\\nexport let _undoable;\\nexport let show_copy_button;\\nexport let show;\\nexport let message;\\nexport let position;\\nexport let avatar;\\nexport let disable;\\nexport let handle_action;\\nexport let layout;\\nfunction is_all_text(message2) {\\n    return Array.isArray(message2) && message2.every((m) => typeof m.content === \\"string\\") || !Array.isArray(message2) && typeof message2.content === \\"string\\";\\n}\\nfunction all_text(message2) {\\n    if (Array.isArray(message2)) {\\n        return message2.map((m) => m.content).join(\\"\\\\n\\");\\n    }\\n    return message2.content;\\n}\\n$: message_text = is_all_text(message) ? all_text(message) : \\"\\";\\n$: show_copy = show_copy_button && message && is_all_text(message);\\n$: show_download = !Array.isArray(message) && is_component_message(message) && message.content.value?.url;\\n<\/script>\\n\\n{#if show}\\n\\t<div\\n\\t\\tclass=\\"message-buttons-{position} {layout} message-buttons {avatar !==\\n\\t\\t\\tnull && 'with-avatar'}\\"\\n\\t>\\n\\t\\t<IconButtonWrapper top_panel={false}>\\n\\t\\t\\t{#if show_copy}\\n\\t\\t\\t\\t<Copy value={message_text} />\\n\\t\\t\\t{/if}\\n\\t\\t\\t{#if show_download && !Array.isArray(message) && is_component_message(message)}\\n\\t\\t\\t\\t<DownloadLink\\n\\t\\t\\t\\t\\thref={message?.content?.value.url}\\n\\t\\t\\t\\t\\tdownload={message.content.value.orig_name || \\"image\\"}\\n\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t<IconButton Icon={DownloadIcon} />\\n\\t\\t\\t\\t</DownloadLink>\\n\\t\\t\\t{/if}\\n\\t\\t\\t{#if _retryable}\\n\\t\\t\\t\\t<IconButton\\n\\t\\t\\t\\t\\tIcon={Retry}\\n\\t\\t\\t\\t\\ton:click={() => handle_action(\\"retry\\")}\\n\\t\\t\\t\\t\\tdisabled={disable}\\n\\t\\t\\t\\t/>\\n\\t\\t\\t{/if}\\n\\t\\t\\t{#if _undoable}\\n\\t\\t\\t\\t<IconButton\\n\\t\\t\\t\\t\\tIcon={Undo}\\n\\t\\t\\t\\t\\ton:click={() => handle_action(\\"undo\\")}\\n\\t\\t\\t\\t\\tdisabled={disable}\\n\\t\\t\\t\\t/>\\n\\t\\t\\t{/if}\\n\\t\\t\\t{#if likeable}\\n\\t\\t\\t\\t<LikeDislike {handle_action} />\\n\\t\\t\\t{/if}\\n\\t\\t</IconButtonWrapper>\\n\\t</div>\\n{/if}\\n\\n<style>\\n\\t:global(.icon-button-wrapper) {\\n\\t\\tmargin: 0px calc(var(--spacing-xl) * 2);\\n\\t}\\n\\n\\t.message-buttons-left {\\n\\t\\talign-self: flex-start;\\n\\t}\\n\\n\\t.message-buttons-right {\\n\\t\\talign-self: flex-end;\\n\\t}\\n\\n\\t.message-buttons-right :global(.icon-button-wrapper) {\\n\\t\\tmargin-left: auto;\\n\\t}\\n\\n\\t.with-avatar {\\n\\t\\tmargin-left: calc(var(--spacing-xl) * 4 + 31px);\\n\\t}</style>\\n"],"names":[],"mappings":"AAuES,oBAAsB,CAC7B,MAAM,CAAE,GAAG,CAAC,KAAK,IAAI,YAAY,CAAC,CAAC,CAAC,CAAC,CAAC,CACvC,CAEA,oCAAsB,CACrB,UAAU,CAAE,UACb,CAEA,qCAAuB,CACtB,UAAU,CAAE,QACb,CAEA,qCAAsB,CAAS,oBAAsB,CACpD,WAAW,CAAE,IACd,CAEA,2BAAa,CACZ,WAAW,CAAE,KAAK,IAAI,YAAY,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,IAAI,CAC/C"}`
};
function is_all_text(message2) {
  return Array.isArray(message2) && message2.every((m) => typeof m.content === "string") || !Array.isArray(message2) && typeof message2.content === "string";
}
function all_text(message2) {
  if (Array.isArray(message2)) {
    return message2.map((m) => m.content).join("\n");
  }
  return message2.content;
}
const ButtonPanel = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let message_text;
  let show_copy;
  let show_download;
  let { likeable } = $$props;
  let { _retryable } = $$props;
  let { _undoable } = $$props;
  let { show_copy_button } = $$props;
  let { show } = $$props;
  let { message } = $$props;
  let { position } = $$props;
  let { avatar } = $$props;
  let { disable } = $$props;
  let { handle_action } = $$props;
  let { layout } = $$props;
  if ($$props.likeable === void 0 && $$bindings.likeable && likeable !== void 0)
    $$bindings.likeable(likeable);
  if ($$props._retryable === void 0 && $$bindings._retryable && _retryable !== void 0)
    $$bindings._retryable(_retryable);
  if ($$props._undoable === void 0 && $$bindings._undoable && _undoable !== void 0)
    $$bindings._undoable(_undoable);
  if ($$props.show_copy_button === void 0 && $$bindings.show_copy_button && show_copy_button !== void 0)
    $$bindings.show_copy_button(show_copy_button);
  if ($$props.show === void 0 && $$bindings.show && show !== void 0)
    $$bindings.show(show);
  if ($$props.message === void 0 && $$bindings.message && message !== void 0)
    $$bindings.message(message);
  if ($$props.position === void 0 && $$bindings.position && position !== void 0)
    $$bindings.position(position);
  if ($$props.avatar === void 0 && $$bindings.avatar && avatar !== void 0)
    $$bindings.avatar(avatar);
  if ($$props.disable === void 0 && $$bindings.disable && disable !== void 0)
    $$bindings.disable(disable);
  if ($$props.handle_action === void 0 && $$bindings.handle_action && handle_action !== void 0)
    $$bindings.handle_action(handle_action);
  if ($$props.layout === void 0 && $$bindings.layout && layout !== void 0)
    $$bindings.layout(layout);
  $$result.css.add(css$2);
  message_text = is_all_text(message) ? all_text(message) : "";
  show_copy = show_copy_button && message && is_all_text(message);
  show_download = !Array.isArray(message) && is_component_message(message) && message.content.value?.url;
  return `${show ? `<div class="${"message-buttons-" + escape(position, true) + " " + escape(layout, true) + " message-buttons " + escape(avatar !== null && "with-avatar", true) + " svelte-12mfpe8"}">${validate_component(IconButtonWrapper, "IconButtonWrapper").$$render($$result, { top_panel: false }, {}, {
    default: () => {
      return `${show_copy ? `${validate_component(Copy_1, "Copy").$$render($$result, { value: message_text }, {}, {})}` : ``} ${show_download && !Array.isArray(message) && is_component_message(message) ? `${validate_component(DownloadLink, "DownloadLink").$$render(
        $$result,
        {
          href: message?.content?.value.url,
          download: message.content.value.orig_name || "image"
        },
        {},
        {
          default: () => {
            return `${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Download }, {}, {})}`;
          }
        }
      )}` : ``} ${_retryable ? `${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Retry, disabled: disable }, {}, {})}` : ``} ${_undoable ? `${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Undo, disabled: disable }, {}, {})}` : ``} ${likeable ? `${validate_component(LikeDislike, "LikeDislike").$$render($$result, { handle_action }, {}, {})}` : ``}`;
    }
  })}</div>` : ``}`;
});
const CopyAll = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  onDestroy(() => {
  });
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  return `${validate_component(IconButton, "IconButton").$$render(
    $$result,
    {
      Icon: Copy,
      label: "Copy conversation"
    },
    {},
    {}
  )}`;
});
const css$1 = {
  code: '.hidden.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:none}.placeholder-content.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:flex;flex-direction:column;height:100%}.placeholder.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-items:center;display:flex;justify-content:center;height:100%;flex-grow:1}.examples.svelte-18fn4d img{pointer-events:none}.examples.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin:auto;padding:var(--spacing-xxl);display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:var(--spacing-xxl);max-width:calc(min(4 * 200px + 5 * var(--spacing-xxl), 100%))}.example.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:flex;flex-direction:column;align-items:center;padding:var(--spacing-xl);border:0.05px solid var(--border-color-primary);border-radius:var(--radius-xl);background-color:var(--background-fill-secondary);cursor:pointer;transition:var(--button-transition);max-width:var(--size-56);width:100%}.example.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d:hover{background-color:var(--color-accent-soft);border-color:var(--border-color-accent)}.example-icon-container.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:flex;align-self:flex-start;margin-left:var(--spacing-md);width:var(--size-6);height:var(--size-6)}.example-display-text.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d,.example-text.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d,.example-file.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{font-size:var(--text-md);width:100%;text-align:center;overflow:hidden;text-overflow:ellipsis}.example-display-text.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d,.example-file.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin-top:var(--spacing-md)}.example-image-container.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{flex-grow:1;display:flex;justify-content:center;align-items:center;margin-top:var(--spacing-xl)}.example-image-container.svelte-18fn4d img{max-height:100%;max-width:100%;height:var(--size-32);width:100%;object-fit:cover;border-radius:var(--radius-xl)}.panel-wrap.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:100%;overflow-y:auto}.flex-wrap.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:100%;height:100%}.bubble-wrap.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:100%;overflow-y:auto;height:100%;padding-top:var(--spacing-xxl)}.dark .bubble-wrap.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{background:var(--background-fill-secondary)}.message-wrap.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:flex;flex-direction:column;justify-content:space-between;margin-bottom:var(--spacing-xxl)}.bubble-gap.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{gap:calc(var(--spacing-xxl) + var(--spacing-lg))}.message-wrap.svelte-18fn4d>div.svelte-18fn4d p:not(:first-child){margin-top:var(--spacing-xxl)}.message.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{position:relative;display:flex;flex-direction:column;width:calc(100% - var(--spacing-xxl));max-width:100%;color:var(--body-text-color);font-size:var(--chatbot-text-size);overflow-wrap:break-word}.thought.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin-top:var(--spacing-xxl)}.message.svelte-18fn4d .prose{font-size:var(--chatbot-text-size)}.message-bubble-border.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{border-width:1px;border-radius:var(--radius-md)}.user.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-end}.message-fit.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:fit-content !important}.panel-full-width.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:100%}.message-markdown-disabled.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{white-space:pre-line}.flex-wrap.user.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{border-width:1px;border-radius:var(--radius-md);align-self:flex-start;border-bottom-right-radius:0;box-shadow:var(--shadow-drop);align-self:flex-start;text-align:right;padding:var(--spacing-sm) var(--spacing-xl);border-color:var(--border-color-accent-subdued);background-color:var(--color-accent-soft)}:not(.component-wrap).flex-wrap.bot.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{border-width:1px;border-radius:var(--radius-lg);align-self:flex-start;border-bottom-left-radius:0;box-shadow:var(--shadow-drop);align-self:flex-start;text-align:right;padding:var(--spacing-sm) var(--spacing-xl);border-color:var(--border-color-primary);background-color:var(--background-fill-secondary)}.panel.svelte-18fn4d .user.svelte-18fn4d *{text-align:right}.bubble.svelte-18fn4d .bot.svelte-18fn4d.svelte-18fn4d{border-color:var(--border-color-primary)}.message-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:flex;position:relative}.message-row.user-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-end}.message-row.bubble.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin:calc(var(--spacing-xl) * 2);margin-bottom:var(--spacing-xl)}.with_avatar.message-row.panel.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{padding-left:calc(var(--spacing-xl) * 2) !important;padding-right:calc(var(--spacing-xl) * 2) !important}.with_avatar.message-row.bubble.user-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin-right:calc(var(--spacing-xl) * 2) !important}.with_avatar.message-row.bubble.bot-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin-left:calc(var(--spacing-xl) * 2) !important}.with_opposite_avatar.message-row.bubble.user-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin-left:calc(var(--spacing-xxl) + 35px + var(--spacing-xxl))}.message-row.panel.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{margin:0;padding:calc(var(--spacing-xl) * 3) calc(var(--spacing-xxl) * 2)}.message-row.panel.bot-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{background:var(--background-fill-secondary)}.message-row.bubble.user-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-end;max-width:calc(100% - var(--spacing-xl) * 6)}.message-row.bubble.bot-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-start;max-width:calc(100% - var(--spacing-xl) * 6)}.message-row.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d:last-of-type{margin-bottom:calc(var(--spacing-xxl) * 2)}.user-row.bubble.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{flex-direction:row;justify-content:flex-end}@media(max-width: 480px){.user-row.bubble.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-end}.bot-row.bubble.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-start}.message.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:100%}}.avatar-container.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{align-self:flex-start;position:relative;display:flex;justify-content:flex-start;align-items:flex-start;width:35px;height:35px;flex-shrink:0;bottom:0;border-radius:50%;border:1px solid var(--border-color-primary)}.user-row.svelte-18fn4d>.avatar-container.svelte-18fn4d.svelte-18fn4d{order:2;margin-left:var(--spacing-xxl)}.bot-row.svelte-18fn4d>.avatar-container.svelte-18fn4d.svelte-18fn4d{margin-right:var(--spacing-xxl);margin-left:0;margin-top:-5px}.avatar-container.svelte-18fn4d:not(.thumbnail-item) img{width:100%;height:100%;object-fit:cover;border-radius:50%;padding:6px}.selectable.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{cursor:pointer}@keyframes svelte-18fn4d-dot-flashing{0%{opacity:0.8}50%{opacity:0.5}100%{opacity:0.8}}.message-wrap.svelte-18fn4d>.message .svelte-18fn4d:not(.image-button) img{margin:var(--size-2);max-height:200px}.message-wrap.svelte-18fn4d>div.svelte-18fn4d :not(.avatar-container) div .svelte-18fn4d:not(.image-button) img{border-radius:var(--radius-xl);margin:var(--size-2);width:400px;max-width:30vw;max-height:30vw}.message-wrap.svelte-18fn4d .message.svelte-18fn4d a{color:var(--color-text-link);text-decoration:underline}.message-wrap.svelte-18fn4d .bot.svelte-18fn4d table,.message-wrap.svelte-18fn4d .bot.svelte-18fn4d tr,.message-wrap.svelte-18fn4d .bot.svelte-18fn4d td,.message-wrap.svelte-18fn4d .bot.svelte-18fn4d th{border:1px solid var(--border-color-primary)}.message-wrap.svelte-18fn4d .user.svelte-18fn4d table,.message-wrap.svelte-18fn4d .user.svelte-18fn4d tr,.message-wrap.svelte-18fn4d .user.svelte-18fn4d td,.message-wrap.svelte-18fn4d .user.svelte-18fn4d th{border:1px solid var(--border-color-accent)}.message-wrap.svelte-18fn4d span.katex{font-size:var(--text-lg);direction:ltr}.message-wrap.svelte-18fn4d div[class*="code_wrap"] > button{position:absolute;top:var(--spacing-md);right:var(--spacing-md);z-index:1;cursor:pointer;border-bottom-left-radius:var(--radius-sm);padding:var(--spacing-md);width:25px;height:25px}.message-wrap.svelte-18fn4d code > button > span{position:absolute;top:var(--spacing-md);right:var(--spacing-md);width:12px;height:12px}.message-wrap.svelte-18fn4d .check{position:absolute;top:0;right:0;opacity:0;z-index:var(--layer-top);transition:opacity 0.2s;background:var(--background-fill-primary);padding:var(--size-1);width:100%;height:100%;color:var(--body-text-color)}.message-wrap.svelte-18fn4d pre{position:relative}.message-wrap.svelte-18fn4d .grid-wrap{max-height:80% !important;max-width:600px;object-fit:contain}.message.svelte-18fn4d .preview{object-fit:contain;width:95%;max-height:93%}.image-preview.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{position:absolute;z-index:999;left:0;top:0;width:100%;height:100%;overflow:auto;background-color:rgba(0, 0, 0, 0.9);display:flex;justify-content:center;align-items:center}.image-preview.svelte-18fn4d svg{stroke:white}.image-preview-close-button.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{position:absolute;top:10px;right:10px;background:none;border:none;font-size:1.5em;cursor:pointer;height:30px;width:30px;padding:3px;background:var(--bg-color);box-shadow:var(--shadow-drop);border:1px solid var(--button-secondary-border-color);border-radius:var(--radius-lg)}.component.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{padding:0;border-radius:var(--radius-md);width:fit-content;overflow:hidden}.component.gallery.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{border:none}.file-pil.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{display:block;width:fit-content;padding:var(--spacing-sm) var(--spacing-lg);border-radius:var(--radius-md);background:var(--background-fill-secondary);color:var(--body-text-color);text-decoration:none;margin:0;font-family:var(--font-mono);font-size:var(--text-sm)}.file.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:auto !important;max-width:fit-content !important}@media(max-width: 600px) or (max-width: 480px){.component.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{width:100%}}.message-wrap.svelte-18fn4d .prose.chatbot.md{opacity:0.8;overflow-wrap:break-word}.message.svelte-18fn4d>button.svelte-18fn4d.svelte-18fn4d{width:100%}.html.svelte-18fn4d.svelte-18fn4d.svelte-18fn4d{padding:0;border:none;background:none}',
  map: '{"version":3,"file":"ChatBot.svelte","sources":["ChatBot.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { format_chat_for_sharing, is_component_message } from \\"./utils\\";\\nimport { Gradio, copy } from \\"@gradio/utils\\";\\nimport { dequal } from \\"dequal/lite\\";\\nimport { beforeUpdate, afterUpdate, createEventDispatcher, tick, onMount } from \\"svelte\\";\\nimport { Image } from \\"@gradio/image/shared\\";\\nimport { Clear, Trash, Community } from \\"@gradio/icons\\";\\nimport { IconButtonWrapper, IconButton } from \\"@gradio/atoms\\";\\nimport { MarkdownCode as Markdown } from \\"@gradio/markdown\\";\\nimport Pending from \\"./Pending.svelte\\";\\nimport MessageBox from \\"./MessageBox.svelte\\";\\nimport { ShareError } from \\"@gradio/utils\\";\\nexport let value = [];\\nlet old_value = null;\\nimport Component from \\"./Component.svelte\\";\\nimport LikeButtons from \\"./ButtonPanel.svelte\\";\\nimport CopyAll from \\"./CopyAll.svelte\\";\\nexport let _fetch;\\nexport let load_component;\\nlet _components = {};\\nasync function load_components(component_names) {\\n    let names = [];\\n    let components = [];\\n    component_names.forEach((component_name) => {\\n        if (_components[component_name] || component_name === \\"file\\") {\\n            return;\\n        }\\n        const { name, component } = load_component(component_name, \\"base\\");\\n        names.push(name);\\n        components.push(component);\\n        component_name;\\n    });\\n    const loaded_components = await Promise.all(components);\\n    loaded_components.forEach((component, i) => {\\n        _components[names[i]] = component.default;\\n    });\\n}\\n$: load_components(get_components_from_messages(value));\\nfunction get_components_from_messages(messages) {\\n    if (!messages)\\n        return [];\\n    let components = /* @__PURE__ */ new Set();\\n    messages.forEach((message) => {\\n        if (message.type === \\"component\\") {\\n            components.add(message.content.component);\\n        }\\n    });\\n    return Array.from(components);\\n}\\nexport let latex_delimiters;\\nexport let pending_message = false;\\nexport let generating = false;\\nexport let selectable = false;\\nexport let likeable = false;\\nexport let show_share_button = false;\\nexport let show_copy_all_button = false;\\nexport let rtl = false;\\nexport let show_copy_button = false;\\nexport let avatar_images = [null, null];\\nexport let sanitize_html = true;\\nexport let bubble_full_width = true;\\nexport let render_markdown = true;\\nexport let line_breaks = true;\\nexport let theme_mode;\\nexport let i18n;\\nexport let layout = \\"bubble\\";\\nexport let placeholder = null;\\nexport let upload;\\nexport let msg_format = \\"tuples\\";\\nexport let examples = null;\\nexport let _retryable = false;\\nexport let _undoable = false;\\nexport let like_user_message = false;\\nexport let root;\\nlet target = null;\\nonMount(() => {\\n    target = document.querySelector(\\"div.gradio-container\\");\\n});\\nlet div;\\nlet autoscroll;\\nconst dispatch = createEventDispatcher();\\nbeforeUpdate(() => {\\n    autoscroll = div && div.offsetHeight + div.scrollTop > div.scrollHeight - 100;\\n});\\nasync function scroll() {\\n    if (!div)\\n        return;\\n    await tick();\\n    requestAnimationFrame(() => {\\n        if (autoscroll) {\\n            div?.scrollTo(0, div.scrollHeight);\\n        }\\n    });\\n}\\nlet image_preview_source;\\nlet image_preview_source_alt;\\nlet is_image_preview_open = false;\\n$: if (value || autoscroll || _components) {\\n    scroll();\\n}\\nafterUpdate(() => {\\n    if (!div)\\n        return;\\n    div.querySelectorAll(\\"img\\").forEach((n) => {\\n        n.addEventListener(\\"click\\", (e) => {\\n            const target2 = e.target;\\n            if (target2) {\\n                image_preview_source = target2.src;\\n                image_preview_source_alt = target2.alt;\\n                is_image_preview_open = true;\\n            }\\n        });\\n    });\\n});\\n$: {\\n    if (!dequal(value, old_value)) {\\n        old_value = value;\\n        dispatch(\\"change\\");\\n    }\\n}\\n$: groupedMessages = value && group_messages(value);\\nfunction handle_example_select(i, example) {\\n    dispatch(\\"example_select\\", {\\n        index: i,\\n        value: { text: example.text, files: example.files }\\n    });\\n}\\nfunction is_last_bot_message(messages, all_messages) {\\n    const is_bot = messages[messages.length - 1].role === \\"assistant\\";\\n    const last_index = messages[messages.length - 1].index;\\n    const is_last = JSON.stringify(last_index) === JSON.stringify(all_messages[all_messages.length - 1].index);\\n    return is_last && is_bot;\\n}\\nfunction handle_select(i, message) {\\n    dispatch(\\"select\\", {\\n        index: message.index,\\n        value: message.content\\n    });\\n}\\nfunction handle_like(i, message, selected) {\\n    if (selected === \\"undo\\" || selected === \\"retry\\") {\\n        const val_ = value;\\n        let last_index = val_.length - 1;\\n        while (val_[last_index].role === \\"assistant\\") {\\n            last_index--;\\n        }\\n        dispatch(selected, {\\n            index: val_[last_index].index,\\n            value: val_[last_index].content\\n        });\\n        return;\\n    }\\n    if (msg_format === \\"tuples\\") {\\n        dispatch(\\"like\\", {\\n            index: message.index,\\n            value: message.content,\\n            liked: selected === \\"like\\"\\n        });\\n    }\\n    else {\\n        if (!groupedMessages)\\n            return;\\n        const message_group = groupedMessages[i];\\n        const [first, last] = [\\n            message_group[0],\\n            message_group[message_group.length - 1]\\n        ];\\n        dispatch(\\"like\\", {\\n            index: [first.index, last.index],\\n            value: message_group.map((m) => m.content),\\n            liked: selected === \\"like\\"\\n        });\\n    }\\n}\\nfunction get_message_label_data(message) {\\n    if (message.type === \\"text\\") {\\n        return message.content;\\n    }\\n    else if (message.type === \\"component\\" && message.content.component === \\"file\\") {\\n        if (Array.isArray(message.content.value)) {\\n            return `file of extension type: ${message.content.value[0].orig_name?.split(\\".\\").pop()}`;\\n        }\\n        return `file of extension type: ${message.content.value?.orig_name?.split(\\".\\").pop()}` + (message.content.value?.orig_name ?? \\"\\");\\n    }\\n    return `a component of type ${message.content.component ?? \\"unknown\\"}`;\\n}\\nfunction group_messages(messages) {\\n    const groupedMessages2 = [];\\n    let currentGroup = [];\\n    let currentRole = null;\\n    for (const message of messages) {\\n        if (msg_format === \\"tuples\\") {\\n            currentRole = null;\\n        }\\n        if (!(message.role === \\"assistant\\" || message.role === \\"user\\")) {\\n            continue;\\n        }\\n        if (message.role === currentRole) {\\n            currentGroup.push(message);\\n        }\\n        else {\\n            if (currentGroup.length > 0) {\\n                groupedMessages2.push(currentGroup);\\n            }\\n            currentGroup = [message];\\n            currentRole = message.role;\\n        }\\n    }\\n    if (currentGroup.length > 0) {\\n        groupedMessages2.push(currentGroup);\\n    }\\n    return groupedMessages2;\\n}\\n<\/script>\\n\\n{#if value !== null && value.length > 0}\\n\\t<IconButtonWrapper>\\n\\t\\t{#if show_share_button}\\n\\t\\t\\t<IconButton\\n\\t\\t\\t\\tIcon={Community}\\n\\t\\t\\t\\ton:click={async () => {\\n\\t\\t\\t\\t\\ttry {\\n\\t\\t\\t\\t\\t\\t// @ts-ignore\\n\\t\\t\\t\\t\\t\\tconst formatted = await format_chat_for_sharing(value);\\n\\t\\t\\t\\t\\t\\tdispatch(\\"share\\", {\\n\\t\\t\\t\\t\\t\\t\\tdescription: formatted\\n\\t\\t\\t\\t\\t\\t});\\n\\t\\t\\t\\t\\t} catch (e) {\\n\\t\\t\\t\\t\\t\\tconsole.error(e);\\n\\t\\t\\t\\t\\t\\tlet message = e instanceof ShareError ? e.message : \\"Share failed.\\";\\n\\t\\t\\t\\t\\t\\tdispatch(\\"error\\", message);\\n\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t}}\\n\\t\\t\\t>\\n\\t\\t\\t\\t<Community />\\n\\t\\t\\t</IconButton>\\n\\t\\t{/if}\\n\\t\\t<IconButton Icon={Trash} on:click={() => dispatch(\\"clear\\")}></IconButton>\\n\\t\\t{#if show_copy_all_button}\\n\\t\\t\\t<CopyAll {value} />\\n\\t\\t{/if}\\n\\t</IconButtonWrapper>\\n{/if}\\n\\n<div\\n\\tclass={layout === \\"bubble\\" ? \\"bubble-wrap\\" : \\"panel-wrap\\"}\\n\\tbind:this={div}\\n\\trole=\\"log\\"\\n\\taria-label=\\"chatbot conversation\\"\\n\\taria-live=\\"polite\\"\\n>\\n\\t{#if value !== null && value.length > 0 && groupedMessages !== null}\\n\\t\\t<div class=\\"message-wrap\\" use:copy>\\n\\t\\t\\t{#each groupedMessages as messages, i}\\n\\t\\t\\t\\t{@const role = messages[0].role === \\"user\\" ? \\"user\\" : \\"bot\\"}\\n\\t\\t\\t\\t{@const avatar_img = avatar_images[role === \\"user\\" ? 0 : 1]}\\n\\t\\t\\t\\t{@const opposite_avatar_img = avatar_images[role === \\"user\\" ? 0 : 1]}\\n\\t\\t\\t\\t{#if is_image_preview_open}\\n\\t\\t\\t\\t\\t<div class=\\"image-preview\\">\\n\\t\\t\\t\\t\\t\\t<img src={image_preview_source} alt={image_preview_source_alt} />\\n\\t\\t\\t\\t\\t\\t<button\\n\\t\\t\\t\\t\\t\\t\\tclass=\\"image-preview-close-button\\"\\n\\t\\t\\t\\t\\t\\t\\ton:click={() => {\\n\\t\\t\\t\\t\\t\\t\\t\\tis_image_preview_open = false;\\n\\t\\t\\t\\t\\t\\t\\t}}><Clear /></button\\n\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t<div\\n\\t\\t\\t\\t\\tclass=\\"message-row {layout} {role}-row\\"\\n\\t\\t\\t\\t\\tclass:with_avatar={avatar_img !== null}\\n\\t\\t\\t\\t\\tclass:with_opposite_avatar={opposite_avatar_img !== null}\\n\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t{#if avatar_img !== null}\\n\\t\\t\\t\\t\\t\\t<div class=\\"avatar-container\\">\\n\\t\\t\\t\\t\\t\\t\\t<Image\\n\\t\\t\\t\\t\\t\\t\\t\\tclass=\\"avatar-image\\"\\n\\t\\t\\t\\t\\t\\t\\t\\tsrc={avatar_img?.url}\\n\\t\\t\\t\\t\\t\\t\\t\\talt=\\"{role} avatar\\"\\n\\t\\t\\t\\t\\t\\t\\t/>\\n\\t\\t\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t\\t<div\\n\\t\\t\\t\\t\\t\\tclass=\\"flex-wrap {role} \\"\\n\\t\\t\\t\\t\\t\\tclass:component-wrap={messages[0].type === \\"component\\"}\\n\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t{#each messages as message, thought_index}\\n\\t\\t\\t\\t\\t\\t\\t<div\\n\\t\\t\\t\\t\\t\\t\\t\\tclass=\\"message {role} {is_component_message(message)\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t? message?.content.component\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t: \'\'}\\"\\n\\t\\t\\t\\t\\t\\t\\t\\tclass:message-fit={!bubble_full_width}\\n\\t\\t\\t\\t\\t\\t\\t\\tclass:panel-full-width={true}\\n\\t\\t\\t\\t\\t\\t\\t\\tclass:message-markdown-disabled={!render_markdown}\\n\\t\\t\\t\\t\\t\\t\\t\\tstyle:text-align={rtl && role === \\"user\\" ? \\"left\\" : \\"right\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\tclass:component={message.type === \\"component\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\tclass:html={is_component_message(message) &&\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tmessage.content.component === \\"html\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\tclass:thought={thought_index > 0}\\n\\t\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t\\t<button\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tdata-testid={role}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tclass:latest={i === value.length - 1}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tclass:message-markdown-disabled={!render_markdown}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tstyle:user-select=\\"text\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tclass:selectable\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tstyle:cursor={selectable ? \\"pointer\\" : \\"default\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tstyle:text-align={rtl ? \\"right\\" : \\"left\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\ton:click={() => handle_select(i, message)}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\ton:keydown={(e) => {\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tif (e.key === \\"Enter\\") {\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\thandle_select(i, message);\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t}}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\tdir={rtl ? \\"rtl\\" : \\"ltr\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\taria-label={role +\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\"\'s message: \\" +\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tget_message_label_data(message)}\\n\\t\\t\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t{#if message.type === \\"text\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{#if message.metadata.title}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t<MessageBox\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\ttitle={message.metadata.title}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\texpanded={is_last_bot_message(messages, value)}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t<Markdown\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tmessage={message.content}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{latex_delimiters}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{sanitize_html}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{render_markdown}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{line_breaks}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\ton:load={scroll}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{root}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t/>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t</MessageBox>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{:else}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t<Markdown\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tmessage={message.content}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{latex_delimiters}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{sanitize_html}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{render_markdown}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{line_breaks}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\ton:load={scroll}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{root}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t/>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t{:else if message.type === \\"component\\" && message.content.component in _components}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t<Component\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{target}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{theme_mode}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tprops={message.content.props}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\ttype={message.content.component}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tcomponents={_components}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tvalue={message.content.value}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{i18n}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{upload}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{_fetch}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\ton:load={scroll}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t/>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t{:else if message.type === \\"component\\" && message.content.component === \\"file\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t<a\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tdata-testid=\\"chatbot-file\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tclass=\\"file-pil\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\thref={message.content.value.url}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\ttarget=\\"_blank\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tdownload={window.__is_colab__\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t? null\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t: message.content.value?.orig_name ||\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tmessage.content.value?.path.split(\\"/\\").pop() ||\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\"file\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t{message.content.value?.orig_name ||\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tmessage.content.value?.path.split(\\"/\\").pop() ||\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\"file\\"}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t</a>\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t\\t\\t\\t\\t</button>\\n\\t\\t\\t\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t\\t\\t{/each}\\n\\t\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t{@const show_like =\\n\\t\\t\\t\\t\\trole === \\"user\\" ? likeable && like_user_message : likeable}\\n\\t\\t\\t\\t{@const show_retry = _retryable && is_last_bot_message(messages, value)}\\n\\t\\t\\t\\t{@const show_undo = _undoable && is_last_bot_message(messages, value)}\\n\\t\\t\\t\\t<LikeButtons\\n\\t\\t\\t\\t\\tshow={show_like || show_retry || show_undo || show_copy_button}\\n\\t\\t\\t\\t\\thandle_action={(selected) => handle_like(i, messages[0], selected)}\\n\\t\\t\\t\\t\\tlikeable={show_like}\\n\\t\\t\\t\\t\\t_retryable={show_retry}\\n\\t\\t\\t\\t\\t_undoable={show_undo}\\n\\t\\t\\t\\t\\tdisable={generating}\\n\\t\\t\\t\\t\\t{show_copy_button}\\n\\t\\t\\t\\t\\tmessage={msg_format === \\"tuples\\" ? messages[0] : messages}\\n\\t\\t\\t\\t\\tposition={role === \\"user\\" ? \\"right\\" : \\"left\\"}\\n\\t\\t\\t\\t\\tavatar={avatar_img}\\n\\t\\t\\t\\t\\t{layout}\\n\\t\\t\\t\\t/>\\n\\t\\t\\t{/each}\\n\\t\\t\\t{#if pending_message}\\n\\t\\t\\t\\t<Pending {layout} />\\n\\t\\t\\t{/if}\\n\\t\\t</div>\\n\\t{:else}\\n\\t\\t<div class=\\"placeholder-content\\">\\n\\t\\t\\t{#if placeholder !== null}\\n\\t\\t\\t\\t<div class=\\"placeholder\\">\\n\\t\\t\\t\\t\\t<Markdown message={placeholder} {latex_delimiters} {root} />\\n\\t\\t\\t\\t</div>\\n\\t\\t\\t{/if}\\n\\t\\t\\t{#if examples !== null}\\n\\t\\t\\t\\t<div class=\\"examples\\">\\n\\t\\t\\t\\t\\t{#each examples as example, i}\\n\\t\\t\\t\\t\\t\\t<button\\n\\t\\t\\t\\t\\t\\t\\tclass=\\"example\\"\\n\\t\\t\\t\\t\\t\\t\\ton:click={() => handle_example_select(i, example)}\\n\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t{#if example.icon !== undefined}\\n\\t\\t\\t\\t\\t\\t\\t\\t<div class=\\"example-icon-container\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t<Image\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tclass=\\"example-icon\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tsrc={example.icon.url}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\talt=\\"example-icon\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t/>\\n\\t\\t\\t\\t\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t\\t\\t\\t{#if example.display_text !== undefined}\\n\\t\\t\\t\\t\\t\\t\\t\\t<span class=\\"example-display-text\\">{example.display_text}</span>\\n\\t\\t\\t\\t\\t\\t\\t{:else}\\n\\t\\t\\t\\t\\t\\t\\t\\t<span class=\\"example-text\\">{example.text}</span>\\n\\t\\t\\t\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t\\t\\t\\t{#if example.files !== undefined && example.files.length > 1}\\n\\t\\t\\t\\t\\t\\t\\t\\t<span class=\\"example-file\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t><em>{example.files.length} Files</em></span\\n\\t\\t\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t{:else if example.files !== undefined && example.files[0] !== undefined && example.files[0].mime_type?.includes(\\"image\\")}\\n\\t\\t\\t\\t\\t\\t\\t\\t<div class=\\"example-image-container\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t<Image\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tclass=\\"example-image\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\tsrc={example.files[0].url}\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\talt=\\"example-image\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t/>\\n\\t\\t\\t\\t\\t\\t\\t\\t</div>\\n\\t\\t\\t\\t\\t\\t\\t{:else if example.files !== undefined && example.files[0] !== undefined}\\n\\t\\t\\t\\t\\t\\t\\t\\t<span class=\\"example-file\\"\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t><em>{example.files[0].orig_name}</em></span\\n\\t\\t\\t\\t\\t\\t\\t\\t>\\n\\t\\t\\t\\t\\t\\t\\t{/if}\\n\\t\\t\\t\\t\\t\\t</button>\\n\\t\\t\\t\\t\\t{/each}\\n\\t\\t\\t\\t</div>\\n\\t\\t\\t{/if}\\n\\t\\t</div>\\n\\t{/if}\\n</div>\\n\\n<style>\\n\\t.hidden {\\n\\t\\tdisplay: none;\\n\\t}\\n\\n\\t.placeholder-content {\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\theight: 100%;\\n\\t}\\n\\n\\t.placeholder {\\n\\t\\talign-items: center;\\n\\t\\tdisplay: flex;\\n\\t\\tjustify-content: center;\\n\\t\\theight: 100%;\\n\\t\\tflex-grow: 1;\\n\\t}\\n\\n\\t.examples :global(img) {\\n\\t\\tpointer-events: none;\\n\\t}\\n\\n\\t.examples {\\n\\t\\tmargin: auto;\\n\\t\\tpadding: var(--spacing-xxl);\\n\\t\\tdisplay: grid;\\n\\t\\tgrid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\\n\\t\\tgap: var(--spacing-xxl);\\n\\t\\tmax-width: calc(min(4 * 200px + 5 * var(--spacing-xxl), 100%));\\n\\t}\\n\\n\\t.example {\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\talign-items: center;\\n\\t\\tpadding: var(--spacing-xl);\\n\\t\\tborder: 0.05px solid var(--border-color-primary);\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t\\tbackground-color: var(--background-fill-secondary);\\n\\t\\tcursor: pointer;\\n\\t\\ttransition: var(--button-transition);\\n\\t\\tmax-width: var(--size-56);\\n\\t\\twidth: 100%;\\n\\t}\\n\\n\\t.example:hover {\\n\\t\\tbackground-color: var(--color-accent-soft);\\n\\t\\tborder-color: var(--border-color-accent);\\n\\t}\\n\\n\\t.example-icon-container {\\n\\t\\tdisplay: flex;\\n\\t\\talign-self: flex-start;\\n\\t\\tmargin-left: var(--spacing-md);\\n\\t\\twidth: var(--size-6);\\n\\t\\theight: var(--size-6);\\n\\t}\\n\\n\\t.example-display-text,\\n\\t.example-text,\\n\\t.example-file {\\n\\t\\tfont-size: var(--text-md);\\n\\t\\twidth: 100%;\\n\\t\\ttext-align: center;\\n\\t\\toverflow: hidden;\\n\\t\\ttext-overflow: ellipsis;\\n\\t}\\n\\n\\t.example-display-text,\\n\\t.example-file {\\n\\t\\tmargin-top: var(--spacing-md);\\n\\t}\\n\\n\\t.example-image-container {\\n\\t\\tflex-grow: 1;\\n\\t\\tdisplay: flex;\\n\\t\\tjustify-content: center;\\n\\t\\talign-items: center;\\n\\t\\tmargin-top: var(--spacing-xl);\\n\\t}\\n\\n\\t.example-image-container :global(img) {\\n\\t\\tmax-height: 100%;\\n\\t\\tmax-width: 100%;\\n\\t\\theight: var(--size-32);\\n\\t\\twidth: 100%;\\n\\t\\tobject-fit: cover;\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t}\\n\\n\\t.panel-wrap {\\n\\t\\twidth: 100%;\\n\\t\\toverflow-y: auto;\\n\\t}\\n\\n\\t.flex-wrap {\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t}\\n\\n\\t.bubble-wrap {\\n\\t\\twidth: 100%;\\n\\t\\toverflow-y: auto;\\n\\t\\theight: 100%;\\n\\t\\tpadding-top: var(--spacing-xxl);\\n\\t}\\n\\n\\t:global(.dark) .bubble-wrap {\\n\\t\\tbackground: var(--background-fill-secondary);\\n\\t}\\n\\n\\t.message-wrap {\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\tjustify-content: space-between;\\n\\t\\tmargin-bottom: var(--spacing-xxl);\\n\\t}\\n\\n\\t.bubble-gap {\\n\\t\\tgap: calc(var(--spacing-xxl) + var(--spacing-lg));\\n\\t}\\n\\n\\t.message-wrap > div :global(p:not(:first-child)) {\\n\\t\\tmargin-top: var(--spacing-xxl);\\n\\t}\\n\\n\\t.message {\\n\\t\\tposition: relative;\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\twidth: calc(100% - var(--spacing-xxl));\\n\\t\\tmax-width: 100%;\\n\\t\\tcolor: var(--body-text-color);\\n\\t\\tfont-size: var(--chatbot-text-size);\\n\\t\\toverflow-wrap: break-word;\\n\\t}\\n\\n\\t.thought {\\n\\t\\tmargin-top: var(--spacing-xxl);\\n\\t}\\n\\n\\t.message :global(.prose) {\\n\\t\\tfont-size: var(--chatbot-text-size);\\n\\t}\\n\\n\\t.message-bubble-border {\\n\\t\\tborder-width: 1px;\\n\\t\\tborder-radius: var(--radius-md);\\n\\t}\\n\\n\\t.user {\\n\\t\\talign-self: flex-end;\\n\\t}\\n\\n\\t.message-fit {\\n\\t\\twidth: fit-content !important;\\n\\t}\\n\\n\\t.panel-full-width {\\n\\t\\twidth: 100%;\\n\\t}\\n\\t.message-markdown-disabled {\\n\\t\\twhite-space: pre-line;\\n\\t}\\n\\n\\t.flex-wrap.user {\\n\\t\\tborder-width: 1px;\\n\\t\\tborder-radius: var(--radius-md);\\n\\t\\talign-self: flex-start;\\n\\t\\tborder-bottom-right-radius: 0;\\n\\t\\tbox-shadow: var(--shadow-drop);\\n\\t\\talign-self: flex-start;\\n\\t\\ttext-align: right;\\n\\t\\tpadding: var(--spacing-sm) var(--spacing-xl);\\n\\t\\tborder-color: var(--border-color-accent-subdued);\\n\\t\\tbackground-color: var(--color-accent-soft);\\n\\t}\\n\\n\\t:not(.component-wrap).flex-wrap.bot {\\n\\t\\tborder-width: 1px;\\n\\t\\tborder-radius: var(--radius-lg);\\n\\t\\talign-self: flex-start;\\n\\t\\tborder-bottom-left-radius: 0;\\n\\t\\tbox-shadow: var(--shadow-drop);\\n\\t\\talign-self: flex-start;\\n\\t\\ttext-align: right;\\n\\t\\tpadding: var(--spacing-sm) var(--spacing-xl);\\n\\t\\tborder-color: var(--border-color-primary);\\n\\t\\tbackground-color: var(--background-fill-secondary);\\n\\t}\\n\\n\\t.panel .user :global(*) {\\n\\t\\ttext-align: right;\\n\\t}\\n\\n\\t/* Colors */\\n\\t.bubble .bot {\\n\\t\\tborder-color: var(--border-color-primary);\\n\\t}\\n\\n\\t.message-row {\\n\\t\\tdisplay: flex;\\n\\t\\t/* flex-direction: column; */\\n\\t\\tposition: relative;\\n\\t}\\n\\n\\t.message-row.user-row {\\n\\t\\talign-self: flex-end;\\n\\t}\\n\\t.message-row.bubble {\\n\\t\\tmargin: calc(var(--spacing-xl) * 2);\\n\\t\\tmargin-bottom: var(--spacing-xl);\\n\\t}\\n\\n\\t.with_avatar.message-row.panel {\\n\\t\\tpadding-left: calc(var(--spacing-xl) * 2) !important;\\n\\t\\tpadding-right: calc(var(--spacing-xl) * 2) !important;\\n\\t}\\n\\n\\t.with_avatar.message-row.bubble.user-row {\\n\\t\\tmargin-right: calc(var(--spacing-xl) * 2) !important;\\n\\t}\\n\\n\\t.with_avatar.message-row.bubble.bot-row {\\n\\t\\tmargin-left: calc(var(--spacing-xl) * 2) !important;\\n\\t}\\n\\n\\t.with_opposite_avatar.message-row.bubble.user-row {\\n\\t\\tmargin-left: calc(var(--spacing-xxl) + 35px + var(--spacing-xxl));\\n\\t}\\n\\n\\t.message-row.panel {\\n\\t\\tmargin: 0;\\n\\t\\tpadding: calc(var(--spacing-xl) * 3) calc(var(--spacing-xxl) * 2);\\n\\t}\\n\\n\\t.message-row.panel.bot-row {\\n\\t\\tbackground: var(--background-fill-secondary);\\n\\t}\\n\\n\\t.message-row.bubble.user-row {\\n\\t\\talign-self: flex-end;\\n\\t\\tmax-width: calc(100% - var(--spacing-xl) * 6);\\n\\t}\\n\\n\\t.message-row.bubble.bot-row {\\n\\t\\talign-self: flex-start;\\n\\t\\tmax-width: calc(100% - var(--spacing-xl) * 6);\\n\\t}\\n\\n\\t.message-row:last-of-type {\\n\\t\\tmargin-bottom: calc(var(--spacing-xxl) * 2);\\n\\t}\\n\\n\\t.user-row.bubble {\\n\\t\\tflex-direction: row;\\n\\t\\tjustify-content: flex-end;\\n\\t}\\n\\t@media (max-width: 480px) {\\n\\t\\t.user-row.bubble {\\n\\t\\t\\talign-self: flex-end;\\n\\t\\t}\\n\\n\\t\\t.bot-row.bubble {\\n\\t\\t\\talign-self: flex-start;\\n\\t\\t}\\n\\t\\t.message {\\n\\t\\t\\twidth: 100%;\\n\\t\\t}\\n\\t}\\n\\n\\t.avatar-container {\\n\\t\\talign-self: flex-start;\\n\\t\\tposition: relative;\\n\\t\\tdisplay: flex;\\n\\t\\tjustify-content: flex-start;\\n\\t\\talign-items: flex-start;\\n\\t\\twidth: 35px;\\n\\t\\theight: 35px;\\n\\t\\tflex-shrink: 0;\\n\\t\\tbottom: 0;\\n\\t\\tborder-radius: 50%;\\n\\t\\tborder: 1px solid var(--border-color-primary);\\n\\t}\\n\\t.user-row > .avatar-container {\\n\\t\\torder: 2;\\n\\t\\tmargin-left: var(--spacing-xxl);\\n\\t}\\n\\t.bot-row > .avatar-container {\\n\\t\\tmargin-right: var(--spacing-xxl);\\n\\t\\tmargin-left: 0;\\n\\t\\tmargin-top: -5px;\\n\\t}\\n\\n\\t.avatar-container:not(.thumbnail-item) :global(img) {\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t\\tobject-fit: cover;\\n\\t\\tborder-radius: 50%;\\n\\t\\tpadding: 6px;\\n\\t}\\n\\n\\t.selectable {\\n\\t\\tcursor: pointer;\\n\\t}\\n\\n\\t@keyframes dot-flashing {\\n\\t\\t0% {\\n\\t\\t\\topacity: 0.8;\\n\\t\\t}\\n\\t\\t50% {\\n\\t\\t\\topacity: 0.5;\\n\\t\\t}\\n\\t\\t100% {\\n\\t\\t\\topacity: 0.8;\\n\\t\\t}\\n\\t}\\n\\t.message-wrap > .message :not(.image-button) :global(img) {\\n\\t\\tmargin: var(--size-2);\\n\\t\\tmax-height: 200px;\\n\\t}\\n\\n\\t.message-wrap\\n\\t\\t> div\\n\\t\\t:not(.avatar-container)\\n\\t\\tdiv\\n\\t\\t:not(.image-button)\\n\\t\\t:global(img) {\\n\\t\\tborder-radius: var(--radius-xl);\\n\\t\\tmargin: var(--size-2);\\n\\t\\twidth: 400px;\\n\\t\\tmax-width: 30vw;\\n\\t\\tmax-height: 30vw;\\n\\t}\\n\\n\\t.message-wrap .message :global(a) {\\n\\t\\tcolor: var(--color-text-link);\\n\\t\\ttext-decoration: underline;\\n\\t}\\n\\n\\t.message-wrap .bot :global(table),\\n\\t.message-wrap .bot :global(tr),\\n\\t.message-wrap .bot :global(td),\\n\\t.message-wrap .bot :global(th) {\\n\\t\\tborder: 1px solid var(--border-color-primary);\\n\\t}\\n\\n\\t.message-wrap .user :global(table),\\n\\t.message-wrap .user :global(tr),\\n\\t.message-wrap .user :global(td),\\n\\t.message-wrap .user :global(th) {\\n\\t\\tborder: 1px solid var(--border-color-accent);\\n\\t}\\n\\n\\t/* KaTeX */\\n\\t.message-wrap :global(span.katex) {\\n\\t\\tfont-size: var(--text-lg);\\n\\t\\tdirection: ltr;\\n\\t}\\n\\n\\t/* Copy button */\\n\\t.message-wrap :global(div[class*=\\"code_wrap\\"] > button) {\\n\\t\\tposition: absolute;\\n\\t\\ttop: var(--spacing-md);\\n\\t\\tright: var(--spacing-md);\\n\\t\\tz-index: 1;\\n\\t\\tcursor: pointer;\\n\\t\\tborder-bottom-left-radius: var(--radius-sm);\\n\\t\\tpadding: var(--spacing-md);\\n\\t\\twidth: 25px;\\n\\t\\theight: 25px;\\n\\t}\\n\\n\\t.message-wrap :global(code > button > span) {\\n\\t\\tposition: absolute;\\n\\t\\ttop: var(--spacing-md);\\n\\t\\tright: var(--spacing-md);\\n\\t\\twidth: 12px;\\n\\t\\theight: 12px;\\n\\t}\\n\\t.message-wrap :global(.check) {\\n\\t\\tposition: absolute;\\n\\t\\ttop: 0;\\n\\t\\tright: 0;\\n\\t\\topacity: 0;\\n\\t\\tz-index: var(--layer-top);\\n\\t\\ttransition: opacity 0.2s;\\n\\t\\tbackground: var(--background-fill-primary);\\n\\t\\tpadding: var(--size-1);\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t\\tcolor: var(--body-text-color);\\n\\t}\\n\\n\\t.message-wrap :global(pre) {\\n\\t\\tposition: relative;\\n\\t}\\n\\n\\t.message-wrap :global(.grid-wrap) {\\n\\t\\tmax-height: 80% !important;\\n\\t\\tmax-width: 600px;\\n\\t\\tobject-fit: contain;\\n\\t}\\n\\n\\t/* Image preview */\\n\\t.message :global(.preview) {\\n\\t\\tobject-fit: contain;\\n\\t\\twidth: 95%;\\n\\t\\tmax-height: 93%;\\n\\t}\\n\\t.image-preview {\\n\\t\\tposition: absolute;\\n\\t\\tz-index: 999;\\n\\t\\tleft: 0;\\n\\t\\ttop: 0;\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t\\toverflow: auto;\\n\\t\\tbackground-color: rgba(0, 0, 0, 0.9);\\n\\t\\tdisplay: flex;\\n\\t\\tjustify-content: center;\\n\\t\\talign-items: center;\\n\\t}\\n\\t.image-preview :global(svg) {\\n\\t\\tstroke: white;\\n\\t}\\n\\t.image-preview-close-button {\\n\\t\\tposition: absolute;\\n\\t\\ttop: 10px;\\n\\t\\tright: 10px;\\n\\t\\tbackground: none;\\n\\t\\tborder: none;\\n\\t\\tfont-size: 1.5em;\\n\\t\\tcursor: pointer;\\n\\t\\theight: 30px;\\n\\t\\twidth: 30px;\\n\\t\\tpadding: 3px;\\n\\t\\tbackground: var(--bg-color);\\n\\t\\tbox-shadow: var(--shadow-drop);\\n\\t\\tborder: 1px solid var(--button-secondary-border-color);\\n\\t\\tborder-radius: var(--radius-lg);\\n\\t}\\n\\n\\t.component {\\n\\t\\tpadding: 0;\\n\\t\\tborder-radius: var(--radius-md);\\n\\t\\twidth: fit-content;\\n\\t\\toverflow: hidden;\\n\\t}\\n\\n\\t.component.gallery {\\n\\t\\tborder: none;\\n\\t}\\n\\n\\t.file-pil {\\n\\t\\tdisplay: block;\\n\\t\\twidth: fit-content;\\n\\t\\tpadding: var(--spacing-sm) var(--spacing-lg);\\n\\t\\tborder-radius: var(--radius-md);\\n\\t\\tbackground: var(--background-fill-secondary);\\n\\t\\tcolor: var(--body-text-color);\\n\\t\\ttext-decoration: none;\\n\\t\\tmargin: 0;\\n\\t\\tfont-family: var(--font-mono);\\n\\t\\tfont-size: var(--text-sm);\\n\\t}\\n\\n\\t.file {\\n\\t\\twidth: auto !important;\\n\\t\\tmax-width: fit-content !important;\\n\\t}\\n\\n\\t@media (max-width: 600px) or (max-width: 480px) {\\n\\t\\t.component {\\n\\t\\t\\twidth: 100%;\\n\\t\\t}\\n\\t}\\n\\n\\t.message-wrap :global(.prose.chatbot.md) {\\n\\t\\topacity: 0.8;\\n\\t\\toverflow-wrap: break-word;\\n\\t}\\n\\n\\t.message > button {\\n\\t\\twidth: 100%;\\n\\t}\\n\\t.html {\\n\\t\\tpadding: 0;\\n\\t\\tborder: none;\\n\\t\\tbackground: none;\\n\\t}</style>\\n"],"names":[],"mappings":"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"}'
};
function get_components_from_messages(messages) {
  if (!messages)
    return [];
  let components = /* @__PURE__ */ new Set();
  messages.forEach((message) => {
    if (message.type === "component") {
      components.add(message.content.component);
    }
  });
  return Array.from(components);
}
function is_last_bot_message(messages, all_messages) {
  const is_bot = messages[messages.length - 1].role === "assistant";
  const last_index = messages[messages.length - 1].index;
  const is_last = JSON.stringify(last_index) === JSON.stringify(all_messages[all_messages.length - 1].index);
  return is_last && is_bot;
}
function get_message_label_data(message) {
  if (message.type === "text") {
    return message.content;
  } else if (message.type === "component" && message.content.component === "file") {
    if (Array.isArray(message.content.value)) {
      return `file of extension type: ${message.content.value[0].orig_name?.split(".").pop()}`;
    }
    return `file of extension type: ${message.content.value?.orig_name?.split(".").pop()}` + (message.content.value?.orig_name ?? "");
  }
  return `a component of type ${message.content.component ?? "unknown"}`;
}
const ChatBot = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let groupedMessages;
  let { value = [] } = $$props;
  let old_value = null;
  let { _fetch } = $$props;
  let { load_component } = $$props;
  let _components = {};
  async function load_components(component_names) {
    let names = [];
    let components = [];
    component_names.forEach((component_name) => {
      if (_components[component_name] || component_name === "file") {
        return;
      }
      const { name, component } = load_component(component_name, "base");
      names.push(name);
      components.push(component);
    });
    const loaded_components = await Promise.all(components);
    loaded_components.forEach((component, i) => {
      _components[names[i]] = component.default;
    });
  }
  let { latex_delimiters } = $$props;
  let { pending_message = false } = $$props;
  let { generating = false } = $$props;
  let { selectable = false } = $$props;
  let { likeable = false } = $$props;
  let { show_share_button = false } = $$props;
  let { show_copy_all_button = false } = $$props;
  let { rtl = false } = $$props;
  let { show_copy_button = false } = $$props;
  let { avatar_images = [null, null] } = $$props;
  let { sanitize_html = true } = $$props;
  let { bubble_full_width = true } = $$props;
  let { render_markdown = true } = $$props;
  let { line_breaks = true } = $$props;
  let { theme_mode } = $$props;
  let { i18n } = $$props;
  let { layout = "bubble" } = $$props;
  let { placeholder = null } = $$props;
  let { upload } = $$props;
  let { msg_format = "tuples" } = $$props;
  let { examples = null } = $$props;
  let { _retryable = false } = $$props;
  let { _undoable = false } = $$props;
  let { like_user_message = false } = $$props;
  let { root } = $$props;
  let target = null;
  let div;
  let autoscroll;
  const dispatch = createEventDispatcher();
  async function scroll() {
    return;
  }
  function handle_like(i, message, selected) {
    if (selected === "undo" || selected === "retry") {
      const val_ = value;
      let last_index = val_.length - 1;
      while (val_[last_index].role === "assistant") {
        last_index--;
      }
      dispatch(selected, {
        index: val_[last_index].index,
        value: val_[last_index].content
      });
      return;
    }
    if (msg_format === "tuples") {
      dispatch("like", {
        index: message.index,
        value: message.content,
        liked: selected === "like"
      });
    } else {
      if (!groupedMessages)
        return;
      const message_group = groupedMessages[i];
      const [first, last] = [message_group[0], message_group[message_group.length - 1]];
      dispatch("like", {
        index: [first.index, last.index],
        value: message_group.map((m) => m.content),
        liked: selected === "like"
      });
    }
  }
  function group_messages(messages) {
    const groupedMessages2 = [];
    let currentGroup = [];
    let currentRole = null;
    for (const message of messages) {
      if (msg_format === "tuples") {
        currentRole = null;
      }
      if (!(message.role === "assistant" || message.role === "user")) {
        continue;
      }
      if (message.role === currentRole) {
        currentGroup.push(message);
      } else {
        if (currentGroup.length > 0) {
          groupedMessages2.push(currentGroup);
        }
        currentGroup = [message];
        currentRole = message.role;
      }
    }
    if (currentGroup.length > 0) {
      groupedMessages2.push(currentGroup);
    }
    return groupedMessages2;
  }
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props._fetch === void 0 && $$bindings._fetch && _fetch !== void 0)
    $$bindings._fetch(_fetch);
  if ($$props.load_component === void 0 && $$bindings.load_component && load_component !== void 0)
    $$bindings.load_component(load_component);
  if ($$props.latex_delimiters === void 0 && $$bindings.latex_delimiters && latex_delimiters !== void 0)
    $$bindings.latex_delimiters(latex_delimiters);
  if ($$props.pending_message === void 0 && $$bindings.pending_message && pending_message !== void 0)
    $$bindings.pending_message(pending_message);
  if ($$props.generating === void 0 && $$bindings.generating && generating !== void 0)
    $$bindings.generating(generating);
  if ($$props.selectable === void 0 && $$bindings.selectable && selectable !== void 0)
    $$bindings.selectable(selectable);
  if ($$props.likeable === void 0 && $$bindings.likeable && likeable !== void 0)
    $$bindings.likeable(likeable);
  if ($$props.show_share_button === void 0 && $$bindings.show_share_button && show_share_button !== void 0)
    $$bindings.show_share_button(show_share_button);
  if ($$props.show_copy_all_button === void 0 && $$bindings.show_copy_all_button && show_copy_all_button !== void 0)
    $$bindings.show_copy_all_button(show_copy_all_button);
  if ($$props.rtl === void 0 && $$bindings.rtl && rtl !== void 0)
    $$bindings.rtl(rtl);
  if ($$props.show_copy_button === void 0 && $$bindings.show_copy_button && show_copy_button !== void 0)
    $$bindings.show_copy_button(show_copy_button);
  if ($$props.avatar_images === void 0 && $$bindings.avatar_images && avatar_images !== void 0)
    $$bindings.avatar_images(avatar_images);
  if ($$props.sanitize_html === void 0 && $$bindings.sanitize_html && sanitize_html !== void 0)
    $$bindings.sanitize_html(sanitize_html);
  if ($$props.bubble_full_width === void 0 && $$bindings.bubble_full_width && bubble_full_width !== void 0)
    $$bindings.bubble_full_width(bubble_full_width);
  if ($$props.render_markdown === void 0 && $$bindings.render_markdown && render_markdown !== void 0)
    $$bindings.render_markdown(render_markdown);
  if ($$props.line_breaks === void 0 && $$bindings.line_breaks && line_breaks !== void 0)
    $$bindings.line_breaks(line_breaks);
  if ($$props.theme_mode === void 0 && $$bindings.theme_mode && theme_mode !== void 0)
    $$bindings.theme_mode(theme_mode);
  if ($$props.i18n === void 0 && $$bindings.i18n && i18n !== void 0)
    $$bindings.i18n(i18n);
  if ($$props.layout === void 0 && $$bindings.layout && layout !== void 0)
    $$bindings.layout(layout);
  if ($$props.placeholder === void 0 && $$bindings.placeholder && placeholder !== void 0)
    $$bindings.placeholder(placeholder);
  if ($$props.upload === void 0 && $$bindings.upload && upload !== void 0)
    $$bindings.upload(upload);
  if ($$props.msg_format === void 0 && $$bindings.msg_format && msg_format !== void 0)
    $$bindings.msg_format(msg_format);
  if ($$props.examples === void 0 && $$bindings.examples && examples !== void 0)
    $$bindings.examples(examples);
  if ($$props._retryable === void 0 && $$bindings._retryable && _retryable !== void 0)
    $$bindings._retryable(_retryable);
  if ($$props._undoable === void 0 && $$bindings._undoable && _undoable !== void 0)
    $$bindings._undoable(_undoable);
  if ($$props.like_user_message === void 0 && $$bindings.like_user_message && like_user_message !== void 0)
    $$bindings.like_user_message(like_user_message);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  $$result.css.add(css$1);
  {
    load_components(get_components_from_messages(value));
  }
  {
    if (value || autoscroll || _components) {
      scroll();
    }
  }
  {
    {
      if (!dequal(value, old_value)) {
        old_value = value;
        dispatch("change");
      }
    }
  }
  groupedMessages = value && group_messages(value);
  return `${value !== null && value.length > 0 ? `${validate_component(IconButtonWrapper, "IconButtonWrapper").$$render($$result, {}, {}, {
    default: () => {
      return `${show_share_button ? `${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Community }, {}, {
        default: () => {
          return `${validate_component(Community, "Community").$$render($$result, {}, {}, {})}`;
        }
      })}` : ``} ${validate_component(IconButton, "IconButton").$$render($$result, { Icon: Trash }, {}, {})} ${show_copy_all_button ? `${validate_component(CopyAll, "CopyAll").$$render($$result, { value }, {}, {})}` : ``}`;
    }
  })}` : ``} <div class="${escape(null_to_empty(layout === "bubble" ? "bubble-wrap" : "panel-wrap"), true) + " svelte-18fn4d"}" role="log" aria-label="chatbot conversation" aria-live="polite"${add_attribute("this", div, 0)}>${value !== null && value.length > 0 && groupedMessages !== null ? `<div class="message-wrap svelte-18fn4d">${each(groupedMessages, (messages, i) => {
    let role = messages[0].role === "user" ? "user" : "bot", avatar_img = avatar_images[role === "user" ? 0 : 1], opposite_avatar_img = avatar_images[role === "user" ? 0 : 1], show_like = role === "user" ? likeable && like_user_message : likeable, show_retry = _retryable && is_last_bot_message(messages, value), show_undo = _undoable && is_last_bot_message(messages, value);
    return `   ${``} <div class="${[
      "message-row " + escape(layout, true) + " " + escape(role, true) + "-row svelte-18fn4d",
      (avatar_img !== null ? "with_avatar" : "") + " " + (opposite_avatar_img !== null ? "with_opposite_avatar" : "")
    ].join(" ").trim()}">${avatar_img !== null ? `<div class="avatar-container svelte-18fn4d">${validate_component(Image$1, "Image").$$render(
      $$result,
      {
        class: "avatar-image",
        src: avatar_img?.url,
        alt: role + " avatar"
      },
      {},
      {}
    )} </div>` : ``} <div class="${[
      "flex-wrap " + escape(role, true) + " svelte-18fn4d",
      messages[0].type === "component" ? "component-wrap" : ""
    ].join(" ").trim()}">${each(messages, (message, thought_index) => {
      return `<div class="${[
        "message " + escape(role, true) + " " + escape(
          is_component_message(message) ? message?.content.component : "",
          true
        ) + " svelte-18fn4d",
        (!bubble_full_width ? "message-fit" : "") + " panel-full-width " + (!render_markdown ? "message-markdown-disabled" : "") + " " + (message.type === "component" ? "component" : "") + " " + (is_component_message(message) && message.content.component === "html" ? "html" : "") + " " + (thought_index > 0 ? "thought" : "")
      ].join(" ").trim()}"${add_styles({
        "text-align": rtl && role === "user" ? "left" : "right"
      })}><button${add_attribute("data-testid", role, 0)}${add_attribute("dir", rtl ? "rtl" : "ltr", 0)}${add_attribute("aria-label", role + "'s message: " + get_message_label_data(message), 0)} class="${[
        "svelte-18fn4d",
        (i === value.length - 1 ? "latest" : "") + " " + (!render_markdown ? "message-markdown-disabled" : "") + " " + (selectable ? "selectable" : "")
      ].join(" ").trim()}"${add_styles({
        "user-select": `text`,
        "cursor": selectable ? "pointer" : "default",
        "text-align": rtl ? "right" : "left"
      })}>${message.type === "text" ? `${message.metadata.title ? `${validate_component(MessageBox, "MessageBox").$$render(
        $$result,
        {
          title: message.metadata.title,
          expanded: is_last_bot_message(messages, value)
        },
        {},
        {
          default: () => {
            return `${validate_component(MarkdownCode, "Markdown").$$render(
              $$result,
              {
                message: message.content,
                latex_delimiters,
                sanitize_html,
                render_markdown,
                line_breaks,
                root
              },
              {},
              {}
            )} `;
          }
        }
      )}` : `${validate_component(MarkdownCode, "Markdown").$$render(
        $$result,
        {
          message: message.content,
          latex_delimiters,
          sanitize_html,
          render_markdown,
          line_breaks,
          root
        },
        {},
        {}
      )}`}` : `${message.type === "component" && message.content.component in _components ? `${validate_component(Component, "Component").$$render(
        $$result,
        {
          target,
          theme_mode,
          props: message.content.props,
          type: message.content.component,
          components: _components,
          value: message.content.value,
          i18n,
          upload,
          _fetch
        },
        {},
        {}
      )}` : `${message.type === "component" && message.content.component === "file" ? `<a data-testid="chatbot-file" class="file-pil svelte-18fn4d"${add_attribute("href", message.content.value.url, 0)} target="_blank"${add_attribute(
        "download",
        window.__is_colab__ ? null : message.content.value?.orig_name || message.content.value?.path.split("/").pop() || "file",
        0
      )}>${escape(message.content.value?.orig_name || message.content.value?.path.split("/").pop() || "file")} </a>` : ``}`}`}</button> </div>`;
    })} </div></div>    ${validate_component(ButtonPanel, "LikeButtons").$$render(
      $$result,
      {
        show: show_like || show_retry || show_undo || show_copy_button,
        handle_action: (selected) => handle_like(i, messages[0], selected),
        likeable: show_like,
        _retryable: show_retry,
        _undoable: show_undo,
        disable: generating,
        show_copy_button,
        message: msg_format === "tuples" ? messages[0] : messages,
        position: role === "user" ? "right" : "left",
        avatar: avatar_img,
        layout
      },
      {},
      {}
    )}`;
  })} ${pending_message ? `${validate_component(Pending, "Pending").$$render($$result, { layout }, {}, {})}` : ``}</div>` : `<div class="placeholder-content svelte-18fn4d">${placeholder !== null ? `<div class="placeholder svelte-18fn4d">${validate_component(MarkdownCode, "Markdown").$$render(
    $$result,
    {
      message: placeholder,
      latex_delimiters,
      root
    },
    {},
    {}
  )}</div>` : ``} ${examples !== null ? `<div class="examples svelte-18fn4d">${each(examples, (example, i) => {
    return `<button class="example svelte-18fn4d">${example.icon !== void 0 ? `<div class="example-icon-container svelte-18fn4d">${validate_component(Image$1, "Image").$$render(
      $$result,
      {
        class: "example-icon",
        src: example.icon.url,
        alt: "example-icon"
      },
      {},
      {}
    )} </div>` : ``} ${example.display_text !== void 0 ? `<span class="example-display-text svelte-18fn4d">${escape(example.display_text)}</span>` : `<span class="example-text svelte-18fn4d">${escape(example.text)}</span>`} ${example.files !== void 0 && example.files.length > 1 ? `<span class="example-file svelte-18fn4d"><em class="svelte-18fn4d">${escape(example.files.length)} Files</em></span>` : `${example.files !== void 0 && example.files[0] !== void 0 && example.files[0].mime_type?.includes("image") ? `<div class="example-image-container svelte-18fn4d">${validate_component(Image$1, "Image").$$render(
      $$result,
      {
        class: "example-image",
        src: example.files[0].url,
        alt: "example-image"
      },
      {},
      {}
    )} </div>` : `${example.files !== void 0 && example.files[0] !== void 0 ? `<span class="example-file svelte-18fn4d"><em class="svelte-18fn4d">${escape(example.files[0].orig_name)}</em></span>` : ``}`}`} </button>`;
  })}</div>` : ``}</div>`} </div>`;
});
const ChatBot$1 = ChatBot;
const css = {
  code: ".wrapper.svelte-g3p8na{display:flex;position:relative;flex-direction:column;align-items:start;width:100%;height:100%;flex-grow:1}.progress-text{right:auto}",
  map: '{"version":3,"file":"Index.svelte","sources":["Index.svelte"],"sourcesContent":["<script context=\\"module\\" lang=\\"ts\\">export { default as BaseChatBot } from \\"./shared/ChatBot.svelte\\";\\n<\/script>\\n\\n<script lang=\\"ts\\">import ChatBot from \\"./shared/ChatBot.svelte\\";\\nimport { Block, BlockLabel } from \\"@gradio/atoms\\";\\nimport { Chat } from \\"@gradio/icons\\";\\nimport { StatusTracker } from \\"@gradio/statustracker\\";\\nimport { normalise_tuples, normalise_messages } from \\"./shared/utils\\";\\nexport let elem_id = \\"\\";\\nexport let elem_classes = [];\\nexport let visible = true;\\nexport let value = [];\\nexport let scale = null;\\nexport let min_width = void 0;\\nexport let label;\\nexport let show_label = true;\\nexport let root;\\nexport let _selectable = false;\\nexport let likeable = false;\\nexport let show_share_button = false;\\nexport let rtl = false;\\nexport let show_copy_button = true;\\nexport let show_copy_all_button = false;\\nexport let sanitize_html = true;\\nexport let bubble_full_width = true;\\nexport let layout = \\"bubble\\";\\nexport let type = \\"tuples\\";\\nexport let render_markdown = true;\\nexport let line_breaks = true;\\nexport let _retryable = false;\\nexport let _undoable = false;\\nexport let latex_delimiters;\\nexport let gradio;\\nlet _value = [];\\n$: _value = type === \\"tuples\\" ? normalise_tuples(value, root) : normalise_messages(value, root);\\nexport let avatar_images = [null, null];\\nexport let like_user_message = false;\\nexport let loading_status = void 0;\\nexport let height;\\nexport let min_height;\\nexport let max_height;\\nexport let placeholder = null;\\nexport let examples = null;\\nexport let theme_mode;\\n<\/script>\\n\\n<Block\\n\\t{elem_id}\\n\\t{elem_classes}\\n\\t{visible}\\n\\tpadding={false}\\n\\t{scale}\\n\\t{min_width}\\n\\t{height}\\n\\t{min_height}\\n\\t{max_height}\\n\\tallow_overflow={true}\\n\\tflex={true}\\n\\toverflow_behavior=\\"auto\\"\\n>\\n\\t{#if loading_status}\\n\\t\\t<StatusTracker\\n\\t\\t\\tautoscroll={gradio.autoscroll}\\n\\t\\t\\ti18n={gradio.i18n}\\n\\t\\t\\t{...loading_status}\\n\\t\\t\\tshow_progress={loading_status.show_progress === \\"hidden\\"\\n\\t\\t\\t\\t? \\"hidden\\"\\n\\t\\t\\t\\t: \\"minimal\\"}\\n\\t\\t\\ton:clear_status={() => gradio.dispatch(\\"clear_status\\", loading_status)}\\n\\t\\t/>\\n\\t{/if}\\n\\t<div class=\\"wrapper\\">\\n\\t\\t{#if show_label}\\n\\t\\t\\t<BlockLabel\\n\\t\\t\\t\\t{show_label}\\n\\t\\t\\t\\tIcon={Chat}\\n\\t\\t\\t\\tfloat={true}\\n\\t\\t\\t\\tlabel={label || \\"Chatbot\\"}\\n\\t\\t\\t/>\\n\\t\\t{/if}\\n\\t\\t<ChatBot\\n\\t\\t\\ti18n={gradio.i18n}\\n\\t\\t\\tselectable={_selectable}\\n\\t\\t\\t{likeable}\\n\\t\\t\\t{show_share_button}\\n\\t\\t\\t{show_copy_all_button}\\n\\t\\t\\tvalue={_value}\\n\\t\\t\\t{latex_delimiters}\\n\\t\\t\\t{render_markdown}\\n\\t\\t\\t{theme_mode}\\n\\t\\t\\tpending_message={loading_status?.status === \\"pending\\"}\\n\\t\\t\\tgenerating={loading_status?.status === \\"generating\\"}\\n\\t\\t\\t{rtl}\\n\\t\\t\\t{show_copy_button}\\n\\t\\t\\t{like_user_message}\\n\\t\\t\\ton:change={() => gradio.dispatch(\\"change\\", value)}\\n\\t\\t\\ton:select={(e) => gradio.dispatch(\\"select\\", e.detail)}\\n\\t\\t\\ton:like={(e) => gradio.dispatch(\\"like\\", e.detail)}\\n\\t\\t\\ton:share={(e) => gradio.dispatch(\\"share\\", e.detail)}\\n\\t\\t\\ton:error={(e) => gradio.dispatch(\\"error\\", e.detail)}\\n\\t\\t\\ton:example_select={(e) => gradio.dispatch(\\"example_select\\", e.detail)}\\n\\t\\t\\ton:retry={(e) => gradio.dispatch(\\"retry\\", e.detail)}\\n\\t\\t\\ton:undo={(e) => gradio.dispatch(\\"undo\\", e.detail)}\\n\\t\\t\\ton:clear={() => {\\n\\t\\t\\t\\tvalue = [];\\n\\t\\t\\t\\tgradio.dispatch(\\"clear\\");\\n\\t\\t\\t}}\\n\\t\\t\\t{avatar_images}\\n\\t\\t\\t{sanitize_html}\\n\\t\\t\\t{bubble_full_width}\\n\\t\\t\\t{line_breaks}\\n\\t\\t\\t{layout}\\n\\t\\t\\t{placeholder}\\n\\t\\t\\t{examples}\\n\\t\\t\\t{_retryable}\\n\\t\\t\\t{_undoable}\\n\\t\\t\\tupload={(...args) => gradio.client.upload(...args)}\\n\\t\\t\\t_fetch={(...args) => gradio.client.fetch(...args)}\\n\\t\\t\\tload_component={gradio.load_component}\\n\\t\\t\\tmsg_format={type}\\n\\t\\t\\troot={gradio.root}\\n\\t\\t/>\\n\\t</div>\\n</Block>\\n\\n<style>\\n\\t.wrapper {\\n\\t\\tdisplay: flex;\\n\\t\\tposition: relative;\\n\\t\\tflex-direction: column;\\n\\t\\talign-items: start;\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t\\tflex-grow: 1;\\n\\t}\\n\\n\\t:global(.progress-text) {\\n\\t\\tright: auto;\\n\\t}</style>\\n"],"names":[],"mappings":"AA8HC,sBAAS,CACR,OAAO,CAAE,IAAI,CACb,QAAQ,CAAE,QAAQ,CAClB,cAAc,CAAE,MAAM,CACtB,WAAW,CAAE,KAAK,CAClB,KAAK,CAAE,IAAI,CACX,MAAM,CAAE,IAAI,CACZ,SAAS,CAAE,CACZ,CAEQ,cAAgB,CACvB,KAAK,CAAE,IACR"}'
};
const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { elem_id = "" } = $$props;
  let { elem_classes = [] } = $$props;
  let { visible = true } = $$props;
  let { value = [] } = $$props;
  let { scale = null } = $$props;
  let { min_width = void 0 } = $$props;
  let { label } = $$props;
  let { show_label = true } = $$props;
  let { root } = $$props;
  let { _selectable = false } = $$props;
  let { likeable = false } = $$props;
  let { show_share_button = false } = $$props;
  let { rtl = false } = $$props;
  let { show_copy_button = true } = $$props;
  let { show_copy_all_button = false } = $$props;
  let { sanitize_html = true } = $$props;
  let { bubble_full_width = true } = $$props;
  let { layout = "bubble" } = $$props;
  let { type = "tuples" } = $$props;
  let { render_markdown = true } = $$props;
  let { line_breaks = true } = $$props;
  let { _retryable = false } = $$props;
  let { _undoable = false } = $$props;
  let { latex_delimiters } = $$props;
  let { gradio } = $$props;
  let _value = [];
  let { avatar_images = [null, null] } = $$props;
  let { like_user_message = false } = $$props;
  let { loading_status = void 0 } = $$props;
  let { height } = $$props;
  let { min_height } = $$props;
  let { max_height } = $$props;
  let { placeholder = null } = $$props;
  let { examples = null } = $$props;
  let { theme_mode } = $$props;
  if ($$props.elem_id === void 0 && $$bindings.elem_id && elem_id !== void 0)
    $$bindings.elem_id(elem_id);
  if ($$props.elem_classes === void 0 && $$bindings.elem_classes && elem_classes !== void 0)
    $$bindings.elem_classes(elem_classes);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.scale === void 0 && $$bindings.scale && scale !== void 0)
    $$bindings.scale(scale);
  if ($$props.min_width === void 0 && $$bindings.min_width && min_width !== void 0)
    $$bindings.min_width(min_width);
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.root === void 0 && $$bindings.root && root !== void 0)
    $$bindings.root(root);
  if ($$props._selectable === void 0 && $$bindings._selectable && _selectable !== void 0)
    $$bindings._selectable(_selectable);
  if ($$props.likeable === void 0 && $$bindings.likeable && likeable !== void 0)
    $$bindings.likeable(likeable);
  if ($$props.show_share_button === void 0 && $$bindings.show_share_button && show_share_button !== void 0)
    $$bindings.show_share_button(show_share_button);
  if ($$props.rtl === void 0 && $$bindings.rtl && rtl !== void 0)
    $$bindings.rtl(rtl);
  if ($$props.show_copy_button === void 0 && $$bindings.show_copy_button && show_copy_button !== void 0)
    $$bindings.show_copy_button(show_copy_button);
  if ($$props.show_copy_all_button === void 0 && $$bindings.show_copy_all_button && show_copy_all_button !== void 0)
    $$bindings.show_copy_all_button(show_copy_all_button);
  if ($$props.sanitize_html === void 0 && $$bindings.sanitize_html && sanitize_html !== void 0)
    $$bindings.sanitize_html(sanitize_html);
  if ($$props.bubble_full_width === void 0 && $$bindings.bubble_full_width && bubble_full_width !== void 0)
    $$bindings.bubble_full_width(bubble_full_width);
  if ($$props.layout === void 0 && $$bindings.layout && layout !== void 0)
    $$bindings.layout(layout);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.render_markdown === void 0 && $$bindings.render_markdown && render_markdown !== void 0)
    $$bindings.render_markdown(render_markdown);
  if ($$props.line_breaks === void 0 && $$bindings.line_breaks && line_breaks !== void 0)
    $$bindings.line_breaks(line_breaks);
  if ($$props._retryable === void 0 && $$bindings._retryable && _retryable !== void 0)
    $$bindings._retryable(_retryable);
  if ($$props._undoable === void 0 && $$bindings._undoable && _undoable !== void 0)
    $$bindings._undoable(_undoable);
  if ($$props.latex_delimiters === void 0 && $$bindings.latex_delimiters && latex_delimiters !== void 0)
    $$bindings.latex_delimiters(latex_delimiters);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.avatar_images === void 0 && $$bindings.avatar_images && avatar_images !== void 0)
    $$bindings.avatar_images(avatar_images);
  if ($$props.like_user_message === void 0 && $$bindings.like_user_message && like_user_message !== void 0)
    $$bindings.like_user_message(like_user_message);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.height === void 0 && $$bindings.height && height !== void 0)
    $$bindings.height(height);
  if ($$props.min_height === void 0 && $$bindings.min_height && min_height !== void 0)
    $$bindings.min_height(min_height);
  if ($$props.max_height === void 0 && $$bindings.max_height && max_height !== void 0)
    $$bindings.max_height(max_height);
  if ($$props.placeholder === void 0 && $$bindings.placeholder && placeholder !== void 0)
    $$bindings.placeholder(placeholder);
  if ($$props.examples === void 0 && $$bindings.examples && examples !== void 0)
    $$bindings.examples(examples);
  if ($$props.theme_mode === void 0 && $$bindings.theme_mode && theme_mode !== void 0)
    $$bindings.theme_mode(theme_mode);
  $$result.css.add(css);
  _value = type === "tuples" ? normalise_tuples(value, root) : normalise_messages(value, root);
  return `${validate_component(Block, "Block").$$render(
    $$result,
    {
      elem_id,
      elem_classes,
      visible,
      padding: false,
      scale,
      min_width,
      height,
      min_height,
      max_height,
      allow_overflow: true,
      flex: true,
      overflow_behavior: "auto"
    },
    {},
    {
      default: () => {
        return `${loading_status ? `${validate_component(Static, "StatusTracker").$$render(
          $$result,
          Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status, {
            show_progress: loading_status.show_progress === "hidden" ? "hidden" : "minimal"
          }),
          {},
          {}
        )}` : ``} <div class="wrapper svelte-g3p8na">${show_label ? `${validate_component(BlockLabel, "BlockLabel").$$render(
          $$result,
          {
            show_label,
            Icon: Chat,
            float: true,
            label: label || "Chatbot"
          },
          {},
          {}
        )}` : ``} ${validate_component(ChatBot$1, "ChatBot").$$render(
          $$result,
          {
            i18n: gradio.i18n,
            selectable: _selectable,
            likeable,
            show_share_button,
            show_copy_all_button,
            value: _value,
            latex_delimiters,
            render_markdown,
            theme_mode,
            pending_message: loading_status?.status === "pending",
            generating: loading_status?.status === "generating",
            rtl,
            show_copy_button,
            like_user_message,
            avatar_images,
            sanitize_html,
            bubble_full_width,
            line_breaks,
            layout,
            placeholder,
            examples,
            _retryable,
            _undoable,
            upload: (...args) => gradio.client.upload(...args),
            _fetch: (...args) => gradio.client.fetch(...args),
            load_component: gradio.load_component,
            msg_format: type,
            root: gradio.root
          },
          {},
          {}
        )}</div>`;
      }
    }
  )}`;
});

export { ChatBot$1 as BaseChatBot, Index as default };
//# sourceMappingURL=Index57-DdnxSGdp.js.map
