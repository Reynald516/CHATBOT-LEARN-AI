const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.DC4R8pax.js","app":"_app/immutable/entry/app.A3kyY2BB.js","imports":["_app/immutable/entry/start.DC4R8pax.js","_app/immutable/chunks/client.Do6qnxfb.js","_app/immutable/entry/app.A3kyY2BB.js","_app/immutable/chunks/preload-helper.DpQnamwV.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-B5V0ajga.js')),
			__memo(() => import('./chunks/1-fueTJ_0f.js')),
			__memo(() => import('./chunks/2-DMesThp_.js').then(function (n) { return n.aC; }))
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
