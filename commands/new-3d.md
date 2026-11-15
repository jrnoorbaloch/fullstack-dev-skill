---
description: Build a 3D web experience with Three.js or React Three Fiber
argument-hint: "<what to show in 3D: product viewer, hero scene, configurator…>"
---
Use the fullstack-developer skill to build this 3D experience: $ARGUMENTS

1. Read `references/threejs.md` (and `references/animation-gsap.md` if scroll-driven).
2. Choose vanilla Three.js (static site) or React Three Fiber + drei (React/Next.js; load the canvas client-only).
3. Use compressed glTF/GLB for models, cap pixel ratio at 2, pause rendering off-screen, dispose resources on unmount.
4. Provide a WebGL fallback image, reduced-motion behaviour, and keep all important text outside the canvas.
5. Test on desktop and mobile sizes; report the bundle size and frame-rate considerations.
