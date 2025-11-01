FROM node:20-alpine as build

WORKDIR /app

COPY package.json package-lock.json* pnpm-lock.yaml* ./

# Install dependencies
RUN npm ci --legacy-peer-deps

COPY . .

RUN npm run build

FROM node:20-alpine
WORKDIR /app

# Install a simple static server
RUN npm install -g serve

COPY --from=build /app/dist /app/dist

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]