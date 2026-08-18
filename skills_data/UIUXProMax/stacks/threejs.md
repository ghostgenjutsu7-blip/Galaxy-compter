---
name: threejs Best Practices
source: UIUXProMax
version: 1.0.0
description: 53 curated threejs guidelines (state, perf, a11y, patterns)
tags: ["stack", "threejs"]
triggers: ["threejs"]
license: MIT
target_agent: 
category: tech_stack
---

# threejs — Best Practices (53 guidelines)

## CDN Version Lock
Always use Three.js r128 from cdnjs. It is the stable CDN baseline. Never use a floating 'latest' URL — it silently breaks when the CDN updates without warning.
- **Do:** Pin to the exact r128 cdnjs URL in every HTML file
- **Don't:** Use unpkg@latest or any unversioned CDN URL that can silently update
- Severity: Critical

## CapsuleGeometry Does Not Exist in r128
THREE.CapsuleGeometry was introduced in r142. Using it on the r128 CDN throws 'CapsuleGeometry is not a constructor' and crashes the entire scene. Build a capsule from primitives instead.
- **Do:** Build a capsule from CylinderGeometry plus two SphereGeometry end caps
- **Don't:** Call THREE.CapsuleGeometry on r128 — it is undefined and throws immediately
- Severity: Critical

## OrbitControls Must Be Loaded Separately
OrbitControls is NOT bundled in the core Three.js r128 CDN file. It lives in examples/js and must be loaded from a separate cdnjs script tag. THREE.OrbitControls is undefined without it.
- **Do:** Load the OrbitControls script from cdnjs examples path before your scene script
- **Don't:** Expect THREE.OrbitControls to exist after loading only the core Three.js CDN script
- Severity: Critical

## Custom Drag Orbit Fallback
When OrbitControls cannot be loaded implement spherical orbit using mousedown/mousemove/mouseup. The key is rotating in spherical coordinates so both horizontal AND vertical drag work correctly.
- **Do:** Rotate camera in spherical coordinates so both axes respond correctly to drag
- **Don't:** Move camera.position.x directly — vertical drag is silently ignored and the orbit is incorrect
- Severity: High

## ESM vs CDN Import
When using a bundler import Three.js as an ES module. When using CDN the THREE global is already available — do not import it again. Mixing both loads Three.js twice and causes subtle runtime errors.
- **Do:** Match import style to build environment: ESM import for bundlers; rely on the window.THREE global for CDN pages
- **Don't:** Mix a CDN script tag with an ES module import in the same file
- Severity: Critical

## Single Renderer Per Page
Create one WebGLRenderer instance for the lifetime of the page. Multiple renderers compete for the browser GPU context limit (8–16 contexts) and cause context-lost errors especially on mobile.
- **Do:** Reuse a single renderer and swap scene content instead of recreating the renderer
- **Don't:** Create a new renderer on each component mount or scene transition
- Severity: Critical

## Pixel Ratio Cap at 2
Cap devicePixelRatio at 2. Retina displays report 3x or higher. Going from 2x to 3x multiplies pixel count by 2.25x with no visible quality improvement at normal viewing distance.
- **Do:** Apply Math.min(window.devicePixelRatio, 2) — cap is at 2 not at 3
- **Don't:** Pass window.devicePixelRatio directly without any cap
- Severity: High

## Alpha Canvas Plus CSS Background
Set alpha:true on the renderer and control the background color through CSS rather than a renderer clear color. This composites the canvas correctly over any HTML content behind it.
- **Do:** Set alpha:true on renderer and let body or a parent div provide the background color
- **Don't:** Set a solid renderer clear color when the canvas must composite over HTML behind it
- Severity: Medium

## Aspect Ratio on Resize
Always update camera.aspect and call camera.updateProjectionMatrix() inside every resize handler. A stale aspect ratio causes the entire scene to appear stretched or squashed horizontally.
- **Do:** Update camera.aspect then call updateProjectionMatrix() on every resize
- **Don't:** Let aspect ratio become stale after the browser window changes size
- Severity: High

## FOV Range 45 to 75
Use a field of view between 45 and 75 degrees. Below 45 creates compressed telephoto distortion. Above 90 creates visible fisheye distortion at frame edges.
- **Do:** Start at 75 for general interactive scenes; use 45–55 for product close-ups
- **Don't:** Use FOV above 90 or below 30 without a deliberate artistic reason
- Severity: Medium

## Explicit Position and lookAt
Always set an explicit camera position and call camera.lookAt() before the first render. The default camera at the origin pointing down -Z makes subjects at arbitrary coordinates invisible or tiny.
- **Do:** Set camera.position.set() and camera.lookAt() to frame the subject before the first render
- **Don't:** Leave the camera at default position (0 0 0) with no lookAt — subject may be behind the camera or microscopic
- Severity: Medium

