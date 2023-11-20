import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()
  const deposits = ref([])
  const depositsOption = ref([])
  const savings = ref([])
  const savingOptions = ref([])

  const isLogin = computed(() => {
    if(token.value === null) {
      return false
    } else {
      return true
    }
  })

  // DRF에 article 조회 요청을 보내는 action
  const getArticles = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    }).then((res) => {
      articles.value = res.data
    }).catch((error) => {
      console.log(error)
    })
  }
  
  const signUp = function(payload) {
    axios({
      method : 'post',
      url: `${API_URL}/accounts/signup/`,
      data : {
        username: payload.username,
        password1: payload.password1,
        password2 : payload.password2
      }
    }).then((res) => {
      alert('회원 가입 성공')
      router.push({name : 'LogInView'})
    }).catch((err) => {
      console.log(err)
    })
  }

  const login = function (payload) {
    const {username, password} = payload
    axios({
      method : 'post',
      url: `${API_URL}/accounts/login/`,
      data : {
        username, password
      }
    }).then((res) => {
      console.log(res.data)
      token.value = res.data.key
      router.push({name : 'ArticleView'})
      
    }).catch((err) => {
      console.log(err)
    })
  }

  const DepositSaving = function() {
    axios({
      method : 'get',
      url: `${API_URL}/api/v2/dview/`,
    }).then((res) => {
      deposits.value = res.data
    }).catch((err) => {
      console.log(err)
    })
  }

  const DepositOptions = function() {
    axios({
      method : 'get',
      url: `${API_URL}/api/v2/doview/`,
    }).then((res) => {
      depositsOption.value = res.data
    }).catch((err) => {
      console.log(err)
    })
  }

  const Saving = function() {
    axios({
      method : 'get',
      url: `${API_URL}/api/v2/sview/`,
    }).then((res) => {
      savings.value = res.data
    }).catch((err) => {
      console.log(err)
    })
  }

  const SavingOption = function() {
    axios({
      method : 'get',
      url: `${API_URL}/api/v2/soview/`,
    }).then((res) => {
      savingOptions.value = res.data
      console.log(savingOptions)
    }).catch((err) => {
      console.log(err)
    })
  }



  return {Saving, SavingOption, savings, savingOptions, articles, API_URL, getArticles, signUp, login, token, isLogin, DepositSaving, deposits, DepositOptions, depositsOption}
}, { persist: true })
