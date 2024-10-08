import { c as create_ssr_component, v as validate_component, e as escape } from './ssr-Cz1f32Mr.js';
import './2-B44WpJir.js';
import { I as ImagePaste, U as Upload } from './Upload2-CQQNjaMs.js';

const RE_HEADING = /^(#\s*)(.+)$/m;
function inject(text) {
  const trimmed_text = text.trim();
  const heading_match = trimmed_text.match(RE_HEADING);
  if (!heading_match) {
    return [false, trimmed_text || false];
  }
  const [full_match, , heading_content] = heading_match;
  const _heading = heading_content.trim();
  if (trimmed_text === full_match) {
    return [_heading, false];
  }
  const heading_end_index = heading_match.index !== void 0 ? heading_match.index + full_match.length : 0;
  const remaining_text = trimmed_text.substring(heading_end_index).trim();
  const _paragraph = remaining_text || false;
  return [_heading, _paragraph];
}
const css = {
  code: "h2.svelte-12ioyct{font-size:var(--text-xl) !important}p.svelte-12ioyct,h2.svelte-12ioyct{white-space:pre-line}.wrap.svelte-12ioyct{display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:var(--size-60);color:var(--block-label-text-color);line-height:var(--line-md);height:100%;padding-top:var(--size-3);text-align:center;margin:auto var(--spacing-lg)}.or.svelte-12ioyct{color:var(--body-text-color-subdued);display:flex}.icon-wrap.svelte-12ioyct{width:30px;margin-bottom:var(--spacing-lg)}@media(min-width: 768px){.wrap.svelte-12ioyct{font-size:var(--text-lg)}}.hovered.svelte-12ioyct{color:var(--color-accent)}",
  map: '{"version":3,"file":"UploadText.svelte","sources":["UploadText.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { Upload as UploadIcon, ImagePaste } from \\"@gradio/icons\\";\\nimport { inject } from \\"./utils/parse_placeholder\\";\\nexport let type = \\"file\\";\\nexport let i18n;\\nexport let message = void 0;\\nexport let mode = \\"full\\";\\nexport let hovered = false;\\nexport let placeholder = void 0;\\nconst defs = {\\n    image: \\"upload_text.drop_image\\",\\n    video: \\"upload_text.drop_video\\",\\n    audio: \\"upload_text.drop_audio\\",\\n    file: \\"upload_text.drop_file\\",\\n    csv: \\"upload_text.drop_csv\\",\\n    gallery: \\"upload_text.drop_gallery\\",\\n    clipboard: \\"upload_text.paste_clipboard\\"\\n};\\n$: [heading, paragraph] = placeholder ? inject(placeholder) : [false, false];\\n<\/script>\\n\\n<div class=\\"wrap\\">\\n\\t<span class=\\"icon-wrap\\" class:hovered>\\n\\t\\t{#if type === \\"clipboard\\"}\\n\\t\\t\\t<ImagePaste />\\n\\t\\t{:else}\\n\\t\\t\\t<UploadIcon />\\n\\t\\t{/if}\\n\\t</span>\\n\\n\\t{#if heading || paragraph}\\n\\t\\t{#if heading}\\n\\t\\t\\t<h2>{heading}</h2>\\n\\t\\t{/if}\\n\\t\\t{#if paragraph}\\n\\t\\t\\t<p>{paragraph}</p>\\n\\t\\t{/if}\\n\\t{:else}\\n\\t\\t{i18n(defs[type] || defs.file)}\\n\\n\\t\\t{#if mode !== \\"short\\"}\\n\\t\\t\\t<span class=\\"or\\">- {i18n(\\"common.or\\")} -</span>\\n\\t\\t\\t{message || i18n(\\"upload_text.click_to_upload\\")}\\n\\t\\t{/if}\\n\\t{/if}\\n</div>\\n\\n<style>\\n\\th2 {\\n\\t\\tfont-size: var(--text-xl) !important;\\n\\t}\\n\\n\\tp,\\n\\th2 {\\n\\t\\twhite-space: pre-line;\\n\\t}\\n\\n\\t.wrap {\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\tjustify-content: center;\\n\\t\\talign-items: center;\\n\\t\\tmin-height: var(--size-60);\\n\\t\\tcolor: var(--block-label-text-color);\\n\\t\\tline-height: var(--line-md);\\n\\t\\theight: 100%;\\n\\t\\tpadding-top: var(--size-3);\\n\\t\\ttext-align: center;\\n\\t\\tmargin: auto var(--spacing-lg);\\n\\t}\\n\\n\\t.or {\\n\\t\\tcolor: var(--body-text-color-subdued);\\n\\t\\tdisplay: flex;\\n\\t}\\n\\n\\t.icon-wrap {\\n\\t\\twidth: 30px;\\n\\t\\tmargin-bottom: var(--spacing-lg);\\n\\t}\\n\\n\\t@media (min-width: 768px) {\\n\\t\\t.wrap {\\n\\t\\t\\tfont-size: var(--text-lg);\\n\\t\\t}\\n\\t}\\n\\n\\t.hovered {\\n\\t\\tcolor: var(--color-accent);\\n\\t}</style>\\n"],"names":[],"mappings":"AA+CC,iBAAG,CACF,SAAS,CAAE,IAAI,SAAS,CAAC,CAAC,UAC3B,CAEA,gBAAC,CACD,iBAAG,CACF,WAAW,CAAE,QACd,CAEA,oBAAM,CACL,OAAO,CAAE,IAAI,CACb,cAAc,CAAE,MAAM,CACtB,eAAe,CAAE,MAAM,CACvB,WAAW,CAAE,MAAM,CACnB,UAAU,CAAE,IAAI,SAAS,CAAC,CAC1B,KAAK,CAAE,IAAI,wBAAwB,CAAC,CACpC,WAAW,CAAE,IAAI,SAAS,CAAC,CAC3B,MAAM,CAAE,IAAI,CACZ,WAAW,CAAE,IAAI,QAAQ,CAAC,CAC1B,UAAU,CAAE,MAAM,CAClB,MAAM,CAAE,IAAI,CAAC,IAAI,YAAY,CAC9B,CAEA,kBAAI,CACH,KAAK,CAAE,IAAI,yBAAyB,CAAC,CACrC,OAAO,CAAE,IACV,CAEA,yBAAW,CACV,KAAK,CAAE,IAAI,CACX,aAAa,CAAE,IAAI,YAAY,CAChC,CAEA,MAAO,YAAY,KAAK,CAAE,CACzB,oBAAM,CACL,SAAS,CAAE,IAAI,SAAS,CACzB,CACD,CAEA,uBAAS,CACR,KAAK,CAAE,IAAI,cAAc,CAC1B"}'
};
const UploadText = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let heading;
  let paragraph;
  let { type = "file" } = $$props;
  let { i18n } = $$props;
  let { message = void 0 } = $$props;
  let { mode = "full" } = $$props;
  let { hovered = false } = $$props;
  let { placeholder = void 0 } = $$props;
  const defs = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.i18n === void 0 && $$bindings.i18n && i18n !== void 0)
    $$bindings.i18n(i18n);
  if ($$props.message === void 0 && $$bindings.message && message !== void 0)
    $$bindings.message(message);
  if ($$props.mode === void 0 && $$bindings.mode && mode !== void 0)
    $$bindings.mode(mode);
  if ($$props.hovered === void 0 && $$bindings.hovered && hovered !== void 0)
    $$bindings.hovered(hovered);
  if ($$props.placeholder === void 0 && $$bindings.placeholder && placeholder !== void 0)
    $$bindings.placeholder(placeholder);
  $$result.css.add(css);
  [heading, paragraph] = placeholder ? inject(placeholder) : [false, false];
  return `<div class="wrap svelte-12ioyct"><span class="${["icon-wrap svelte-12ioyct", hovered ? "hovered" : ""].join(" ").trim()}">${type === "clipboard" ? `${validate_component(ImagePaste, "ImagePaste").$$render($$result, {}, {}, {})}` : `${validate_component(Upload, "UploadIcon").$$render($$result, {}, {}, {})}`}</span> ${heading || paragraph ? `${heading ? `<h2 class="svelte-12ioyct">${escape(heading)}</h2>` : ``} ${paragraph ? `<p class="svelte-12ioyct">${escape(paragraph)}</p>` : ``}` : `${escape(i18n(defs[type] || defs.file))} ${mode !== "short" ? `<span class="or svelte-12ioyct">- ${escape(i18n("common.or"))} -</span> ${escape(message || i18n("upload_text.click_to_upload"))}` : ``}`} </div>`;
});

export { UploadText as U };
//# sourceMappingURL=UploadText-BJefVQ_A.js.map
