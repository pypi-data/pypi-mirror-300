import { c as create_ssr_component, b as add_attribute } from './ssr-Cz1f32Mr.js';
import './2-B44WpJir.js';

const css = {
  code: ".empty.svelte-1oiin9d{display:flex;justify-content:center;align-items:center;margin-top:calc(0px - var(--size-6));height:var(--size-full)}.icon.svelte-1oiin9d{opacity:0.5;height:var(--size-5);color:var(--body-text-color)}.small.svelte-1oiin9d{min-height:calc(var(--size-32) - 20px)}.large.svelte-1oiin9d{min-height:calc(var(--size-64) - 20px)}.unpadded_box.svelte-1oiin9d{margin-top:0}.small_parent.svelte-1oiin9d{min-height:100% !important}",
  map: '{"version":3,"file":"Empty.svelte","sources":["Empty.svelte"],"sourcesContent":["<script lang=\\"ts\\">export let size = \\"small\\";\\nexport let unpadded_box = false;\\nlet el;\\n$: parent_height = compare_el_to_parent(el);\\nfunction compare_el_to_parent(el2) {\\n    if (!el2)\\n        return false;\\n    const { height: el_height } = el2.getBoundingClientRect();\\n    const { height: parent_height2 } = el2.parentElement?.getBoundingClientRect() || { height: el_height };\\n    return el_height > parent_height2 + 2;\\n}\\n<\/script>\\n\\n<div\\n\\tclass=\\"empty\\"\\n\\tclass:small={size === \\"small\\"}\\n\\tclass:large={size === \\"large\\"}\\n\\tclass:unpadded_box\\n\\tbind:this={el}\\n\\tclass:small_parent={parent_height}\\n\\taria-label=\\"Empty value\\"\\n>\\n\\t<div class=\\"icon\\">\\n\\t\\t<slot />\\n\\t</div>\\n</div>\\n\\n<style>\\n\\t.empty {\\n\\t\\tdisplay: flex;\\n\\t\\tjustify-content: center;\\n\\t\\talign-items: center;\\n\\t\\tmargin-top: calc(0px - var(--size-6));\\n\\t\\theight: var(--size-full);\\n\\t}\\n\\n\\t.icon {\\n\\t\\topacity: 0.5;\\n\\t\\theight: var(--size-5);\\n\\t\\tcolor: var(--body-text-color);\\n\\t}\\n\\n\\t.small {\\n\\t\\tmin-height: calc(var(--size-32) - 20px);\\n\\t}\\n\\n\\t.large {\\n\\t\\tmin-height: calc(var(--size-64) - 20px);\\n\\t}\\n\\n\\t.unpadded_box {\\n\\t\\tmargin-top: 0;\\n\\t}\\n\\n\\t.small_parent {\\n\\t\\tmin-height: 100% !important;\\n\\t}</style>\\n"],"names":[],"mappings":"AA4BC,qBAAO,CACN,OAAO,CAAE,IAAI,CACb,eAAe,CAAE,MAAM,CACvB,WAAW,CAAE,MAAM,CACnB,UAAU,CAAE,KAAK,GAAG,CAAC,CAAC,CAAC,IAAI,QAAQ,CAAC,CAAC,CACrC,MAAM,CAAE,IAAI,WAAW,CACxB,CAEA,oBAAM,CACL,OAAO,CAAE,GAAG,CACZ,MAAM,CAAE,IAAI,QAAQ,CAAC,CACrB,KAAK,CAAE,IAAI,iBAAiB,CAC7B,CAEA,qBAAO,CACN,UAAU,CAAE,KAAK,IAAI,SAAS,CAAC,CAAC,CAAC,CAAC,IAAI,CACvC,CAEA,qBAAO,CACN,UAAU,CAAE,KAAK,IAAI,SAAS,CAAC,CAAC,CAAC,CAAC,IAAI,CACvC,CAEA,4BAAc,CACb,UAAU,CAAE,CACb,CAEA,4BAAc,CACb,UAAU,CAAE,IAAI,CAAC,UAClB"}'
};
function compare_el_to_parent(el2) {
  return false;
}
const Empty = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let parent_height;
  let { size = "small" } = $$props;
  let { unpadded_box = false } = $$props;
  let el;
  if ($$props.size === void 0 && $$bindings.size && size !== void 0)
    $$bindings.size(size);
  if ($$props.unpadded_box === void 0 && $$bindings.unpadded_box && unpadded_box !== void 0)
    $$bindings.unpadded_box(unpadded_box);
  $$result.css.add(css);
  parent_height = compare_el_to_parent();
  return `<div class="${[
    "empty svelte-1oiin9d",
    (size === "small" ? "small" : "") + " " + (size === "large" ? "large" : "") + " " + (unpadded_box ? "unpadded_box" : "") + " " + (parent_height ? "small_parent" : "")
  ].join(" ").trim()}" aria-label="Empty value"${add_attribute("this", el, 0)}><div class="icon svelte-1oiin9d">${slots.default ? slots.default({}) : ``}</div> </div>`;
});

export { Empty as E };
//# sourceMappingURL=Empty-3_kIXlIW.js.map
