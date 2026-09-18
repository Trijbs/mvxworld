import * as THREE from 'three';

// --- Configuration ---
const CONFIG = {
  backgroundColor: 0x0a0a09,
  accentColor: 0xc8ff00,
  fogColor: 0x0a0a09,
};

const ROOM_CONFIGS = {
  void: {
    name: 'The Void',
    state: 'Origin',
    atmosphere: 'Silent',
    color: 0xc8ff00,
    geometry: 'core'
  },
  nexus: {
    name: 'The Nexus',
    state: 'Intersection',
    atmosphere: 'Dense',
    color: 0x00ffff, 
    geometry: 'slabs'
  },
  echo: {
    name: 'The Echo',
    state: 'Reflection',
    atmosphere: 'Vast',
    color: 0xff00ff, 
    geometry: 'rings'
  },
  archive: {
    name: 'The Archive',
    state: 'Storage',
    atmosphere: 'Ordered',
    color: 0xffffff,
    geometry: 'grid'
  },
  monolith: {
    name: 'The Monolith',
    state: 'Singularity',
    atmosphere: 'Oppressive',
    color: 0xff4d1c, // The 'Burn' color
    geometry: 'pillars'
  },
  lattice: {
    name: 'The Lattice',
    state: 'Connectivity',
    atmosphere: 'Complex',
    color: 0x8a887e, // The 'Mute' color
    geometry: 'lattice'
  }
};

class RoomManager {
  constructor(scene) {
    this.scene = scene;
    this.currentRoom = null;
    this.roomGroup = new THREE.Group();
    this.scene.add(this.roomGroup);
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
  }

  async transitionTo(roomKey) {
    const config = ROOM_CONFIGS[roomKey];
    if (!config) return;

    if (this.currentRoom) {
      await this.fadeOut();
      this.roomGroup.clear();
    }

    this.currentRoom = config;
    this.buildRoom(config);
    await this.fadeIn();
    
    return config;
  }

  buildRoom(config) {
    const color = config.color;

    if (config.geometry === 'core') {
      const coreGeo = new THREE.IcosahedronGeometry(1, 1);
      const coreMat = new THREE.MeshStandardMaterial({ color, wireframe: true, emissive: color, emissiveIntensity: 1.5 });
      const core = new THREE.Mesh(coreGeo, coreMat);
      core.position.y = 1;
      this.roomGroup.add(core);
    } else if (config.geometry === 'slabs') {
      for(let i = 0; i < 20; i++) {
        const slabGeo = new THREE.BoxGeometry(Math.random() * 2, 0.1, Math.random() * 2);
        const slabMat = new THREE.MeshStandardMaterial({ color, transparent: true, opacity: 0.6 });
        const slab = new THREE.Mesh(slabGeo, slabMat);
        slab.position.set((Math.random()-0.5)*10, Math.random()*5, (Math.random()-0.5)*10);
        slab.rotation.set(Math.random()*Math.PI, Math.random()*Math.PI, 0);
        
        // Attach metadata for interactivity
        slab.userData = { 
          type: 'transmission', 
          id: `tx-${i}`, 
          title: `Transmission ${i+1}`,
          url: `posts/00${(i % 3) + 1}.html` // Mock URLs for now
        };
        
        this.roomGroup.add(slab);
      }
    } else if (config.geometry === 'rings') {
      for(let i = 0; i < 10; i++) {
        const ringGeo = new THREE.TorusGeometry(i * 1.5, 0.02, 16, 100);
        const ringMat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.2 });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.rotation.x = Math.PI / 2;
        this.roomGroup.add(ring);
      }
    } else if (config.geometry === 'grid') {
      const boxGeo = new THREE.BoxGeometry(0.2, 0.2, 0.2);
      const boxMat = new THREE.MeshStandardMaterial({ color });
      let i = 0;
      for(let x = -2; x <= 2; x++) {
        for(let z = -2; z <= 2; z++) {
          const box = new THREE.Mesh(boxGeo, boxMat);
          box.position.set(x * 2, 0.1, z * 2);
          
          // Attach metadata for interactivity
          box.userData = { 
            type: 'archive-node', 
            id: `node-${i}`, 
            title: `Archive Node ${i+1}`,
            url: `posts/00${(i % 3) + 1}.html` // Mock URLs for now
          };
          
          this.roomGroup.add(box);
          i++;
        }
      }
    } else if (config.geometry === 'pillars') {
      // Monolith: Towering, oppressive pillars
      for(let i = 0; i < 12; i++) {
        const height = Math.random() * 10 + 2;
        const pillarGeo = new THREE.BoxGeometry(0.5, height, 0.5);
        const pillarMat = new THREE.MeshStandardMaterial({ color, roughness: 0, metalness: 1 });
        const pillar = new THREE.Mesh(pillarGeo, pillarMat);
        pillar.position.set((Math.random()-0.5)*15, height/2, (Math.random()-0.5)*15);
        this.roomGroup.add(pillar);
      }
    } else if (config.geometry === 'lattice') {
      // Lattice: Interconnected lines of data
      const material = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.4 });
      for(let i = 0; i < 15; i++) {
        const points = [];
        for(let j = 0; j < 5; j++) {
          points.push(new THREE.Vector3((Math.random()-0.5)*10, Math.random()*10, (Math.random()-0.5)*10));
        }
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, material);
        this.roomGroup.add(line);
      }
    }
  }
  }

  async fadeOut() {
    return new Promise(resolve => {
      this.roomGroup.children.forEach(child => {
        if (child.material) child.material.opacity = 0;
      });
      setTimeout(resolve, 500);
    });
  }

  async fadeIn() {
    return new Promise(resolve => {
      this.roomGroup.children.forEach(child => {
        if (child.material && child.material.transparent) child.material.opacity = 0.6;
      });
      setTimeout(resolve, 500);
    });
  }
}