## OrbitControls vs GSAP Camera Rig
Use OrbitControls for model viewers and exploratory scenes where the user needs free-look. Use a GSAP scroll-driven camera rig for product reveals or storytelling where the camera path must stay fixed.
- **Do:** Match camera control approach to the UX intent of the scene
- **Don't:** Use OrbitControls for a scripted reveal — users can orbit away from the reveal before it completes
- Severity: High

## Never Create Geometry Per Frame
Creating a new geometry inside animate() allocates a fresh GPU buffer every frame and exhausts VRAM within seconds. Create all geometry exactly once before the loop starts. Use attribute mutation if positions must change per frame.
- **Do:** Create all geometry before the animation loop; mutate BufferAttribute arrays in-place if needed
- **Don't:** Call any new XxxGeometry() constructor inside the animation loop
- Severity: Critical

## Share Geometry Across Meshes
When multiple objects share the same shape create one geometry instance and pass it to every Mesh. Each Mesh gets its own transform and material while all share a single GPU buffer.
- **Do:** Create one geometry and pass the same reference to every Mesh constructor
- **Don't:** Create a separate identical geometry inside a loop for each object
- Severity: Critical

## dispose on Scene Removal
Call geometry.dispose() and material.dispose() and texture.dispose() for every texture map when removing objects from the scene. Three.js never releases GPU resources automatically — they stay in VRAM until explicitly freed.
- **Do:** Dispose of geometry + material + every texture map before calling scene.remove()
- **Don't:** Call scene.remove() alone without any dispose calls
- Severity: Critical

## Segment Count Budget
Use the minimum segment count that achieves the desired silhouette quality. Hero objects: 32–64 segments. Background objects: 8–16. Particle stand-ins: 6–8. High counts on background geometry waste GPU draw calls with zero visible benefit.
- **Do:** Apply a tiered segment budget based on the visual priority of each object in the scene
- **Don't:** Default every sphere and cylinder to 64+ segments regardless of its role
- Severity: Medium

## BufferGeometry for Custom Vertex Data
For any custom shape use BufferGeometry with setAttribute('position' ...) and a Float32Array. The legacy THREE.Geometry class was removed in r125 and throws ReferenceError in r128.
- **Do:** Use THREE.BufferGeometry with a Float32Array position attribute for custom vertex data
- **Don't:** Reference or instantiate the removed THREE.Geometry class
- Severity: High

## MeshBasicMaterial vs MeshStandardMaterial
MeshBasicMaterial ignores all lights and is significantly cheaper — use it for UI overlays HUDs and flat-colored decorative elements. MeshStandardMaterial is PBR-accurate and requires lights. Never use StandardMaterial where BasicMaterial suffices.
- **Do:** Use MeshBasicMaterial for any object that does not need lighting; use MeshStandardMaterial for physical objects
- **Don't:** Apply MeshStandardMaterial to flat UI elements that never receive light — lights still run for them
- Severity: Medium

## Share Material Instances
Share one material instance across all meshes that have identical properties. Call mat.clone() only when individual meshes genuinely need different property values. Duplicate materials waste GPU VRAM.
- **Do:** Assign the same material reference to all meshes with identical visual properties
- **Don't:** Create a new material inside a loop for objects that look identical
- Severity: High

## Dispose Textures Explicitly
Textures are the single largest consumer of GPU VRAM in most Three.js scenes. Call texture.dispose() when switching scenes or removing objects — Three.js does not garbage-collect GPU resources automatically.
- **Do:** Track all loaded textures and call dispose() on each one during scene teardown or on object removal
- **Don't:** Load textures without any cleanup path — they persist in VRAM for the entire page lifetime
- Severity: High

## Ambient Plus Directional Minimum
Any scene using MeshStandardMaterial or MeshPhongMaterial requires at minimum one AmbientLight (fill) and one DirectionalLight (shading direction). Without both the objects render as solid black — the material is there but no light reaches it.
- **Do:** Add AmbientLight for fill and DirectionalLight for shading whenever PBR or Phong materials are used
- **Don't:** Use MeshStandardMaterial without adding any lights to the scene
- Severity: Critical

## Enable shadowMap Before castShadow
renderer.shadowMap.enabled = true must be set before any castShadow or receiveShadow flags. Without it the shadow map is never allocated and all shadow flags are silently ignored.
- **Do:** Set renderer.shadowMap.enabled = true first then set castShadow and receiveShadow on lights and meshes
- **Don't:** Set castShadow on a light or mesh without enabling renderer.shadowMap.enabled — shadows never render
- Severity: High

