import { c as create_ssr_component, v as validate_component, e as escape } from './ssr-Cz1f32Mr.js';
import './2-B44WpJir.js';

const css = {
  code: "label.svelte-1b6s6s{display:inline-flex;align-items:center;z-index:var(--layer-2);box-shadow:var(--block-label-shadow);border:var(--block-label-border-width) solid var(--border-color-primary);border-top:none;border-left:none;border-radius:var(--block-label-radius);background:var(--block-label-background-fill);padding:var(--block-label-padding);pointer-events:none;color:var(--block-label-text-color);font-weight:var(--block-label-text-weight);font-size:var(--block-label-text-size);line-height:var(--line-sm)}.gr-group label.svelte-1b6s6s{border-top-left-radius:0}label.float.svelte-1b6s6s{position:absolute;top:var(--block-label-margin);left:var(--block-label-margin)}label.svelte-1b6s6s:not(.float){position:static;margin-top:var(--block-label-margin);margin-left:var(--block-label-margin)}.hide.svelte-1b6s6s{height:0}span.svelte-1b6s6s{opacity:0.8;margin-right:var(--size-2);width:calc(var(--block-label-text-size) - 1px);height:calc(var(--block-label-text-size) - 1px)}.hide-label.svelte-1b6s6s{box-shadow:none;border-width:0;background:transparent;overflow:visible}",
  map: '{"version":3,"file":"BlockLabel.svelte","sources":["BlockLabel.svelte"],"sourcesContent":["<script lang=\\"ts\\">export let label = null;\\nexport let Icon;\\nexport let show_label = true;\\nexport let disable = false;\\nexport let float = true;\\n<\/script>\\n\\n<label\\n\\tfor=\\"\\"\\n\\tclass:hide={!show_label}\\n\\tclass:sr-only={!show_label}\\n\\tclass:float\\n\\tclass:hide-label={disable}\\n\\tdata-testid=\\"block-label\\"\\n>\\n\\t<span>\\n\\t\\t<Icon />\\n\\t</span>\\n\\t{label}\\n</label>\\n\\n<style>\\n\\tlabel {\\n\\t\\tdisplay: inline-flex;\\n\\t\\talign-items: center;\\n\\t\\tz-index: var(--layer-2);\\n\\t\\tbox-shadow: var(--block-label-shadow);\\n\\t\\tborder: var(--block-label-border-width) solid var(--border-color-primary);\\n\\t\\tborder-top: none;\\n\\t\\tborder-left: none;\\n\\t\\tborder-radius: var(--block-label-radius);\\n\\t\\tbackground: var(--block-label-background-fill);\\n\\t\\tpadding: var(--block-label-padding);\\n\\t\\tpointer-events: none;\\n\\t\\tcolor: var(--block-label-text-color);\\n\\t\\tfont-weight: var(--block-label-text-weight);\\n\\t\\tfont-size: var(--block-label-text-size);\\n\\t\\tline-height: var(--line-sm);\\n\\t}\\n\\t:global(.gr-group) label {\\n\\t\\tborder-top-left-radius: 0;\\n\\t}\\n\\n\\tlabel.float {\\n\\t\\tposition: absolute;\\n\\t\\ttop: var(--block-label-margin);\\n\\t\\tleft: var(--block-label-margin);\\n\\t}\\n\\tlabel:not(.float) {\\n\\t\\tposition: static;\\n\\t\\tmargin-top: var(--block-label-margin);\\n\\t\\tmargin-left: var(--block-label-margin);\\n\\t}\\n\\n\\t.hide {\\n\\t\\theight: 0;\\n\\t}\\n\\n\\tspan {\\n\\t\\topacity: 0.8;\\n\\t\\tmargin-right: var(--size-2);\\n\\t\\twidth: calc(var(--block-label-text-size) - 1px);\\n\\t\\theight: calc(var(--block-label-text-size) - 1px);\\n\\t}\\n\\t.hide-label {\\n\\t\\tbox-shadow: none;\\n\\t\\tborder-width: 0;\\n\\t\\tbackground: transparent;\\n\\t\\toverflow: visible;\\n\\t}</style>\\n"],"names":[],"mappings":"AAsBC,mBAAM,CACL,OAAO,CAAE,WAAW,CACpB,WAAW,CAAE,MAAM,CACnB,OAAO,CAAE,IAAI,SAAS,CAAC,CACvB,UAAU,CAAE,IAAI,oBAAoB,CAAC,CACrC,MAAM,CAAE,IAAI,0BAA0B,CAAC,CAAC,KAAK,CAAC,IAAI,sBAAsB,CAAC,CACzE,UAAU,CAAE,IAAI,CAChB,WAAW,CAAE,IAAI,CACjB,aAAa,CAAE,IAAI,oBAAoB,CAAC,CACxC,UAAU,CAAE,IAAI,6BAA6B,CAAC,CAC9C,OAAO,CAAE,IAAI,qBAAqB,CAAC,CACnC,cAAc,CAAE,IAAI,CACpB,KAAK,CAAE,IAAI,wBAAwB,CAAC,CACpC,WAAW,CAAE,IAAI,yBAAyB,CAAC,CAC3C,SAAS,CAAE,IAAI,uBAAuB,CAAC,CACvC,WAAW,CAAE,IAAI,SAAS,CAC3B,CACQ,SAAU,CAAC,mBAAM,CACxB,sBAAsB,CAAE,CACzB,CAEA,KAAK,oBAAO,CACX,QAAQ,CAAE,QAAQ,CAClB,GAAG,CAAE,IAAI,oBAAoB,CAAC,CAC9B,IAAI,CAAE,IAAI,oBAAoB,CAC/B,CACA,mBAAK,KAAK,MAAM,CAAE,CACjB,QAAQ,CAAE,MAAM,CAChB,UAAU,CAAE,IAAI,oBAAoB,CAAC,CACrC,WAAW,CAAE,IAAI,oBAAoB,CACtC,CAEA,mBAAM,CACL,MAAM,CAAE,CACT,CAEA,kBAAK,CACJ,OAAO,CAAE,GAAG,CACZ,YAAY,CAAE,IAAI,QAAQ,CAAC,CAC3B,KAAK,CAAE,KAAK,IAAI,uBAAuB,CAAC,CAAC,CAAC,CAAC,GAAG,CAAC,CAC/C,MAAM,CAAE,KAAK,IAAI,uBAAuB,CAAC,CAAC,CAAC,CAAC,GAAG,CAChD,CACA,yBAAY,CACX,UAAU,CAAE,IAAI,CAChB,YAAY,CAAE,CAAC,CACf,UAAU,CAAE,WAAW,CACvB,QAAQ,CAAE,OACX"}'
};
const BlockLabel = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { label = null } = $$props;
  let { Icon } = $$props;
  let { show_label = true } = $$props;
  let { disable = false } = $$props;
  let { float = true } = $$props;
  if ($$props.label === void 0 && $$bindings.label && label !== void 0)
    $$bindings.label(label);
  if ($$props.Icon === void 0 && $$bindings.Icon && Icon !== void 0)
    $$bindings.Icon(Icon);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.disable === void 0 && $$bindings.disable && disable !== void 0)
    $$bindings.disable(disable);
  if ($$props.float === void 0 && $$bindings.float && float !== void 0)
    $$bindings.float(float);
  $$result.css.add(css);
  return `<label for="" data-testid="block-label" class="${[
    "svelte-1b6s6s",
    (!show_label ? "hide" : "") + " " + (!show_label ? "sr-only" : "") + " " + (float ? "float" : "") + " " + (disable ? "hide-label" : "")
  ].join(" ").trim()}"><span class="svelte-1b6s6s">${validate_component(Icon, "Icon").$$render($$result, {}, {}, {})}</span> ${escape(label)} </label>`;
});

export { BlockLabel as B };
//# sourceMappingURL=BlockLabel-BHjb1jyn.js.map
