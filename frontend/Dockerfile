# Build stage
FROM node:22-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the project
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

# Copy built files from build stage to nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html/server-status

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Change exposed port from 80 to 1232
EXPOSE 1232

CMD ["nginx", "-g", "daemon off;"]
