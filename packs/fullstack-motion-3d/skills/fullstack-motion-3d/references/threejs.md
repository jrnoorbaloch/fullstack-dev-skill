# 3D on the Web: Three.js & React Three Fiber

Use 3D when it communicates something (product viewer, configurator, data in space, immersive hero), not as decoration that slows the page.

## Choose
| Project | Use |
|---|---|
| Vanilla site / single section | `three` directly |
| React / Next.js app | **React Three Fiber** (`@react-three/fiber`) + `@react-three/drei` helpers |
| Physics | `@react-three/rapier` |
| Post-processing (bloom, DOF) | `@react-three/postprocessing` |
| Scroll-driven 3D | GSAP ScrollTrigger animating camera/object values (`references/animation-gsap.md`) |

```bash
npm i three && npm i -D @types/three
npm i @react-three/fiber @react-three/drei      # React
```

## Vanilla scene skeleton
```js
import * as THREE from "three";

const canvas = document.querySelector("#scene");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 0, 6);

scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const key = new THREE.DirectionalLight(0xffffff, 2); key.position.set(3, 4, 5); scene.add(key);

const mesh = new THREE.Mesh(
  new THREE.TorusKnotGeometry(1, 0.35, 220, 32),
  new THREE.MeshStandardMaterial({ color: 0x7c8cff, metalness: 0.6, roughness: 0.25 }),
);
scene.add(mesh);

function resize() {
  const { clientWidth: w, clientHeight: h } = canvas;
  if (canvas.width !== w * renderer.getPixelRatio() || canvas.height !== h * renderer.getPixelRatio()) {
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }
}
const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  resize();
  mesh.rotation.y += clock.getDelta() * 0.4;
  renderer.render(scene, camera);
});
```
CSS: `#scene { width: 100%; height: 100%; display: block; }` inside a sized container.

## React Three Fiber skeleton
```tsx
import { Canvas, useFrame } from "@react-three/fiber";
import { Environment, OrbitControls, Float, ContactShadows } from "@react-three/drei";
import { useRef } from "react";
import type { Mesh } from "three";

function Knot() {
  const ref = useRef<Mesh>(null!);
  useFrame((_, dt) => { ref.current.rotation.y += dt * 0.4; });   // mutate refs, never setState per frame
  return (
    <Float speed={2} rotationIntensity={0.4}>
      <mesh ref={ref}><torusKnotGeometry args={[1, 0.35, 220, 32]} /><meshStandardMaterial color="#7c8cff" metalness={0.6} roughness={0.25} /></mesh>
    </Float>
  );
}

export default function Scene() {
  return (
    <Canvas camera={{ position: [0, 0, 6], fov: 45 }} dpr={[1, 2]}>
      <ambientLight intensity={0.4} />
      <directionalLight position={[3, 4, 5]} intensity={2} />
      <Knot />
      <ContactShadows position={[0, -1.6, 0]} opacity={0.4} blur={2.5} />
      <Environment preset="city" />
      <OrbitControls enablePan={false} enableZoom={false} />
    </Canvas>
  );
}
```
Next.js: put the canvas in a Client Component and load it with `dynamic(() => import("./Scene"), { ssr: false })`.

## Models
- Format: **glTF/GLB**. Compress with `npx gltf-transform optimize in.glb out.glb --compress draco --texture-compress webp`.
- Load: `GLTFLoader` (+ `DRACOLoader`) or drei `useGLTF("/model.glb")`; generate typed components with `npx gltfjsx model.glb --transform`.
- Keep hero models < 2–3 MB; textures ≤ 2048 px; use KTX2 for many textures.

## Interaction
- Raycasting for hover/click (`raycaster.setFromCamera(pointer, camera)`; R3F: `onPointerOver`/`onClick` on meshes).
- Pointer parallax: lerp camera/group rotation towards pointer each frame (or `gsap.quickTo`).
- Scroll: ScrollTrigger timeline animating `camera.position`, `mesh.rotation`, material uniforms.

## Performance budget
- Cap pixel ratio at 2 (1.5 on mobile); pause rendering when the canvas is off-screen (`IntersectionObserver`) or tab hidden.
- Reuse geometries/materials; use `InstancedMesh` for many copies; merge static meshes.
- Prefer baked lighting/environment maps over many real-time lights; limit shadow-casting lights to one.
- Dispose on unmount: `geometry.dispose()`, `material.dispose()`, `texture.dispose()`, `renderer.dispose()`.
- Target 60 fps on a mid-range phone; check with `stats.js` / `r3f-perf`.

## Accessibility & fallbacks
- Canvas is decorative unless interactive: `aria-hidden="true"`, or provide a text description and keyboard controls for configurators.
- Respect `prefers-reduced-motion` (stop auto-rotation, disable scroll scrubbing).
- Fallback image when WebGL is unavailable (`WebGL.isWebGL2Available()` from `three/addons/capabilities/WebGL.js`).
- Never put essential text only inside the 3D scene.

See `examples/aurora-3d` for a GSAP + Three.js landing page.
