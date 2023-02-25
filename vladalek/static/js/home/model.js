import * as THREE from 'three';
import { OrbitControls } from "https://unpkg.com/three@0.135.0/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://unpkg.com/three@0.135.0/examples/jsm/loaders/GLTFLoader.js";

const canvas = document.getElementById("greeting_text")
const ctx = canvas.getContext('2d');
const layers = 4;
let size = 0;
let particles = [];
let targets = [];
const lerp = (t, v0, v1) => (1 - t) * v0 + t * v1;
const fov = 2000;
const viewDistance = 200;
let targetRotationY = 0.5;
let rotationY = 0.5;
let speed = 40;
let animFrame;

let textIndex = 0;

canvas.width = window.innerWidth;
canvas.height = 30 * window.innerWidth/100

class Vector3 {
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  static fromScreenCoords(_x, _y, _z) {
    const factor = fov / viewDistance;
    const x = (_x - canvas.width / 2) / factor;
    const y = (_y - canvas.height / 2) / factor;
    const z = _z !== undefined ? _z : 0;

    return new Vector3(x, y, z);
  }

  rotateX(angle) {
    const z = this.z * Math.cos(angle) - this.x * Math.sin(angle);
    const x = this.z * Math.sin(angle) + this.x * Math.cos(angle);
    return new Vector3(x, this.y, z);
  }
  rotateY(angle) {
    const y = this.y * Math.cos(angle) - this.z * Math.sin(angle);
    const z = this.y * Math.sin(angle) + this.z * Math.cos(angle);
    return new Vector3(this.x, y, z);
  }
  pp() {
    const factor = fov / (viewDistance + this.z);
    const x = this.x * factor + canvas.width / 2;
    const y = this.y * factor + canvas.height / 2;
    return new Vector3(x, y, this.z);
  }}


function init(e) {
  if (e) e.preventDefault();
  cancelAnimationFrame(animFrame);
  const text = "Привіт!";
  let fontSize = 150;
  let startX = window.innerWidth / 2;
  let startY = canvas.clientHeight / 2;
  particles = [];
  targets = [];
  // Create temp canvas for the text, draw it and get the image data.
  const c = document.createElement('canvas');
  const cx = c.getContext('2d');
  cx.font = `900 ${fontSize}px Arial`;
  let w = cx.measureText(text).width;
  const h = fontSize * 1.5;
  let gap = 7;

  // Adjust font and particle size to fit text on screen
  while (w > window.innerWidth * .8) {
    fontSize -= 1;
    cx.font = `900 ${fontSize}px Arial`;
    w = cx.measureText(text).width;
  }
  if (fontSize < 100) gap = 6;
  if (fontSize < 70) gap = 4;
  if (fontSize < 40) gap = 2;
  size = Math.max(gap / 2, 1);
  c.width = w;
  c.height = h;
  startX = Math.floor(startX - w / 2);
  startY = Math.floor(startY - h / 2);
  cx.fillStyle = '#000';
  // For reasons unknown to me, font needs to be set here again, otherwise font size will be wrong.
  cx.font = `900 ${fontSize}px Arial`;
  cx.fillText(text, 0, fontSize);
  const data = cx.getImageData(0, 0, w, h);


  // Iterate the image data and determine target coordinates for the flying particles
  for (let i = 0; i < data.data.length; i += 4) {
    const rw = data.width * 4;
    const rh = data.height * 4;
    const x = startX + Math.floor(i % rw / 4);
    const y = startY + Math.floor(i / rw);

    if (data.data[i + 3] > 0 && x % gap === 0 && y % gap === 0) {
      for (let j = 0; j < layers; j++) {
        targets.push(Vector3.fromScreenCoords(x, y, j * 1));
      }
    }
  }

  targets = targets.sort((a, b) => a.x - b.x);
  loop();
  return false;
}

function loop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // As long as there are targets, keep creating new particles.
  // Remove target from the targets array when it's been assigned to a particle.
  for (let i = 0; i < speed; i++) {
    if (targets.length > 0) {

      let target = targets[0];
      let x = canvas.width / 2 + target.x * 10;
      let y = canvas.height / 2;
      let z = -10;

      const position = Vector3.fromScreenCoords(x, y, z);
      const interpolant = 0;

      particles.push({ position, target, interpolant });
      targets.splice(0, 1);
    }
  }

  particles.
  sort((pa, pb) => pb.target.z - pa.target.z).
  forEach((p, i) => {
    if (p.interpolant < 1) {
      p.interpolant = Math.min(p.interpolant + .01, 1);

      p.position.x = lerp(p.interpolant, p.position.x, p.target.x);
      p.position.y = lerp(p.interpolant, p.position.y, p.target.y);
      p.position.z = lerp(p.interpolant, p.position.z, p.target.z);
    }
    const rotationX = Math.sin(Date.now() / 2000) * .8;
    rotationY = lerp(0.00001, rotationY, targetRotationY);
    const particle = p.position.
    rotateX(rotationX).
    rotateY(rotationY).
    pp();

    const s = 1 - p.position.z / layers;
    ctx.fillStyle = p.target.z === 0 ?
    'rgb(114, 204, 255)' :
    `rgba(242, 101, 49, ${s})`;

    ctx.fillRect(particle.x, particle.y, s * size, s * size);
  });

  animFrame = requestAnimationFrame(loop);
}

init();

window.addEventListener('mousemove', e => {
  const halfHeight = window.innerHeight / 2;
  targetRotationY = (e.clientY - halfHeight) / window.innerHeight;
});

function setSpeed(e, val) {
  document.querySelectorAll('button').forEach(el => {
    el.classList.remove('active');
  });
  e.target.classList.add('active');
  speed = val;
}

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 0.35;
camera.position.y = 0.05;
const light = new THREE.PointLight(0xffffff, 8);
light.position.set(0, 2, 2);
scene.add(light);
const ambient_light = new THREE.AmbientLight(0xffffff, 3);
scene.add(ambient_light);
const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setClearColor(0x000000, 0)
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("model-container").appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
const loader = new GLTFLoader();
loader.load(
  "/static/3d_models/robot_playground/scene.gltf",
  function (gltf) {
    const mixer = new THREE.AnimationMixer(gltf.scene);
    gltf.animations.forEach((clip) => {
      mixer.clipAction(clip).play();
      clip.loop = THREE.LoopRepeat;
    });
    gltf.scene.position.set(0, 0, 0);
    gltf.scene.scale.set(0.1, 0.1, 0.1);
    scene.add(gltf.scene);
    function animate() {
      requestAnimationFrame(animate);
      mixer.update(0.016);
      renderer.render(scene, camera);
    }
    animate();
  },
  undefined,
  function (error) {
    console.error(error);
  }
);

window.addEventListener("resize", function () {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
});