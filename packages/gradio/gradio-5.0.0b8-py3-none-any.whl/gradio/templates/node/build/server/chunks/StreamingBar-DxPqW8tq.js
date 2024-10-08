import { c as create_ssr_component, d as add_styles } from './ssr-Cz1f32Mr.js';
import './2-B44WpJir.js';

const css = {
  code: ".streaming-bar.svelte-roz8lq{position:absolute;bottom:0;left:0;right:0;height:4px;background-color:var(--primary-600);animation:svelte-roz8lq-countdown linear forwards;z-index:1}@keyframes svelte-roz8lq-countdown{from{transform:translateX(0%)}to{transform:translateX(-100%)}}",
  map: '{"version":3,"file":"StreamingBar.svelte","sources":["StreamingBar.svelte"],"sourcesContent":["<script lang=\\"ts\\">export let time_limit;\\n<\/script>\\n\\n{#if time_limit}\\n\\t<div class=\\"streaming-bar\\" style:animation-duration=\\"{time_limit}s\\"></div>\\n{/if}\\n\\n<style>\\n\\t.streaming-bar {\\n\\t\\tposition: absolute;\\n\\t\\tbottom: 0;\\n\\t\\tleft: 0;\\n\\t\\tright: 0;\\n\\t\\theight: 4px;\\n\\t\\tbackground-color: var(--primary-600);\\n\\t\\tanimation: countdown linear forwards;\\n\\t\\tz-index: 1;\\n\\t}\\n\\n\\t@keyframes countdown {\\n\\t\\tfrom {\\n\\t\\t\\ttransform: translateX(0%);\\n\\t\\t}\\n\\t\\tto {\\n\\t\\t\\ttransform: translateX(-100%);\\n\\t\\t}\\n\\t}</style>\\n"],"names":[],"mappings":"AAQC,4BAAe,CACd,QAAQ,CAAE,QAAQ,CAClB,MAAM,CAAE,CAAC,CACT,IAAI,CAAE,CAAC,CACP,KAAK,CAAE,CAAC,CACR,MAAM,CAAE,GAAG,CACX,gBAAgB,CAAE,IAAI,aAAa,CAAC,CACpC,SAAS,CAAE,uBAAS,CAAC,MAAM,CAAC,QAAQ,CACpC,OAAO,CAAE,CACV,CAEA,WAAW,uBAAU,CACpB,IAAK,CACJ,SAAS,CAAE,WAAW,EAAE,CACzB,CACA,EAAG,CACF,SAAS,CAAE,WAAW,KAAK,CAC5B,CACD"}'
};
const StreamingBar = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { time_limit } = $$props;
  if ($$props.time_limit === void 0 && $$bindings.time_limit && time_limit !== void 0)
    $$bindings.time_limit(time_limit);
  $$result.css.add(css);
  return `${time_limit ? `<div class="streaming-bar svelte-roz8lq"${add_styles({ "animation-duration": `${time_limit}s` })}></div>` : ``}`;
});

export { StreamingBar as S };
//# sourceMappingURL=StreamingBar-DxPqW8tq.js.map
