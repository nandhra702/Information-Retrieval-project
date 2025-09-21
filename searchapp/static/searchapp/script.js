// -------------------
// Basic BabylonJS setup
// -------------------
const canvas = document.getElementById("renderCanvas");
const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
const scene = new BABYLON.Scene(engine);
scene.clearColor = new BABYLON.Color4(0, 0, 0, 1);

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

// Globe
const globe = BABYLON.MeshBuilder.CreateSphere("globe", { diameter: 2, segments: 64 }, scene);
const globeMat = new BABYLON.StandardMaterial("globeMat", scene);
globeMat.diffuseColor = new BABYLON.Color3(0.12, 0.15, 0.22);
globeMat.alpha = 0.7;
globeMat.backFaceCulling = false;
globe.material = globeMat;

// -------------------
// Helper to create markers
// -------------------
function makeMarker(name, pos, colorHex = 0x0000ff, radius = 0.03) {
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

// -------------------
// Load document points and render
// -------------------
function loadDocPoints() {
    fetch(docPointsUrl + "?t=" + Date.now()) // cache-busting
        .then(res => {
            if (!res.ok) throw new Error("Failed to load doc_points.json");
            return res.json();
        })
        .then(points => {
            console.log("Loaded doc_points.json:", points);
            if (!points || points.length === 0) {
                console.warn("No document points to render.");
                return;
            }

            const markersRoot = new BABYLON.TransformNode("markersRoot", scene);

            points.forEach((p, idx) => {
                // normalize vector
                let vx = p.x, vy = p.y, vz = p.z;
                const len = Math.sqrt(vx*vx + vy*vy + vz*vz);
                if (len === 0) { vx=1; vy=0; vz=0; } else { vx/=len; vy/=len; vz/=len; }
                const pos = new BABYLON.Vector3(vx*1.02, vy*1.02, vz*1.02);

                // marker (blue)
                const marker = makeMarker("m"+idx, pos, 0x0000ff, 0.03);
                marker.metadata = { doc: p.doc };
                marker.parent = markersRoot;

                // line from origin
                const line = BABYLON.MeshBuilder.CreateLines("line"+idx, { points: [BABYLON.Vector3.Zero(), pos] }, scene);
                line.color = new BABYLON.Color3(0,0,1);
                line.parent = markersRoot;
                line.thickness = 2;
            });
        })
        .catch(err => console.error(err));
}

// Initial load
loadDocPoints();

// -------------------
// Hover tooltip
// -------------------
let lastHovered = null;
canvas.addEventListener("pointermove", ev => {
    const pick = scene.pick(scene.pointerX, scene.pointerY, mesh => mesh && mesh.metadata && mesh.metadata.doc);
    if (pick && pick.hit && pick.pickedMesh) {
        const m = pick.pickedMesh;
        if (m !== lastHovered) {
            lastHovered = m;
            tooltip.style.display = "block";
            tooltip.textContent = m.metadata.doc;
            m.scaling = new BABYLON.Vector3(1.6,1.6,1.6);
        }
        tooltip.style.left = ev.clientX + "px";
        tooltip.style.top = ev.clientY + "px";
    } else {
        if (lastHovered) lastHovered.scaling = BABYLON.Vector3.One();
        lastHovered = null;
        tooltip.style.display = "none";
    }
});

// -------------------
// Render User Query from query_point.json
// -------------------
let queryMarker = null;
let queryLine = null;

function renderQueryMarker() {
    fetch(queryPointUrl + "?t=" + Date.now()) // cache-busting
        .then(res => res.json())
        .then(p => {
            if (!p || !('x' in p && 'y' in p && 'z' in p)) return;

            // Normalize vector
            let vx = p.x, vy = p.y, vz = p.z;
            const len = Math.sqrt(vx*vx + vy*vy + vz*vz);
            if (len === 0) { vx=1; vy=0; vz=0; } else { vx/=len; vy/=len; vz/=len; }
            const pos = new BABYLON.Vector3(vx*1.05, vy*1.05, vz*1.05);

            // Remove old marker/line
            if (queryMarker) queryMarker.dispose();
            if (queryLine) queryLine.dispose();

            // Add red marker
            queryMarker = makeMarker("query", pos, 0xff0000, 0.05);
            queryMarker.metadata = { doc: "User Query" };

            // Line
            queryLine = BABYLON.MeshBuilder.CreateLines("queryLine", {
                points: [BABYLON.Vector3.Zero(), pos]
            }, scene);
            queryLine.color = new BABYLON.Color3(1,0,0);
            queryLine.thickness = 3;
        })
        .catch(err => console.error(err));
}

// Initial query marker render
renderQueryMarker();

// Refresh every 2 seconds
setInterval(renderQueryMarker, 2000);

// -------------------
// Camera settings
// -------------------
camera.setTarget(BABYLON.Vector3.Zero());
camera.lowerRadiusLimit = 1.5;
camera.upperRadiusLimit = 12;

// -------------------
// Resize
// -------------------
window.addEventListener("resize", () => { engine.resize(); });

// -------------------
// Render loop
// -------------------
engine.runRenderLoop(() => {
    globe.rotation.y += 0.0008;
    scene.render();
});
