# mcp

## Example servers

### postgresql

```bash
cd official/servers
docker build -t mcp/postgres -f src/postgres/Dockerfile . 

docker run --rm -it --entrypoint sh mcp/postgres

# docker run --rm -it --entrypoint node mcp/postgres dist/index.js 


docker run --rm -i mcp/postgres \
    postgresql://admin:admin@host.docker.internal:5432/agents-backend
```


```bash
cd servers/postgres
npm install
npm run prepare
npx -y @modelcontextprotocol/server-postgres \
    postgresql://admin:admin@localhost:5432/agents-backend
```


```bash
uvicorn server:app --port 8001
```
