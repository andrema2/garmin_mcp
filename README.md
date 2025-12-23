[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/taxuspt-garmin-mcp-badge.png)](https://mseep.ai/app/taxuspt-garmin-mcp)

# Garmin MCP Server

This Model Context Protocol (MCP) server connects to Garmin Connect and exposes your fitness and health data to Claude and other MCP-compatible clients.

## Features

- List recent activities
- Get detailed activity information
- Access health metrics (steps, heart rate, sleep)
- View body composition data

## Setup

1. Install the required packages on a new environment:

```bash
uv sync
```

## Running the Server

### Configuration

Your Garmin Connect credentials are read from environment variables:

- `GARMIN_EMAIL`: Your Garmin Connect email address
- `GARMIN_EMAIL_FILE`: Path to a file containing your Garmin Connect email address
- `GARMIN_PASSWORD`: Your Garmin Connect password
- `GARMIN_PASSWORD_FILE`: Path to a file containing your Garmin Connect password
- `GARMIN_MFA_CODE`: One-time MFA code (required when MFA is enabled and tokens are not yet stored)

File-based secrets are useful in certain environments, such as inside a Docker container. Note that you cannot set both `GARMIN_EMAIL` and `GARMIN_EMAIL_FILE`, similarly you cannot set both `GARMIN_PASSWORD` and `GARMIN_PASSWORD_FILE`.

**Important**: The MCP server cannot use interactive input (stdin is used for the MCP protocol). If MFA is required, you must provide the code via the `GARMIN_MFA_CODE` environment variable.

### With Claude Desktop

1. Create a configuration in Claude Desktop:

Edit your Claude Desktop configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add this server configuration:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uvx",
      "args": [
        "--python",
        "3.12",
        "--from",
        "git+https://github.com/Taxuspt/garmin_mcp",
        "garmin-mcp"
      ],
      "env": {
        "GARMIN_EMAIL": "YOUR_GARMIN_EMAIL",
        "GARMIN_PASSWORD": "YOUR_GARMIN_PASSWORD",
        "GARMIN_MFA_CODE": "YOUR_MFA_CODE"
      }
    }
  }
}
```

Replace the path with the absolute path to your server file.

2. Restart Claude Desktop

### With MCP Inspector

For testing, you can use the MCP Inspector from the project root:

```bash
npx @modelcontextprotocol/inspector uv run garmin-mcp
```

## Usage Examples

Once connected in Claude, you can ask questions like:

- "Show me my recent activities"
- "What was my sleep like last night?"
- "How many steps did I take yesterday?"
- "Show me the details of my latest run"

## Security Note

## Troubleshooting

If you encounter login issues:

1. Verify your credentials are correct
2. Check if Garmin Connect requires additional verification
3. Ensure the garminconnect package is up to date

For other issues, check the Claude Desktop logs at:

- macOS: `~/Library/Logs/Claude/mcp-server-garmin.log`
- Windows: `%APPDATA%\Claude\logs\mcp-server-garmin.log`

### Garmin Connect one-time code (MFA)

If you have one-time codes (MFA) enabled in your account, you have two options:

#### Option 1: Initial login via command line (recommended for first-time setup)

The MCP server cannot use interactive input, so for the initial login with MFA, you should run the login script manually at the command line to generate the OAuth tokens.

The app expects either the env var `GARMIN_EMAIL` or `GARMIN_EMAIL_FILE`. You can store these in files with the following command:

```bash
echo "your_email@example.com" > ~/.garmin_email
echo "your_password" > ~/.garmin_password
chmod 600 ~/.garmin_email ~/.garmin_password
```

Then you can manually run the login script (this will prompt for MFA interactively):

```bash
GARMIN_EMAIL_FILE=~/.garmin_email GARMIN_PASSWORD_FILE=~/.garmin_password python -m garmin_mcp
```

Or if you need to provide MFA code via environment variable:

```bash
GARMIN_EMAIL_FILE=~/.garmin_email GARMIN_PASSWORD_FILE=~/.garmin_password GARMIN_MFA_CODE=123456 python -m garmin_mcp
```

After the initial login, OAuth tokens will be stored in `~/.garminconnect` and you won't need to provide credentials or MFA codes again.

#### Option 2: Use GARMIN_MFA_CODE environment variable

If you need to provide MFA during MCP server startup, set the `GARMIN_MFA_CODE` environment variable:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uvx",
      "args": [
        "--python",
        "3.12",
        "--from",
        "git+https://github.com/Taxuspt/garmin_mcp",
        "garmin-mcp"
      ],
      "env": {
        "GARMIN_EMAIL": "YOUR_GARMIN_EMAIL",
        "GARMIN_PASSWORD": "YOUR_GARMIN_PASSWORD",
        "GARMIN_MFA_CODE": "YOUR_MFA_CODE"
      }
    }
  }
}
```

**Note**: After the OAuth tokens are stored (first successful login), you can remove the credentials and MFA code from the environment variables as the tokens will be reused automatically.

```bash
"garmin": {
  "command": "uvx",
  "args": [
    "--python",
    "3.12",
    "--from",
    "git+https://github.com/Taxuspt/garmin_mcp",
    "garmin-mcp"
  ]
}
```
