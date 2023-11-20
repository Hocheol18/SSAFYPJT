<template>
    <div>
        <h1> {{ username }}의프로필</h1>
    </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { onMounted, ref } from 'vue'
import axios from 'axios'

const store = useCounterStore()
const username = ref('')
const token = store.token
onMounted (() => {
        
    axios({
        method: 'get',
        url: `${store.API_URL}/accounts/user/`,
        headers: {
            Authorization: `Token ${token}`
        }
        
    })
    .then((res) => {
        console.log(res.data)
        username.value = res.data.username
    })
    .catch((err) => {
        console.log(err)
    })
    
    
    
})

</script>

<style scoped>

</style>