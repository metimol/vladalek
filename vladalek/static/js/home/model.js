import * as THREE from 'three';
import { OrbitControls } from "https://unpkg.com/three@0.135.0/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://unpkg.com/three@0.135.0/examples/jsm/loaders/GLTFLoader.js";

// Создаем сцену, камеру и рендерер
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 0.35;
camera.position.y = 0.05;
const light = new THREE.PointLight(0xffffff, 8);
light.position.set(0, 2, 2);
scene.add(light);
const ambient_light = new THREE.AmbientLight(0xffffff, 3);
scene.add(ambient_light);
const background = new THREE.Color();
background.setRGB(0, 0, 0);
scene.background = background;
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("model-container").appendChild(renderer.domElement);

// Добавляем контроллер вращения с помощью мыши или пальца на телефоне
const controls = new OrbitControls(camera, renderer.domElement);

// Загружаем модель в формате glTF
const loader = new GLTFLoader();
loader.load(
  "/static/3d_models/robot_playground/scene.gltf",
  function (gltf) {
    // Создаем анимационный миксер и добавляем анимацию к модели
    const mixer = new THREE.AnimationMixer(gltf.scene);
    gltf.animations.forEach((clip) => {
      mixer.clipAction(clip).play();
      clip.loop = THREE.LoopRepeat; // устанавливаем повторение анимации
    });
    
    gltf.scene.position.set(0, 0, 0);
    gltf.scene.scale.set(0.1, 0.1, 0.1);

    // Добавляем модель в сцену
    scene.add(gltf.scene);

    // Рендерим сцену
    function animate() {
      requestAnimationFrame(animate);

      // Обновляем анимационный миксер на каждом кадре
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

// Обновляем сцену при изменении размера окна
window.addEventListener("resize", function () {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
});