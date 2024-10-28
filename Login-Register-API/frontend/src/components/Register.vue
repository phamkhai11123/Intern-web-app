<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="register">
      <input class="form-control my-2" type="text" v-model="name" placeholder="Fullname" required />
      <input class="form-control my-2" type="text" v-model="username" placeholder="Username" required />
      <input class="form-control my-2" type="text" v-model="email" placeholder="Email" required>
      <input class="form-control my-2" type="password" v-model="password" placeholder="Password" required />
      <input class="form-control my-2" type="password" v-model="password2" name="" id="" placeholder="Confirm password">
      <!-- <input class="form-control my-2" type="text" v-model="role" placeholder="Role" required /> -->
      <select name="" id="" v-model="role" class="form-control my-2">
        <option value="">Role</option>
        <option value="admin">admin</option>
        <option value="user">user</option>
      </select>
      <button class="btn btn-warning" type="submit">Register</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
// import axios from 'axios';
import router from '@/router';

export default {
  data() {
    return {
      name:'',
      username: '',
      password: '',
      email: "",
      password2:"",
      role:"",
      error: '',
      route : router
    };
  },
  methods: {
    async register() {
      if(this.password != this.password2){
        alert("Password2 is different to password1")
        return
      }
      try {
        fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
        body: JSON.stringify({
              name:this.name,
              username: this.username,
              password: this.password,
              email: this.email,
              role :this.role
      })
      })
        .then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log(data); // Handle the response data here 
  // alert("Register successfully!")
  this.route.push('/login')
})
.catch(error => {
  console.error('There was a problem with the fetch operation:', error);
});

      } catch (error) {
        this.error = error.response.data.detail || 'Registration failed';
      }
    },
  },
};
</script>

