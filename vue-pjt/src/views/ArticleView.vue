<template>
  <div class="toptop">
    <h1>Article Page</h1>
    <ArticleList />
    <RouterLink :to="{ name:'CreateView'}">
      [Create]
    </RouterLink>
  </div>
</template>

<script setup>
// 최상단 훅인 ArticleView.vue에 mounted 시켜야 한다.
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'


const store = useCounterStore()

onMounted(() => {
  store.getArticles()
})

</script>

<style>
.toptop {
  padding: 50px
}

</style>
