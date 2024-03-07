# Use the official Node.js 14 image as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the main.mjs file to the working directory
COPY main.mjs .

# Set the command to run when the container starts
CMD ["node", "main.mjs"]