## Selective Shadow Casting
Shadow map rendering redraws the entire scene from the light's perspective every frame. Enable castShadow only on the primary directional light and receiveShadow only on hero meshes and the ground plane.
- **Do:** Enable shadows only on the key light and the most important meshes
- **Don't:** Enable castShadow and receiveShadow on every object in the scene including particles
- Severity: High

## Skip Lights for MeshBasicMaterial
MeshBasicMaterial completely ignores all scene lights. Adding lights solely to illuminate BasicMaterial objects wastes a light pass on every frame with zero visible effect.
- **Do:** Omit lights entirely when every material in the scene is MeshBasicMaterial
- **Don't:** Add AmbientLight and DirectionalLight to a scene that uses only MeshBasicMaterial
- Severity: Low

## Single Shared Raycaster
Create exactly one Raycaster instance outside all event handlers. Store mouse coordinates in pointermove (cheap). Call setFromCamera and intersectObjects together inside the animate() loop — once per frame instead of once per mouse event.
- **Do:** Create one Raycaster; store mouse in pointermove; call setFromCamera + intersectObjects inside animate()
- **Don't:** Create a new THREE.Raycaster() inside a mousemove handler or call setFromCamera inside the event listener
- Severity: Critical

## NDC Mouse Coordinates
Raycasting requires mouse in Normalized Device Coordinates: X from -1 (left) to +1 (right) and Y from +1 (top) to -1 (bottom). The Y axis is inverted relative to screen space. A missing negation on Y causes all raycasts to miss or hit the wrong objects.
- **Do:** Apply the full NDC formula — including the negation on the Y axis
- **Don't:** Forget to negate Y — raycasting appears to work but hits objects mirrored vertically
- Severity: Critical

## setFromCamera and intersectObjects in animate
Call raycaster.setFromCamera(mouse camera) and then raycaster.intersectObjects(targets true) inside the animate() loop. setFromCamera must come before intersectObjects every frame — without it the raycaster uses a stale ray direction.
- **Do:** Call setFromCamera then intersectObjects in order inside every animate() frame
- **Don't:** Call intersectObjects without calling setFromCamera first — the raycaster uses a stale or zero ray
- Severity: Critical

## Recursive Flag for Groups and GLTF
Pass true as the second argument to intersectObjects when testing Groups or GLTF loaded models. Geometry lives on child Mesh objects — without recursive:true the parent group is tested but has no geometry and hits is always empty.
- **Do:** Use intersectObjects(targets true) for Groups or any loaded model
- **Don't:** Raycast against a parent Group without the recursive flag
- Severity: High

## Cursor Feedback on Hover
Set document.body.style.cursor = 'pointer' when intersections are found and reset to 'auto' when none are found. Without cursor feedback users cannot discover that 3D objects are interactive.
- **Do:** Update cursor to pointer on hit; reset to auto on miss in the same animate loop block
- **Don't:** Run raycasting and read hits without ever updating the cursor style
- Severity: Medium

## requestAnimationFrame Loop Only
Drive the render loop exclusively with requestAnimationFrame or renderer.setAnimationLoop(). Never use setInterval or setTimeout — they are not synchronized to the display refresh rate and keep running when the tab is hidden draining battery.
- **Do:** Use requestAnimationFrame or renderer.setAnimationLoop() as the sole render loop driver
- **Don't:** Use setInterval or setTimeout for render timing
- Severity: Critical

## THREE.Clock for Delta Time
Use THREE.Clock and clock.getDelta() for all time-based motion. A hardcoded increment like += 0.01 runs at 2x speed on 120Hz displays and at unpredictable speed when frames drop under load. CRITICAL: call getDelta() exactly ONCE per animate() frame and store the result in a local dt variable. getDelta() resets the internal clock on every call — a second call in the same frame always returns ~0, silently breaking any animation block that uses it.
- **Do:** Call clock.getDelta() once at the top of animate(); store result in dt; reuse dt everywhere in that frame
- **Don't:** Call clock.getDelta() more than once per frame or inside a helper called from animate()
- Severity: High

## Lerp for Smooth Pointer Follow
Use value += (target - value) * alpha each frame to smoothly interpolate toward a moving target. An alpha of 0.03–0.1 produces organic easing for camera follow pointer-tracking and hover scale effects without requiring GSAP.
- **Do:** Apply the lerp formula each frame with a small alpha for smooth organic motion
- **Don't:** Snap a value directly to the target producing an instant jarring jump
- Severity: Medium

