/* Grainient shader adapted from React Bits by David Haz.
   License: MIT + Commons Clause; see grainient.LICENSE.txt.
   Native WebGL2, with a static CSS fallback and reduced-motion support. */
(function () {
  'use strict';

  var VERT = `#version 300 es
in vec2 position;
void main(){ gl_Position = vec4(position, 0.0, 1.0); }`;

  var FRAG = `#version 300 es
precision highp float;
uniform vec2 iResolution;
uniform float iTime;
uniform float uTimeSpeed;
uniform float uColorBalance;
uniform float uWarpStrength;
uniform float uWarpFrequency;
uniform float uWarpSpeed;
uniform float uWarpAmplitude;
uniform float uBlendAngle;
uniform float uBlendSoftness;
uniform float uRotationAmount;
uniform float uNoiseScale;
uniform float uGrainAmount;
uniform float uGrainScale;
uniform float uGrainAnimated;
uniform float uContrast;
uniform float uGamma;
uniform float uSaturation;
uniform vec2 uCenterOffset;
uniform float uZoom;
uniform vec3 uColor1;
uniform vec3 uColor2;
uniform vec3 uColor3;
out vec4 fragColor;
#define S(a,b,t) smoothstep(a,b,t)
mat2 Rot(float a){float s=sin(a),c=cos(a);return mat2(c,-s,s,c);}
vec2 hash(vec2 p){p=vec2(dot(p,vec2(2127.1,81.17)),dot(p,vec2(1269.5,283.37)));return fract(sin(p)*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p),u=f*f*(3.0-2.0*f);float n=mix(mix(dot(-1.0+2.0*hash(i+vec2(0.0,0.0)),f-vec2(0.0,0.0)),dot(-1.0+2.0*hash(i+vec2(1.0,0.0)),f-vec2(1.0,0.0)),u.x),mix(dot(-1.0+2.0*hash(i+vec2(0.0,1.0)),f-vec2(0.0,1.0)),dot(-1.0+2.0*hash(i+vec2(1.0,1.0)),f-vec2(1.0,1.0)),u.x),u.y);return 0.5+0.5*n;}
void mainImage(out vec4 o, vec2 C){
  float t=iTime*uTimeSpeed;
  vec2 uv=C/iResolution.xy;
  float ratio=iResolution.x/iResolution.y;
  vec2 tuv=(uv-0.5+uCenterOffset)/max(uZoom,0.001);
  float degree=noise(vec2(t*0.1,tuv.x*tuv.y)*uNoiseScale);
  tuv.y/=ratio;
  tuv*=Rot(radians((degree-0.5)*uRotationAmount+180.0));
  tuv.y*=ratio;
  float amplitude=uWarpAmplitude/max(uWarpStrength,0.001);
  float warpTime=t*uWarpSpeed;
  tuv.x+=sin(tuv.y*uWarpFrequency+warpTime)/amplitude;
  tuv.y+=sin(tuv.x*(uWarpFrequency*1.5)+warpTime)/(amplitude*0.5);
  float b=uColorBalance,s=max(uBlendSoftness,0.0);
  float blendX=(tuv*Rot(radians(uBlendAngle))).x;
  float blend=S(-0.3-b-s,0.2-b+s,blendX);
  vec3 layer1=mix(uColor3,uColor2,blend);
  vec3 layer2=mix(uColor2,uColor1,blend);
  // Descending blend with defined smoothstep edges on every GPU.
  vec3 col=mix(layer1,layer2,1.0-S(-0.3-b-s,0.5-b+s,tuv.y));
  vec2 grainUv=uv*max(uGrainScale,0.001);
  if(uGrainAnimated>0.5) grainUv+=vec2(iTime*0.05);
  float grain=fract(sin(dot(grainUv,vec2(12.9898,78.233)))*43758.5453);
  col+=(grain-0.5)*uGrainAmount;
  col=(col-0.5)*uContrast+0.5;
  float luma=dot(col,vec3(0.2126,0.7152,0.0722));
  col=mix(vec3(luma),col,uSaturation);
  col=pow(max(col,0.0),vec3(1.0/max(uGamma,0.001)));
  o=vec4(clamp(col,0.0,1.0),1.0);
}
void main(){
  vec4 o = vec4(0.0);
  mainImage(o, gl_FragCoord.xy);
  fragColor = o;
}`;

  var canvas = document.getElementById('hero-grain');
  if (!canvas) return;
  var gl;
  try { gl = canvas.getContext('webgl2', { alpha: false, antialias: false, depth: false, powerPreference: 'low-power' }); }
  catch (error) { canvas.hidden = true; return; }
  if (!gl) { canvas.hidden = true; return; }

  function shader(type, source) {
    var result = gl.createShader(type);
    gl.shaderSource(result, source);
    gl.compileShader(result);
    if (!gl.getShaderParameter(result, gl.COMPILE_STATUS)) {
      var message = gl.getShaderInfoLog(result);
      gl.deleteShader(result);
      throw new Error(message);
    }
    return result;
  }
  var program = gl.createProgram();
  try {
    var vertex = shader(gl.VERTEX_SHADER, VERT);
    var fragment = shader(gl.FRAGMENT_SHADER, FRAG);
    gl.attachShader(program, vertex);
    gl.attachShader(program, fragment);
    gl.linkProgram(program);
    gl.deleteShader(vertex);
    gl.deleteShader(fragment);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
  } catch (error) {
    console.warn('[Grainient] Fundo estático ativado:', error.message);
    gl.deleteProgram(program);
    canvas.hidden = true;
    return;
  }
  gl.useProgram(program);
  var buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  var position = gl.getAttribLocation(program, 'position');
  gl.enableVertexAttribArray(position);
  gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

  // Valores do componente enviado pelo usuário, sem dependências React/OGL.
  var settings = {
    uTimeSpeed: 0.9, uColorBalance: 0, uWarpStrength: 1,
    uWarpFrequency: 6.2, uWarpSpeed: 2, uWarpAmplitude: 50,
    uBlendAngle: 16, uBlendSoftness: 0.06, uRotationAmount: 500,
    uNoiseScale: 2, uGrainAmount: 0, uGrainScale: 2,
    uGrainAnimated: 0, uContrast: 1.5, uGamma: 1, uSaturation: 1, uZoom: 0.9
  };
  Object.keys(settings).forEach(function (key) {
    gl.uniform1f(gl.getUniformLocation(program, key), settings[key]);
  });
  ['#d2c58f', '#9ab3ff', '#cfc897'].forEach(function (hex, index) {
    var rgb = hex.slice(1).match(/../g).map(function (part) { return parseInt(part, 16) / 255; });
    gl.uniform3fv(gl.getUniformLocation(program, 'uColor' + (index + 1)), rgb);
  });
  gl.uniform2f(gl.getUniformLocation(program, 'uCenterOffset'), 0, 0);
  var resolution = gl.getUniformLocation(program, 'iResolution');
  var time = gl.getUniformLocation(program, 'iTime');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  var visible = true, lost = false, disposed = false, raf = 0, elapsed = 0, last = 0;

  function draw() {
    if (lost || disposed) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var width = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var height = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }
    gl.viewport(0, 0, width, height);
    gl.uniform2f(resolution, width, height);
    gl.uniform1f(time, elapsed);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  function stop() { cancelAnimationFrame(raf); raf = 0; last = 0; }
  function loop(now) {
    raf = 0;
    if (last) elapsed += Math.min(now - last, 100) / 1000;
    last = now;
    draw();
    raf = requestAnimationFrame(loop);
  }
  function sync() {
    stop();
    if (!lost && !disposed && visible && !document.hidden) {
      draw();
      if (!reduced.matches) raf = requestAnimationFrame(loop);
    }
  }
  var resize = new ResizeObserver(draw);
  resize.observe(canvas);
  var intersection = new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting;
    sync();
  });
  intersection.observe(canvas);
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  canvas.addEventListener('webglcontextlost', function () {
    lost = true;
    stop();
    canvas.hidden = true;
  });
  window.addEventListener('pagehide', function (event) {
    stop();
    if (event.persisted) return;
    disposed = true;
    resize.disconnect();
    intersection.disconnect();
    reduced.removeEventListener('change', sync);
    document.removeEventListener('visibilitychange', sync);
    gl.deleteBuffer(buffer);
    gl.deleteProgram(program);
  });
  window.addEventListener('pageshow', sync);
  sync();
})();