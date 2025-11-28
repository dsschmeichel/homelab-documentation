{
  "Chrome Dev Tools": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "chrome-devtools-mcp@latest"
    ],
    "env": {}
  },
  "Ref": {
    "type": "http",
    "url": "https://api.ref.tools/mcp",
    "headers": {
      "x-ref-api-key": "ref-080ceae7f99a78079b4c"
    }
  },
  "Sequential Thinking": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-sequential-thinking"
    ]
  },
  "Task Manager": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@kazuph/mcp-taskmanager"
    ]
  },
  "Fetch": {
    "type": "stdio",
    "command": "uvx",
    "args": [
      "mcp-server-fetch"
    ],
    "env": {}
  }
}
