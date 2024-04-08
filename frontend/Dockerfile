# Use an official Node runtime as a parent image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN yarn install

# Expose port 3000 to the outside world
EXPOSE 3000

# Command to run the application
CMD ["yarn", "start"]