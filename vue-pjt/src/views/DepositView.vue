<template>
    <div class = "topcontainer">
        <div class="tab">
            <RouterLink :to="{ name : 'Deposit' }" class="subbox">
            예금
            </RouterLink> <p style="filter: invert(100%);"> | </p>
            <RouterLink :to="{ name : 'Saving' }" class="notsubbox">
            적금
            </RouterLink>
        </div>
        <div class="input-container">
            <input type="text" style="text-align: right;" @click="clearInput" v-model="inputText">
        </div>
    </div>
    <Transition>
      <div v-show="isVisible">
    <div class="container">
      <div v-if="filteredDeposits.length > 0">
        <table class="table">
        <thead>
          <tr>
            <th>공시 날짜</th>
            <th>회사 이름</th>
            <th>상품 이름</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>18개월</th>
            <th>24개월</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="deposit in filteredDeposits" :key="deposit.fin_prdt_cd" @click="clickfunction(deposit.fin_prdt_cd)">
            <td>{{ currentTime }}</td>
            <td>{{ deposit.kor_co_nm }}</td>
            <td>{{ deposit.fin_prdt_nm }}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][0]}}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][1]}}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][2]}}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][3]}}</td>
          </tr>
        </tbody>
      </table>
    </div>
      <div v-else>
        <table class="table">
        <thead>
          <tr>
            <th>공시 날짜</th>
            <th>회사 이름</th>
            <th>상품 이름</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>18개월</th>
            <th>24개월</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="deposit in store.deposits" :key="deposit.fin_prdt_cd" @click="clickfunction(deposit.fin_prdt_cd)">
            <td>{{ currentTime }}</td>
            <td>{{ deposit.kor_co_nm }}</td>
            <td>{{ deposit.fin_prdt_nm }}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][0]}}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][1]}}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][2]}}</td>
            <td>{{groupDeposits[deposit.fin_prdt_cd][3]}}</td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>
    </div>
    </Transition>
  </template>

<script setup>
import dayjs from "dayjs";
import { ref,  computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue';
import { RouterLink, useRouter } from "vue-router";

const store = useCounterStore()
const isVisible = ref(false)
const currentTime = ref(dayjs().format('YYYYMMDD')) // 현재날짜 + 시각
const inputText = ref('검색')
const router = useRouter()

const clickfunction = function (key) {
  router.push({name:'Bank', params:{'id':key}})
}

const clearInput = function() {
  inputText.value = ''
}

const filteredDeposits = computed(() => {
  const searchText = inputText.value.toLowerCase()
  return store.deposits.filter(deposit => deposit.kor_co_nm.toLowerCase().includes(searchText))
})

onMounted(() => {
  store.DepositSaving()
  store.DepositOptions()
})

const groupDeposits = computed(() => {
  const grouped = {}
  store.deposits.forEach((deposit) => {
      const finPrdtCd = deposit.fin_prdt_cd
      if (!grouped[finPrdtCd]) {
          grouped[finPrdtCd] = [];
      }
      store.depositsOption.forEach((opt) => {
          if (opt.fin_prdt_cd === finPrdtCd) {
            grouped[finPrdtCd].push(opt['intr_rate'])
          }
      })
  })
  return grouped
})

setTimeout(() => {
    isVisible.value = true
}, 300)

</script>

<style scoped>


@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300&display=swap');
/* 전체 레이아웃에 대한 스타일 */
.notsubbox {
border:1px solid rgba(0,0,0,0.8);
  border-radius: 5px;
  width:50px;
  height:40px;
  background-color:white;
  text-align: center;
  line-height: 40px;
}
.container {
  width: 80%;
  margin: 0 auto; /* 가운데 정렬 */
  background-color: white;
  font-size: 20px;
  border:none;
}

/* 상단 탭 / 버튼 스타일 */
.topcontainer {
    width:80%;
    margin: 0 auto;
    display: flex;
}

input {
  width: 200px;
  height: 35px;
}
.tab {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 10px 20px;
  flex:1;
}
.input-container {
  display: flex;
  justify-content: flex-end; /* input을 오른쪽에 배치 */
  flex: 1; /* 나머지 공간을 차지하도록 flex-grow 설정 */
  align-items: center; /* 세로축 중앙 정렬 */
}


.subbox {
  border:1px solid rgba(0,0,0,0.8);
  border-radius: 5px;
  width:50px;
  height:40px;
  background-color:black;
  text-align: center;
  line-height: 40px;
  color:white;
}
/* 탭 사이의 세로선 스타일 */
.tab p {
  display: inline-block; /* 인라인 블록 요소로 변경 */
  margin: 0 10px; /* 좌우 여백 추가 */
  color: #ccc; /* 색상 변경 */
}



/* 탭 / 버튼 활성화 상태 */
.tab.active {
  background-color: skyblue;
  color: white;
}

/* 테이블 스타일 */
.table {
  width: 100%;
  border-collapse: collapse;
}

/* 테이블 헤더 스타일 */.table th {
    font-family: 'Noto Sans KR', sans-serif;
  background-color: white;
  color: black;
  padding: 15px;
  text-align: center;
}

/* 테이블 셀 스타일 */
.table td {
font-family: 'Noto Sans KR', sans-serif;
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  font-size: 20px;
  background-color: white;
}

a {
  text-decoration: none;
}

.v-enter-from{
    opacity: 0;
    transform: translateY(10px);
    
}

.v-leave-to {
    opacity: 0;
    transform: translateY(10px);
    
}

.v-enter-active, .v-leave-active {
    transition: opacity 1.2s ease;
}
</style>