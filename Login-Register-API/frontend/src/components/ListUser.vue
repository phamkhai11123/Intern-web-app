<template>
  <div>
    <input v-if="userData"
      class="form-control w-25 my-2"
      type="text"
      v-model="searchQuery"
      placeholder="Search users by name"
      
    />
     <table  v-if="userData" border="1" width="100%" class="table">
      <thead class="thead-dark">
        <tr>
            <td>STT</td>
            <td>Name</td>
            <td>Username</td>
            <td>Email</td>
            <td>Role</td>
            <td>Register day</td>
            <td>--</td>
        </tr>
      </thead>
         <tbody>
          <tr v-if="!searchQuery" v-for="(user) in userData" :key="user.name">
            <td> {{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role  }}</td>
            <td>{{ user.created_at }}</td>
            <td>
              <button class="btn btn-dark" @click="editUser(user)">Update</button>
              <button class="ms-1 btn btn-info" @click="deleteUser(user.id)">Delete</button>
            </td>
          </tr>
          <tr v-if="searchQuery" v-for="user in filteredUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.created_at }}</td>
          <td>
            <button class="btn btn-dark" @click="editUser(user)">Update</button>
            <button class="ms-1 btn btn-info" @click="deleteUser(user.id)">Delete</button>
          </td>
        </tr>
         </tbody>
     </table>
     <div v-if="selectedUser">
      <h2>Edit User</h2>
      <form @submit.prevent="updateUser">
        <div>
          <label>Name:</label>
          <input v-model="selectedUser.name" type="text" required class="form-control"/>
        </div>
        <div>
          <label>Username:</label>
          <input v-model="selectedUser.username" type="text" required class="form-control"/>
        </div>
        <div>
          <label>Email:</label>
          <input v-model="selectedUser.email" type="email" required  class="form-control"/>
        </div>
        <div>
          <label>Role:</label>
          <!-- <input v-model="selectedUser.role" type="text" required  class="form-control"/> -->
          <select name="" id="" v-model="selectedUser.role" class="form-control">
            <option value="user">user</option>
            <option value="admin">admin</option>
          </select>
        </div>
        <button type="submit" class="btn btn-outline-primary my-2">Update User</button>
      </form>
    </div>
    <p v-if="error">you are not admin</p>
  </div>

    
  </template>
  
  <script>
  import axios from 'axios';
  import router from '@/router';
import { onUpdated } from 'vue';

  export default {
    data() {
      return {
        searchQuery: '',
        route : router,
        userData: null,
        selectedUser: null,
        error:"",
        users: [],  
        stt: 0
      };
    },
    computed: {
      filteredUsers() {
      // Return the users filtered by the search query
        return this.users.filter(user => {
        return user.name.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
  },
    methods:{
      async fetchUsers(){
        try{
          const token = localStorage.getItem('access_token');
          const response = await axios.get("http://127.0.0.1:8000/user",{
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.userData = response.data;
        }catch(error){
          this.error = "you are not admin!"
        }
        
      },
      async updateUser(){
        try{
          const token = localStorage.getItem('access_token');
          const response = await fetch(`http://127.0.0.1:8000/users/${this.selectedUser.id}`, {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.selectedUser)
        });
        } catch (error) {
        console.error(error);
      }
        await this.fetchUsers(); // Refresh the user list
        this.selectedUser = null; //
        this.searchQuery = null; 
      },
      editUser(user) {
      this.selectedUser = { ...user };  // Create a copy of the user to edit
      },
      async deleteUser(userId){
        if (confirm('Are you sure you want to delete this user?')) {
        try {
          const token = localStorage.getItem('access_token');
          const response = await fetch(`http://127.0.0.1:8000/users/${userId}`, {
            method:'DELETE',
            headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          });

          if (!response.ok) {
            throw new Error('Failed to delete user');
          }

          await this.fetchUsers(); // Refresh the user list
          this.searchQuery = null; 
        } catch (error) {
          console.error(error);
      }
    }
      },
      async queryUsers() {
          try {
              const response = await fetch(`http://127.0.0.1:8000/queryUsers/?name=${this.searchQuery}`);
              this.users = await response.json();
          } catch (error) {
              console.error('Error fetching users:', error);
          }
      },
  },
    async mounted() {
        this.fetchUsers();
    },
    watch: {
    searchQuery: 'queryUsers', // Refetch users whenever the search query changes
  },
  };
  </script>

  <style>
      table tr td{
        border: 1px solid black;
        text-align: center;
      }
  </style>
  