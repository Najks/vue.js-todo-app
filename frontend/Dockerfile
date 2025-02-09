# Base image
FROM node:18

# Nastavi delovni direktorij
WORKDIR /app

# Kopiraj package.json in namesti odvisnosti
COPY package.json .
RUN npm install

# Kopiraj celoten projekt
COPY . .

# Zgradi aplikacijo
RUN npm run build

# Serviraj s statičnim strežnikom
CMD ["npx", "http-server", "dist"]
