const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png"]),
	mimeTypes: {".png":"image/png"},
	_: {
		client: {"start":"_app/immutable/entry/start.BkBfHsbt.js","app":"_app/immutable/entry/app.CIXoW2uc.js","imports":["_app/immutable/entry/start.BkBfHsbt.js","_app/immutable/chunks/entry.C_fLXhM2.js","_app/immutable/chunks/scheduler.C_sdfy-5.js","_app/immutable/entry/app.CIXoW2uc.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/scheduler.C_sdfy-5.js","_app/immutable/chunks/index.D_Dnc2IG.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-B1LVse0E.js')),
			__memo(() => import('./chunks/1-CXf0hi9g.js')),
			__memo(() => import('./chunks/2-B44WpJir.js').then(function (n) { return n._; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
