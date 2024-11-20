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

export default {
  data() {
    return {
      user:null,
      route : router,
      // admin : null
      apiUrl : import.meta.env.VITE_API_URL
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