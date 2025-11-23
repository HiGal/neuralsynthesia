<template>
  <div class="particle-background">
    <canvas ref="canvas" class="particle-canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let ctx = null
let particles = []
let animationId = null

class Particle {
  constructor(x, y) {
    this.x = x
    this.y = y
    this.size = Math.random() * 2 + 1
    this.speedX = Math.random() * 1 - 0.5
    this.speedY = Math.random() * 1 - 0.5
    this.opacity = Math.random() * 0.5 + 0.2
  }

  update() {
    this.x += this.speedX
    this.y += this.speedY

    if (this.x > canvas.value.width || this.x < 0) {
      this.speedX *= -1
    }
    if (this.y > canvas.value.height || this.y < 0) {
      this.speedY *= -1
    }
  }

  draw() {
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
  }
}

const init = () => {
  const canvasEl = canvas.value
  ctx = canvasEl.getContext('2d')

  canvasEl.width = window.innerWidth
  canvasEl.height = window.innerHeight

  particles = []
  const numberOfParticles = Math.min(80, Math.floor((canvasEl.width * canvasEl.height) / 15000))

  for (let i = 0; i < numberOfParticles; i++) {
    const x = Math.random() * canvasEl.width
    const y = Math.random() * canvasEl.height
    particles.push(new Particle(x, y))
  }
}

const animate = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  particles.forEach(particle => {
    particle.update()
    particle.draw()
  })

  // Draw connections
  particles.forEach((particleA, indexA) => {
    particles.slice(indexA + 1).forEach(particleB => {
      const dx = particleA.x - particleB.x
      const dy = particleA.y - particleB.y
      const distance = Math.sqrt(dx * dx + dy * dy)

      if (distance < 150) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 * (1 - distance / 150)})`
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.moveTo(particleA.x, particleA.y)
        ctx.lineTo(particleB.x, particleB.y)
        ctx.stroke()
      }
    })
  })

  animationId = requestAnimationFrame(animate)
}

const handleResize = () => {
  init()
}

onMounted(() => {
  init()
  animate()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
.particle-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.particle-canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
