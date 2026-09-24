/* Local map annotation only: no persistence, filtering or network actions. */
class PolygonDrawControl {
  constructor(map, button, hint) {
    this.map = map; this.button = button; this.hint = hint;
    this.active = false; this.points = []; this.polygons = []; this.preview = null;
    this.button.addEventListener("click", () => this.active ? this.cancel() : this.start());
    map.on("style.load", () => { this.render(); button.disabled = false; });
    map.on("click", event => this.click(event));
    map.on("mousemove", event => { if (this.active) { this.preview = [event.lngLat.lng,event.lngLat.lat]; this.render(); } });
    document.addEventListener("keydown", event => { if (event.key === "Escape" && this.active) { this.cancel(); event.preventDefault(); } });
  }
  start() {
    this.active = true; this.points = []; this.preview = null;
    this.zoomWasEnabled = this.map.doubleClickZoom.isEnabled();
    this.map.doubleClickZoom.disable(); this.updateUi(); this.render();
  }
  cancel() { this.points = []; this.preview = null; this.finish(); }
  finish() {
    this.active = false;
    if (this.zoomWasEnabled) this.map.doubleClickZoom.enable();
    this.updateUi(); this.render();
  }
  updateUi() {
    this.button.setAttribute("aria-pressed", String(this.active));
    this.hint.hidden = !this.active;
    this.map.getContainer().classList.toggle("polygon-drawing", this.active);
    this.map.getCanvas().style.cursor = this.active ? "crosshair" : "";
  }
  click(event) {
    if (!this.active) return;
    event.originalEvent?.preventDefault();
    const point = [event.lngLat.lng,event.lngLat.lat];
    const near = p => { const pixel = this.map.project(p); return Math.hypot(pixel.x-event.point.x,pixel.y-event.point.y) <= 12; };
    if (this.points.length >= 3 && near(this.points[0])) {
      this.polygons.push([...this.points.map(p => [...p]), [...this.points[0]]]);
      this.points = []; this.preview = null; this.finish(); return;
    }
    if (this.points.some(near)) return;
    this.points.push(point); this.preview = null; this.render();
  }
  data() {
    const feature = (type,coordinates,properties={}) => ({type:"Feature",properties,geometry:{type,coordinates}});
    const features = this.polygons.map(ring => feature("Polygon",[ring]));
    const line = this.preview ? [...this.points,this.preview] : this.points;
    if (line.length >= 2) features.push(feature("LineString",line));
    this.points.forEach((p,i) => features.push(feature("Point",p,{first:i===0})));
    return {type:"FeatureCollection",features};
  }
  render() {
    const source = this.map.getSource("draw-polygon");
    if (source) { source.setData(this.data()); return; }
    if (!this.map.isStyleLoaded()) return;
    this.map.addSource("draw-polygon",{type:"geojson",data:this.data()});
    this.map.addLayer({id:"draw-polygon-fill",type:"fill",source:"draw-polygon",filter:["==","$type","Polygon"],paint:{"fill-color":"#72c9ff","fill-opacity":0.18}});
    this.map.addLayer({id:"draw-polygon-line",type:"line",source:"draw-polygon",filter:["!=","$type","Point"],paint:{"line-color":"#9adaff","line-width":2}});
    this.map.addLayer({id:"draw-polygon-points",type:"circle",source:"draw-polygon",filter:["==","$type","Point"],paint:{"circle-radius":["case",["get","first"],7,4],"circle-color":"#132636","circle-stroke-color":"#9adaff","circle-stroke-width":2}});
  }
}
if (typeof module !== "undefined") module.exports = PolygonDrawControl;
