// -------------------
// Basic Babylon setup
// -------------------
const canvas = document.getElementById("renderCanvas");
const engine = new BABYLON.Engine(canvas, true, {preserveDrawingBuffer: true, stencil: true});
const scene = new BABYLON.Scene(engine);
scene.clearColor = new BABYLON.Color4(0.0, 0.0, 0.0, 1);

// Camera
const camera = new BABYLON.ArcRotateCamera(
  "cam",
  -Math.PI / 2,
  Math.PI / 2.5,
  3,
  BABYLON.Vector3.Zero(),
  scene
);
camera.attachControl(canvas, true);
camera.wheelDeltaPercentage = 0.01;

// Light
const light = new BABYLON.HemisphericLight("hlight", new BABYLON.Vector3(0, 1, 0), scene);
light.intensity = 0.9;

// Transparent Globe
const globe = BABYLON.MeshBuilder.CreateSphere("globe", { diameter: 2, segments: 64 }, scene);
const globeMat = new BABYLON.StandardMaterial("globeMat", scene);
globeMat.diffuseColor = new BABYLON.Color3(0.12, 0.15, 0.22);
globeMat.alpha = 0.7; // semi-transparent
globeMat.backFaceCulling = false;
globe.material = globeMat;
globe.receiveShadows = true;

  // // Glow effect (optional)
  // const gl = new BABYLON.GlowLayer("glow", scene);
  // gl.intensity = 0.6;

// Marker helper
function makeMarker(name, pos, colorHex = 0xff3333, radius = 0.03) {
  const mat = new BABYLON.StandardMaterial(name + "_mat", scene);
  const r = ((colorHex >> 16) & 255) / 255;
  const g = ((colorHex >> 8) & 255) / 255;
  const b = (colorHex & 255) / 255;
  mat.emissiveColor = new BABYLON.Color3(r, g, b);
  mat.specularColor = new BABYLON.Color3(0.2, 0.2, 0.2);

  const s = BABYLON.MeshBuilder.CreateSphere(name, { diameter: radius * 2, segments: 12 }, scene);
  s.material = mat;
  s.position = pos;
  return s;
}

// Tooltip
const tooltip = document.getElementById("tooltip");

// Load points from JSON
fetch(docPointsUrl)
  .then(r => {
    if (!r.ok) throw new Error("Failed to load doc_points.json. Serve files via HTTP.");
    return r.json();
  })
  .then(points => {
    const root = new BABYLON.TransformNode("markersRoot", scene);

    const markers = points.map((p, idx) => {
      // Normalize vector to sphere surface
      let vx = p.x, vy = p.y, vz = p.z;
      const len = Math.sqrt(vx * vx + vy * vy + vz * vz);
      if (len === 0) { vx = 1; vy = 0; vz = 0; }
      else { vx /= len; vy /= len; vz /= len; }

      const pos = new BABYLON.Vector3(vx * 1.02, vy * 1.02, vz * 1.02);

      // marker
      const marker = makeMarker("m" + idx, pos, 0x006400, 0.03);


      marker.metadata = { doc: p.doc };
      marker.parent = root;

      // line (vector) from origin to marker
      const line = BABYLON.MeshBuilder.CreateLines("line" + idx, {
        points: [BABYLON.Vector3.Zero(), pos]
      }, scene);
      line.color = new BABYLON.Color3(0.9, 0.3, 0.3);
      line.parent = root;
      line.thickness = 2;

      return marker;
    });




    // Hover interactivity
    let lastHovered = null;
    canvas.addEventListener("pointermove", (ev) => {
      const pick = scene.pick(scene.pointerX, scene.pointerY, mesh => mesh && mesh.metadata && mesh.metadata.doc);
      if (pick && pick.hit && pick.pickedMesh) {
        const m = pick.pickedMesh;
        if (m !== lastHovered) {
          lastHovered = m;
          tooltip.style.display = "block";
          tooltip.textContent = m.metadata.doc;
          m.scaling = new BABYLON.Vector3(1.6, 1.6, 1.6);
        }
        tooltip.style.left = ev.clientX + "px";
        tooltip.style.top = ev.clientY + "px";
      } else {
        if (lastHovered) lastHovered.scaling = BABYLON.Vector3.One();
        lastHovered = null;
        tooltip.style.display = "none";
      }
    });

    fetch(queryPointUrl)
  .then(r => {
    if (!r.ok) throw new Error("Failed to load query_point.json");
    return r.json();
  })
  .then(p => {
    // normalize vector
    let vx = p.x, vy = p.y, vz = p.z;
    const len = Math.sqrt(vx * vx + vy * vy + vz * vz);
    if (len === 0) { vx = 1; vy = 0; vz = 0; }
    else { vx /= len; vy /= len; vz /= len; }

    const pos = new BABYLON.Vector3(vx * 1.05, vy * 1.05, vz * 1.05);

    // red marker
    const qMarker = makeMarker("query", pos, 0xff0000, 0.05);
    qMarker.metadata = { doc: "QUERY" };

    // line for query
    const qLine = BABYLON.MeshBuilder.CreateLines("queryLine", {
      points: [BABYLON.Vector3.Zero(), pos]
    }, scene);
    qLine.color = new BABYLON.Color3(1, 0, 0); // bright red
    qLine.thickness = 3;
  })
  .catch(err => console.error(err));
    // // Click action
    // canvas.addEventListener("pointerdown", () => {
    //   const pick = scene.pick(scene.pointerX, scene.pointerY, mesh => mesh && mesh.metadata && mesh.metadata.doc);
    //   if (pick && pick.hit && pick.pickedMesh) {
    //     const docid = pick.pickedMesh.metadata.doc;
    //     console.log("Clicked:", docid);
    //     // Example: window.open("https://www.google.com/search?q=" + encodeURIComponent(docid), "_blank");
    //   }
    // });

    camera.setTarget(BABYLON.Vector3.Zero());
    camera.lowerRadiusLimit = 1.5;
    camera.upperRadiusLimit = 12;
  })
  .catch(err => { console.error(err); alert(err.message); });

// Resize
window.addEventListener("resize", () => { engine.resize(); });

// Loop
engine.runRenderLoop(() => {
  globe.rotation.y += 0.0008;
  scene.render();
});
