# Sử dụng image Node.js chính thức
FROM node:18

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép package.json và package-lock.json vào container
COPY package*.json ./

# Cài đặt các phụ thuộc
RUN npm install

# Sao chép mã nguồn Vue.js vào container
COPY . .


EXPOSE 8081

# Chạy ứng dụng Vue.js trong chế độ phát triển
CMD ["npm", "run", "dev"]
