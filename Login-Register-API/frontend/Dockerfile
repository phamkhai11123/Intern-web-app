# Use Node.js version 16
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Install npm version 8.x (compatible with Node.js 16)
RUN npm install -g npm@8

# Copy package.json and package-lock.json to the container
COPY package.json package-lock.json ./

# Install dependencies inside the container
RUN npm install

# Copy the rest of the application files to the container
COPY . .

# Expose the port the Vue.js development server will use
EXPOSE 8080

# Start the Vue.js development server using npm run dev
CMD ["npm", "run", "dev"]
