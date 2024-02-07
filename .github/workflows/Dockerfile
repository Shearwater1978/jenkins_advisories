name: GitHub Actions Demo
run-name: Dockerfile linting 🚀
on: [push]
jobs:
  Hadolint:
    runs-on: ubuntu-latest
    steps:
        - name: Checkout
          uses: actions/checkout@v3
          
        - name: Validate Dockerfile with Hadolint tools
          run: |
            export VERSION=$(wget -q -O - https://api.github.com/repos/hadolint/hadolint/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
            wget https://github.com/hadolint/hadolint/releases/download/v${VERSION}/hadolint-Linux-x86_64 -O /tmp/hadolint && chmod +x /tmp/hadolint
            /tmp/hadolint -f json --no-fail Dockerfile
        