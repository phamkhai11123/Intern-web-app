<template>
  <div>
    <h1>User Info</h1>
    <p v-if="user">Name: {{ user.name }}</p> 
    <p v-if="user">Username: {{ user.username }}</p>
    <p v-if="user">Email: {{ user.email }}</p> 
    <p v-if="user" class="text-danger">Role: {{ user.role }}</p> 
    <p v-if="user">Register day: {{ user.created_at }}</p> 
    <p>apiurl: {{ apiUrl }}</p>
    <button v-if="user" class="btn btn-primary" @click="onLogout">Logout</button>
    
    <button v-if="user" class="btn btn-warning ms-2" @click="fetchUserData">Get list user </button>
   

  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';
// const route = router
// const apiurl = process.env.VUE_APP_API_URL

export default {
  data() {
    return {
      user:null,
      route : router,
      // admin : null
      apiUrl : process.env.VUE_APP_API_URL || 'http://172.23.224.1:8000'
    };
  },
  methods:{
    onLogout (){
      localStorage.clear()
      this.route.push('/login')
    },
    fetchUserData(){
      this.route.push('/list')
    }
  },
  async mounted() {
    const token = localStorage.getItem('access_token');
    console.log(token)
    if (token){
      try {
        const response = await axios.get(`${this.apiUrl}/users/me`,{
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.user = response.data;
        // console.log(this.user)
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    }
    

  }
};
</script>