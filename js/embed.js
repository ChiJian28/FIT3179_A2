const version = "31";
const specs = [
  ["#national-bars", "specs/national_bars.vg.json"],
  ["#decade-brush", "specs/decade_brush.vg.json"],
  ["#choropleth", "specs/choropleth.vg.json"],
  ["#bullets", "specs/bullets.vg.json"],
  ["#slope-states", "specs/slope_states.vg.json"],
  ["#symbol-map", "specs/symbol_map.vg.json"],
  ["#cartogram", "specs/cartogram.vg.json"],
  ["#heatmap", "specs/heatmap.vg.json"],
  ["#hours-ratio", "specs/hours_ratio.vg.json"],
  ["#distance", "specs/distance.vg.json"],
  ["#sunburst", "specs/sunburst.vg.json"],
  ["#activity-counts", "specs/activity_counts.vg.json"],
  ["#slope-activity", "specs/slope_activity.vg.json"],
  ["#isotype", "specs/isotype.vg.json"],
  ["#sex-share", "specs/sex_share.vg.json"],
];

async function renderAll() {
  if (document.fonts && document.fonts.ready) {
    try {
      await document.fonts.ready;
    } catch (_) {}
  }
  for (const [el, spec] of specs) {
    vegaEmbed(el, spec + "?v=" + version, { actions: false, renderer: "svg" })
      .then((res) => {
        const container = document.querySelector(el);
        if (container) {
          for (const form of container.querySelectorAll(".vega-bindings")) {
            if (!form.children || form.children.length === 0) {
              form.remove();
            }
          }
        }
        return res;
      })
      .catch((error) => {
        console.error(spec, error);
      });
  }
}

renderAll();