class RoomZero {
  constructor() {
    this.initScene();
    this.initLights();
    this.initCameraSystem();
    this.roomManager = new RoomManager(this.scene);
    this.createGlobalGeometry();
    this.initListeners();
    this.animate();
    
    this.transitionToRoom('void');
  }

  initScene() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(CONFIG.backgroundColor);
    this.scene.fog = new THREE.Fog(CONFIG.fogColor, 1, 20);

    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.camera.position.set(0, 1.65, 5);

    this.renderer = new THREE.WebGLRenderer({
      canvas: document.querySelector('#webgl'),
      antialias: true,
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ReinhardToneMapping;
    this.renderer.toneMappingExposure = 1.2;
  }

  initLights() {
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    this.scene.add(ambientLight);

    this.pointLight = new THREE.PointLight(CONFIG.accentColor, 2, 10);
    this.pointLight.position.set(0, 2, 0);
    this.scene.add(this.pointLight);

    const topLight = new THREE.DirectionalLight(0xffffff, 0.2);
    topLight.position.set(0, 5, 0);
    this.scene.add(topLight);
  }

  initCameraSystem() {
    this.shots = {
      void: { pos: { x: 0, y: 1.65, z: 8 }, target: { x: 0, y: 1, z: 0 } },
      nexus: { pos: { x: 2, y: 1.2, z: 2 }, target: { x: 0, y: 0.5, z: 0 } },
      echo: { pos: { x: -4, y: 1.65, z: 2 }, target: { x: -2, y: 1, z: 0 } },
      archive: { pos: { x: 0, y: 5, z: 8 }, target: { x: 0, y: 0, z: 0 } },
      monolith: { pos: { x: 0, y: 1, z: 12 }, target: { x: 0, y: 5, z: 0 } },
      lattice: { pos: { x: 8, y: 3, z: 8 }, target: { x: 0, y: 0, z: 0 } },
    };
    this.isTransitioning = false;
  }

  lerp(start, end, t) {
    return start + (end - start) * t;
  }

  async transitionToRoom(roomKey) {
    if (this.isTransitioning) return;
    this.isTransitioning = true;

    const config = ROOM_CONFIGS[roomKey];
    const shot = this.shots[roomKey];

    const startPos = { ...this.camera.position };
    const startTime = performance.now();
    const duration = 3000;

    const animateTransition = (now) => {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

      this.camera.position.x = this.lerp(startPos.x, shot.pos.x, ease);
      this.camera.position.y = this.lerp(startPos.y, shot.pos.y, ease);
      this.camera.position.z = this.lerp(startPos.z, shot.pos.z, ease);

      if (t < 1) {
        requestAnimationFrame(animateTransition);
      } else {
        this.isTransitioning = false;
      }
    };
    requestAnimationFrame(animateTransition);

    await this.roomManager.transitionTo(roomKey);
    
    document.querySelector('#ui div:nth-child(1)').innerText = `Coordinate: ${roomKey.toUpperCase()}`;
    document.querySelector('#ui div:nth-child(2)').innerText = `State: ${config.state}`;
    document.querySelector('#ui div:nth-child(3)').innerText = `Atmosphere: ${config.atmosphere}`;
    
    this.pointLight.color.set(config.color);
  }

  createGlobalGeometry() {
    const floorGeo = new THREE.PlaneGeometry(100, 100);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.1, metalness: 0.5 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    this.scene.add(floor);

    const grid = new THREE.GridHelper(40, 40, CONFIG.accentColor, 0x222222);
    grid.position.y = 0.01;
    this.scene.add(grid);

    const particleCount = 2500;
    const particlesGeo = new THREE.BufferGeometry();
    const posArray = new Float32Array(particleCount * 3);
    for(let i = 0; i < particleCount * 3; i++) posArray[i] = (Math.random() - 0.5) * 30;
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const particlesMat = new THREE.PointsMaterial({ size: 0.03, color: CONFIG.accentColor, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending });
    this.particles = new THREE.Points(particlesGeo, particlesMat);
    this.scene.add(this.particles);
  }

  initListeners() {
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Hover effect for interactive geometry
    window.addEventListener('mousemove', (e) => {
      this.roomManager.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      this.roomManager.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      this.roomManager.raycaster.setFromCamera(this.roomManager.mouse, this.camera);
      const intersects = this.roomManager.raycaster.intersectObjects(this.roomManager.roomGroup.children);

      // Reset all interactive objects
      this.roomManager.roomGroup.children.forEach(obj => {
        if (obj.userData && obj.userData.url) {
          obj.scale.set(1, 1, 1);
          if (obj.material) obj.material.emissiveIntensity = 0;
        }
      });

      // Highlight hovered object
      if (intersects.length > 0) {
        const object = intersects[0].object;
        if (object.userData && object.userData.url) {
          object.scale.set(1.2, 1.2, 1.2);
          if (object.material) object.material.emissiveIntensity = 2;
          document.body.style.cursor = 'pointer';
        }
      } else {
        document.body.style.cursor = 'default';
      }
    });

    // Click to interact with procedural geometry
    window.addEventListener('click', (e) => {
      this.roomManager.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      this.roomManager.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      this.roomManager.raycaster.setFromCamera(this.roomManager.mouse, this.camera);
      const intersects = this.roomManager.raycaster.intersectObjects(this.roomManager.roomGroup.children);

      if (intersects.length > 0) {
        const object = intersects[0].object;
        if (object.userData && object.userData.url) {
          console.log(`📂 Opening: ${object.userData.title}`);
          window.location.href = object.userData.url;
        }
      }
    });

    document.querySelectorAll('.cam-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const shotKey = btn.getAttribute('data-shot');
        this.transitionToRoom(shotKey);
        console.log(`🎬 UI Trigger: Switching to room ${shotKey}`);
      });
    });

    window.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth) * 2 - 1;
      const y = -(e.clientY / window.innerHeight) * 2 + 1;
      this.pointLight.position.x = x * 5;
      this.pointLight.position.z = y * 5;
    });

    setTimeout(() => {
      const loader = document.getElementById('loader');
      if (loader) loader.style.opacity = '0';
      setTimeout(() => loader?.remove(), 1000);
    }, 1500);
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    const time = performance.now() * 0.001;
    if (this.particles) {
      this.particles.rotation.y += 0.0002;
      this.particles.position.y = Math.sin(time * 0.5) * 0.1;
    }
    this.renderer.render(this.scene, this.camera);
  }
}

new RoomZero();
