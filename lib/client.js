window.__ModuleLoader__.load({
	id: "@dsh-external/dsh-skill-vault",
	factory: (require) => {
		var module = { exports: {} };
		var exports = module.exports;
		Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
		//#region src/client/index.ts
		const inject = ["slots"];
		function apply(ctx) {
			ctx.effect(() => ctx.slots.inject("conversation.view", () => ctx.slots.register({
				name: "conversation.view",
				id: "@dsh-external/dsh-skill-vault-panel",
				label: () => "技能库",
				component: () => ({ render() {
					const root = document.createElement("div");
					root.style.padding = "12px";
					root.style.fontFamily = "ui-sans-serif, system-ui, sans-serif";
					root.style.maxHeight = "420px";
					root.style.overflowY = "auto";
					const header = document.createElement("div");
					header.textContent = "🧰 dsh-skill-vault 技能开关";
					header.style.fontWeight = "600";
					header.style.marginBottom = "8px";
					root.appendChild(header);
					const status = document.createElement("div");
					status.textContent = "加载中…";
					status.style.color = "#888";
					root.appendChild(status);
					const list = document.createElement("div");
					list.style.display = "grid";
					list.style.gap = "6px";
					root.appendChild(list);
					const refresh = async () => {
						try {
							const data = await (await fetch("/skill-vault/api/list")).json();
							status.textContent = `${data.entries.length} 个 skill · ${data.scenarios.length} 个场景`;
							list.innerHTML = "";
							for (const scenario of data.scenarios) {
								const group = document.createElement("div");
								group.style.border = "1px solid #ddd";
								group.style.borderRadius = "8px";
								group.style.padding = "8px";
								group.style.background = "#fafafa";
								const groupHeader = document.createElement("div");
								groupHeader.style.display = "flex";
								groupHeader.style.alignItems = "center";
								groupHeader.style.justifyContent = "space-between";
								groupHeader.style.marginBottom = "4px";
								const titleEl = document.createElement("span");
								titleEl.textContent = `${scenario.title} (${scenario.enabledCount}/${scenario.skillCount})`;
								titleEl.style.fontWeight = "600";
								const groupToggle = document.createElement("button");
								groupToggle.textContent = scenario.enabledCount === scenario.skillCount ? "全部关" : "全部开";
								groupToggle.style.fontSize = "12px";
								groupToggle.addEventListener("click", async () => {
									const on = scenario.enabledCount !== scenario.skillCount;
									await fetch("/skill-vault/api/" + (on ? "enable" : "disable"), {
										method: "POST",
										headers: { "content-type": "application/json" },
										body: JSON.stringify({
											target: scenario.id,
											scope: "global"
										})
									});
									await refresh();
								});
								groupHeader.append(titleEl, groupToggle);
								group.appendChild(groupHeader);
								const rows = data.entries.filter((r) => r.scenario === scenario.id);
								for (const row of rows) {
									const line = document.createElement("div");
									line.style.display = "flex";
									line.style.alignItems = "center";
									line.style.gap = "6px";
									line.style.padding = "2px 0";
									const toggle = document.createElement("input");
									toggle.type = "checkbox";
									toggle.checked = row.enabled;
									toggle.addEventListener("change", async () => {
										await fetch("/skill-vault/api/" + (toggle.checked ? "enable" : "disable"), {
											method: "POST",
											headers: { "content-type": "application/json" },
											body: JSON.stringify({
												target: row.id,
												scope: "global"
											})
										});
										await refresh();
									});
									const label = document.createElement("label");
									label.style.cursor = "pointer";
									label.style.flex = "1";
									const title = document.createElement("span");
									title.textContent = row.title;
									title.style.fontWeight = "500";
									const desc = document.createElement("div");
									desc.textContent = row.description;
									desc.style.color = "#777";
									desc.style.fontSize = "12px";
									label.append(title, desc);
									line.append(toggle, label);
									group.appendChild(line);
								}
								list.appendChild(group);
							}
						} catch (e) {
							status.textContent = "加载失败：" + String(e);
						}
					};
					refresh();
					return root;
				} })
			})), "@dsh-external/dsh-skill-vault: panel");
		}
		//#endregion
		exports.apply = apply;
		exports.inject = inject;
		return module.exports;
	}
});

//# sourceMappingURL=client.js.map