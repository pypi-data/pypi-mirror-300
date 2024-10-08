import { c as create_ssr_component, b as add_attribute, e as escape } from './ssr-Cz1f32Mr.js';

/* empty css                                      */
const css = {
  code: ".gallery.svelte-1viwdyg{padding:var(--size-1) var(--size-2)}div.svelte-1viwdyg{overflow:hidden;min-width:var(--local-text-width);white-space:nowrap}",
  map: '{"version":3,"file":"Example.svelte","sources":["Example.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { onMount } from \\"svelte\\";\\nexport let value;\\nexport let type;\\nexport let selected = false;\\nlet size;\\nlet el;\\nfunction set_styles(element, el_width) {\\n    if (!element || !el_width)\\n        return;\\n    el.style.setProperty(\\"--local-text-width\\", `${el_width < 150 ? el_width : 200}px`);\\n    el.style.whiteSpace = \\"unset\\";\\n}\\nonMount(() => {\\n    set_styles(el, size);\\n});\\n<\/script>\\n\\n<div\\n\\tbind:clientWidth={size}\\n\\tbind:this={el}\\n\\tclass:table={type === \\"table\\"}\\n\\tclass:gallery={type === \\"gallery\\"}\\n\\tclass:selected\\n>\\n\\t{value ? value : \\"\\"}\\n</div>\\n\\n<style>\\n\\t.gallery {\\n\\t\\tpadding: var(--size-1) var(--size-2);\\n\\t}\\n\\n\\tdiv {\\n\\t\\toverflow: hidden;\\n\\t\\tmin-width: var(--local-text-width);\\n\\n\\t\\twhite-space: nowrap;\\n\\t}</style>\\n"],"names":[],"mappings":"AA4BC,uBAAS,CACR,OAAO,CAAE,IAAI,QAAQ,CAAC,CAAC,IAAI,QAAQ,CACpC,CAEA,kBAAI,CACH,QAAQ,CAAE,MAAM,CAChB,SAAS,CAAE,IAAI,kBAAkB,CAAC,CAElC,WAAW,CAAE,MACd"}'
};
const Example = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  let { type } = $$props;
  let { selected = false } = $$props;
  let el;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.selected === void 0 && $$bindings.selected && selected !== void 0)
    $$bindings.selected(selected);
  $$result.css.add(css);
  return `<div class="${[
    "svelte-1viwdyg",
    (type === "table" ? "table" : "") + " " + (type === "gallery" ? "gallery" : "") + " " + (selected ? "selected" : "")
  ].join(" ").trim()}"${add_attribute("this", el, 0)}>${escape(value ? value : "")} </div>`;
});

export { Example as default };
//# sourceMappingURL=Example2-BI1FX5Tw.js.map
