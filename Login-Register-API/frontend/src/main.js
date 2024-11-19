import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import yaml from 'js-yaml';
import fs from 'fs';


const app = createApp(App)

app.use(router)

app.mount('#app')



const config = yaml.load(fs.readFileSync('path/to/config.yml', 'utf8'));
console.log("API URL from config.yml:", config.api_url);


