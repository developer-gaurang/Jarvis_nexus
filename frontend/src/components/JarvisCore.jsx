import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// Vertex Shader: Controls positions and dynamic motion of particles
const vertexShader = `
uniform float uTime;
uniform float uIsSpeaking;
varying vec3 vPosition;

void main() {
    vPosition = position;
    
    vec3 pos = position;
    
    // 1. Idle State: Soft noise to give it a living, stable feel
    // Adding slight positional variance
    float noise = sin(pos.x * 5.0 + uTime) * cos(pos.y * 5.0 + uTime) * sin(pos.z * 5.0 + uTime);
    pos += normal * noise * 0.1 * (1.0 - uIsSpeaking); // Only highly active during idle
    
    // 2. Voice Reactive State: Agitated, pulsating, and breaking away
    if (uIsSpeaking > 0.0) {
        // High frequency noise for rapid agitation
        float intenseNoise = sin(pos.x * 12.0 + uTime * 6.0) * cos(pos.y * 12.0 + uTime * 6.0) * sin(pos.z * 12.0 + uTime * 6.0);
        
        // Burst energy outwards
        pos += normal * intenseNoise * 0.5 * uIsSpeaking;
        
        // Ripple effect pulsating from core
        float ripple = sin(length(position) * 15.0 - uTime * 20.0) * 0.2 * uIsSpeaking;
        pos += normal * ripple;
    }
    
    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    
    // Size changes dynamically when speaking
    gl_PointSize = (4.0 + (uIsSpeaking * 6.0)) * (1.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
}
`;

// Fragment Shader: Controls colors, giving that dynamic Iridescent Rainbow glow
const fragmentShader = `
uniform float uTime;
varying vec3 vPosition;

// Generates a shifting iridescent (rainbow) gradient based on 3D spatial position
vec3 getRainbowColor(vec3 pos, float time) {
    float shift = length(pos) + time * 0.5;
    // Classic iridescent phase shift
    return vec3(
        0.5 + 0.5 * cos(6.28318 * (shift + 0.0)),
        0.5 + 0.5 * cos(6.28318 * (shift + 0.33)),
        0.5 + 0.5 * cos(6.28318 * (shift + 0.67))
    );
}

void main() {
    // Generate soft circular particles instead of harsh squares
    float r = distance(gl_PointCoord, vec2(0.5));
    if (r > 0.5) discard;
    
    vec3 color = getRainbowColor(vPosition, uTime);
    
    // Fade out towards particle edges for natural glowing aura
    float alpha = 1.0 - (r * 2.0);
    
    gl_FragColor = vec4(color, alpha);
}
`;

export default function JarvisCore({ isSpeaking }) {
  const pointsRef = useRef();
  
  const particlesCount = 15000;
  
  // Create static spherical coordinate cluster for initial state
  const positions = useMemo(() => {
    const arr = new Float32Array(particlesCount * 3);
    for (let i = 0; i < particlesCount; i++) {
        // Distribute uniformly across spherical surface
        const theta = Math.random() * 2 * Math.PI;
        const phi = Math.acos((Math.random() * 2) - 1);
        const radius = 1.6; 
        
        arr[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
        arr[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
        arr[i * 3 + 2] = radius * Math.cos(phi);
    }
    return arr;
  }, [particlesCount]);

  // Track uniforms (time and speaking interaction)
  const uniforms = useMemo(() => ({
      uTime: { value: 0 },
      uIsSpeaking: { value: 0 }
  }), []);

  // Frame Loop updates shader variables on 60fps
  useFrame((state) => {
      const time = state.clock.getElapsedTime();
      
      if (pointsRef.current) {
          // Slow idle rotation on axis
          pointsRef.current.rotation.y = time * 0.2;
          pointsRef.current.rotation.x = time * 0.1;

          // Push Time variable to Fragment
          pointsRef.current.material.uniforms.uTime.value = time;
          
          // Gently interpolate isSpeaking flag (0 to 1 float scale)
          // Doing this inside useFrame avoids strict boolean popping, creating smooth ripples
          const targetIsSpeaking = isSpeaking ? 1.0 : 0.0;
          pointsRef.current.material.uniforms.uIsSpeaking.value = THREE.MathUtils.lerp(
              pointsRef.current.material.uniforms.uIsSpeaking.value,
              targetIsSpeaking,
              0.1 // speed of transition
          );
      }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particlesCount}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        transparent={true}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}
