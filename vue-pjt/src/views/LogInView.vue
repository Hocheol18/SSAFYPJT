<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input type="text" v-model.trim="username">
      <input type="password" v-model.trim="password">
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { ref } from 'vue'
const username = ref(null)
const password = ref(null)
const store = useCounterStore()

const login = function () {
  const payload = {
    username : username.value,
    password : password.value
  }
  store.login(payload)
}

</script>

<style>

</style>