## GSAP for Multi-Step Sequences
Use GSAP timelines for any animation with more than two sequential steps or for scroll-linked camera paths. GSAP timelines can be paused reversed and scrubbed — far more maintainable than boolean state machines.
- **Do:** Use GSAP timelines for sequences with more than two steps and for scroll-driven animations
- **Don't:** Implement multi-step sequences with boolean flags and manual frame counters
- Severity: High

## Pause Render Loop on Tab Hidden
Use renderer.setAnimationLoop() as the loop driver so you can pass null to pause and a function to resume. Continuous rendering in a hidden tab wastes CPU GPU and battery with no user benefit.
- **Do:** Use renderer.setAnimationLoop(animate) to drive the loop; pass null to pause on visibilitychange
- **Don't:** Drive with internal requestAnimationFrame and never stop the loop when the tab is hidden
- Severity: High

## Load GSAP Before Scene Script
Load GSAP from its own CDN script tag before your scene script. In bundler projects install via npm and import. GSAP is a completely separate library from Three.js — never try to import it from the Three.js package.
- **Do:** Load GSAP CDN before the scene script; or npm install gsap and import separately
- **Don't:** Import gsap from three or expect it to be defined without a separate load
- Severity: Critical

## Register ScrollTrigger Before Use
Call gsap.registerPlugin(ScrollTrigger) once at the top of your script before any scrollTrigger config object. Without registration the ScrollTrigger name is undefined and the tween throws immediately.
- **Do:** Call gsap.registerPlugin(ScrollTrigger) as the first line before any gsap.to/from/timeline with scrollTrigger
- **Don't:** Include scrollTrigger config in gsap.to() calls without first registering the plugin
- Severity: Critical

## Tween Three.js Properties Directly
GSAP can tween any numeric JavaScript property including mesh.position.x mesh.rotation.y and material.opacity. No wrapper or adaptor is needed. Note: to tween material.opacity the material must have transparent:true set before the tween starts.
- **Do:** Pass Three.js object properties directly to gsap.to(); set transparent:true before tweening opacity
- **Don't:** Use a plain proxy object then manually copy values to Three.js properties every frame
- Severity: Medium

## scrub for Scroll-Driven Camera Path
Use scrub:true or scrub:1 to link camera movement continuously to scroll position as a 0–1 ratio. scrub:1 adds a 1-second lag for cinematic smoothness. onEnter/onLeave fire only once and create jarring snaps — not the right tool for a camera path.
- **Do:** Use scrub:1 for any scroll-controlled camera movement
- **Don't:** Use onEnter or onLeave callbacks for camera motion — they snap instead of scrubbing
- Severity: High

## InstancedMesh for Repeated Objects
Use THREE.InstancedMesh when rendering 50 or more identical objects. It submits all N transforms in one draw call instead of N draw calls and reduces CPU-GPU communication overhead dramatically.
- **Do:** Use InstancedMesh for any group of 50+ meshes sharing the same geometry and material
- **Don't:** Create 50+ separate Mesh objects with the same geometry and material
- Severity: High

## Tone Mapping and sRGB Encoding
Enable ACESFilmicToneMapping and sRGBEncoding on the renderer for accurate perceptual color. Without tone mapping colors appear washed out or over-saturated. These are renderer properties set after construction and take effect immediately.
- **Do:** Set renderer.toneMapping and renderer.outputEncoding after construction for all production scenes
- **Don't:** Leave tone mapping and output encoding at defaults when the scene targets realistic visuals
- Severity: Medium

## antialias Set at Construction Only
The antialias option can only be set at WebGLRenderer construction time. Setting renderer.antialias after construction has absolutely no effect — the WebGL context is already created without it. Decide before instantiating.
- **Do:** Set antialias:true inside the WebGLRenderer constructor options object
- **Don't:** Construct the renderer without antialias then try to enable it by assigning the property
- Severity: High

## FogExp2 for Depth and Far Culling
Use scene.fog to create atmospheric depth. As a secondary benefit objects that disappear into fog before the far plane stop contributing to draw calls — useful in scenes with large view distances.
- **Do:** Add FogExp2 to scenes with view distances above 100 units for both visual atmosphere and implicit far culling
- **Don't:** Ignore fog in scenes with far:1000+ and many distant objects that contribute tiny pixels per draw call
- Severity: Low

## BufferGeometry Plus Points for Particle Systems
Build all particle systems with BufferGeometry plus a Float32Array position attribute rendered as Points. Never use individual Mesh objects as particles — they cannot scale past a few hundred with good performance.
- **Do:** Use Points plus BufferGeometry for all particle effects
- **Don't:** Create hundreds of individual Mesh objects to simulate a particle system
- Severity: High

