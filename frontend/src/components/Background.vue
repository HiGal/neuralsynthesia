<template>
  <Particles
      id="tsparticles"
      :particlesInit="particlesInit"
      :particlesLoaded="particlesLoaded"
      :options="{
                    background: {
                        color: {
                            value: 'gray'
                        }
                    },
                    fpsLimit: 60,
                    interactivity: {
                        events: {
                            onClick: {
                                enable: true,
                                mode: 'push'
                            },
                            onHover: {
                                enable: false,
                                mode: 'grab'
                            },
                            resize: true
                        },
                        modes: {
                            bubble: {
                                distance: 400,
                                duration: 2,
                                opacity: 0.6,
                                size: 40
                            },
                            push: {
                                quantity: 4
                            },
                            repulse: {
                                distance: 200,
                                duration: 0.4
                            }
                        }
                    },
                    particles: {
                        color: {
                            value: '#F5F5F5FF'
                        },
                        links: {
                            color: '#F5F5F5FF',
                            distance: 150,
                            enable: true,
                            opacity: 0.2,
                            width: 1
                        },
                        collisions: {
                            enable: false
                        },
                        move: {
                            direction: 'none',
                            enable: true,
                            outMode: 'out',
                            bounce: true,
                            random: true,
                            speed: 2,
                            straight: false
                        },
                        number: {
                            density: {
                                enable: true,
                                value_area: 800
                            },
                            value: 80
                        },
                        opacity: {
                            value: 0.1
                        },
                        shape: {
                            type: 'circle'
                        },
                        size: {
                            random: true,
                            value: 5
                        }
                    },
                    detectRetina: true
                }"
  />
</template>

<script>
export default {
  name: "Background"
}
</script>

<style scoped>

</style>