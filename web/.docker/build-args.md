# Docker Build Configuration

If you encounter proxy issues during Docker builds, you can configure Docker to use your system's proxy settings.

## Option 1: Docker Desktop Settings

1. Open Docker Desktop
2. Go to Settings → Resources → Proxies
3. Configure your proxy settings there
4. Docker will use these settings for all builds

## Option 2: Build Arguments

You can pass proxy settings as build arguments:

```bash
docker-compose build \
  --build-arg http_proxy=$http_proxy \
  --build-arg https_proxy=$https_proxy \
  --build-arg HTTP_PROXY=$HTTP_PROXY \
  --build-arg HTTPS_PROXY=$HTTPS_PROXY
```

## Option 3: Docker Config File

Create or edit `~/.docker/config.json`:

```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.example.com:8080",
      "httpsProxy": "http://proxy.example.com:8080",
      "noProxy": "localhost,127.0.0.1"
    }
  }
}
```

## Option 4: Environment Variables

Set proxy environment variables before running docker-compose:

```bash
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080
docker-compose build
```