## Particle Count Ceiling
Start particle systems at 1000–3000 particles. Beyond 50000 causes sustained frame drops on mid-range mobile. Always test on a real device before increasing the count — desktop and mobile GPU performance ratios can be 10:1.
- **Do:** Start at 3000 particles and profile on actual mobile hardware before raising the limit
- **Don't:** Set particle count at 100000 or higher without any mobile profiling
- Severity: High

## needsUpdate After Buffer Mutation
After mutating any BufferAttribute array values per frame you must set geometry.attributes.position.needsUpdate = true so Three.js re-uploads the changed buffer to the GPU. Without it the GPU still uses the old data and particles appear completely frozen.
- **Do:** Set needsUpdate = true on the position attribute after every per-frame mutation of the array
- **Don't:** Mutate the Float32Array values without flagging needsUpdate — positions update in JS but not on the GPU
- Severity: Critical

## Canvas Dimensions Not Window
Size the renderer and camera to the canvas element's clientWidth and clientHeight — not window.innerWidth and innerHeight. This is correct when the canvas is inside a flex or grid container that does not fill the full viewport.
- **Do:** Use canvas.clientWidth and canvas.clientHeight for all renderer and camera sizing
- **Don't:** Hardcode renderer size to window.innerWidth/innerHeight when the canvas may be inside a container
- Severity: High

## ResizeObserver Over window resize Event
Use ResizeObserver on the canvas container instead of the window resize event. ResizeObserver fires when the container element changes size independently of the browser window — common in split-pane layouts and sidebar collapsing.
- **Do:** Attach ResizeObserver to the canvas parent element for accurate container-aware resize detection
- **Don't:** Use only window.addEventListener('resize') for canvas sizing when the canvas is not fullscreen
- Severity: Medium

## Touch Events for Mobile Interaction
Add touchstart and touchmove listeners alongside mouse events so the scene remains interactive on mobile. Normalize touch coordinates to the same NDC range as mouse events and pass passive:false on touchmove if you call preventDefault.
- **Do:** Handle both mouse and touch input for any interactive 3D scene
- **Don't:** Add only mouse event listeners and leave touch users with no interaction
- Severity: Medium

## prefers-reduced-motion
Check window.matchMedia('(prefers-reduced-motion: reduce)') before starting any auto-rotation, particle animation, or camera movement. Users who enable this OS preference have motion sickness or vestibular disorders. IMPORTANT: reading .matches once at page load is a one-time snapshot — if the user changes their OS accessibility setting mid-session the scene will not react. Attach a 'change' listener to the MediaQueryList so noMotion stays in sync at runtime.
- **Do:** Use matchMedia.addEventListener('change') to keep noMotion reactive; gate all auto-animation on the live value
- **Don't:** Read .matches once at startup and never update it — the scene ignores mid-session OS setting changes
- Severity: High

## Canvas aria-label
Add role='img' and a descriptive aria-label to renderer.domElement after appending it to the DOM. Screen readers receive no information from a WebGL canvas — the aria-label is the only description they can announce to users.
- **Do:** Set role='img' and a meaningful aria-label on renderer.domElement before or after appending it
- **Don't:** Append the canvas to the DOM with no accessibility attributes — invisible to screen readers
- Severity: Medium

## Bundler Stack for Production
For production use Three.js via npm plus Vite. You get full tree-shaking reduced bundle size access to the complete examples/jsm library including OrbitControls GLTFLoader and EffectComposer and TypeScript support.
- **Do:** Use npm install three plus Vite or Webpack for any production client-facing project
- **Don't:** Serve raw CDN script tags in a production application that needs tree-shaking or TypeScript
- Severity: Medium

## GLTFLoader with scene traverse
Load 3D models using GLTFLoader and traverse gltf.scene to configure castShadow receiveShadow and material overrides on all child Mesh nodes. Calling scene.add(gltf.scene) alone silently skips all shadow and material configuration.
- **Do:** Use GLTFLoader and traverse the entire gltf.scene graph to set up shadows and materials on every Mesh child
- **Don't:** Load a GLTF model and pass gltf.scene directly to scene.add without traversing child meshes
- Severity: Medium

## LOD for Distance-Based Detail
Use THREE.LOD to automatically swap high-detail and low-detail geometry as objects move closer or farther from the camera. This maintains frame rate in scenes with many objects spread across a large depth range.
- **Do:** Use THREE.LOD to reduce triangle count on distant objects automatically
- **Don't:** Render the same high-polygon geometry for every object regardless of its distance from the camera
- Severity: Medium
