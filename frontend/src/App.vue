<template>
    <div>
        <router-view></router-view>
        <vue-snotify></vue-snotify>
    </div>
</template>

<script>
  export default {
}
</script>

<style lang="scss">
    @import "~vue-snotify/styles/material.css";
</style>
